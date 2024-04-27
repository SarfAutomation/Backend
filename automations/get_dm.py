import asyncio
from web_agent import WebAgent
from playwright.async_api import async_playwright
import argparse
import requests
import os
from dotenv import load_dotenv
import random
import json

load_dotenv()

port = os.getenv("PORT")


async def main():
    async with async_playwright() as p:
        # Initialize the parser
        parser = argparse.ArgumentParser()

        # Add parameters
        parser.add_argument("-n", type=str)

        # Parse the arguments
        name = parser.parse_args().n

        # name = "Dyllan Liu"
        key = "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G"

        browser = await p.chromium.launch(headless=False)

        context = await browser.new_context()
        page = await context.new_page()

        li_at = {
            "name": "li_at",
            "value": key,
            "domain": ".www.linkedin.com",
            "path": "/",
            "secure": True,
        }
        agent = WebAgent(page)
        await context.add_cookies([li_at])
        await page.goto(
            f"https://www.linkedin.com/messaging/",
            wait_until="domcontentloaded",
        )
        input_selector = "#search-conversations"
        await page.wait_for_selector(input_selector, state="visible")
        await page.type(input_selector, name)
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(random.randint(1000, 3000))
        selector = '//a[contains(@id, "ember") and contains(@class, "ember-view msg-conversation-listitem__link msg-conversations-container__convo-item-link pl3")]'
        try:
            await page.wait_for_selector(
                selector,
                timeout=5000,
            )
        except:
            print(json.dumps({"url": "", "messages": []}))
            await browser.close()
            return
        elements = await page.query_selector_all(selector)
        if elements:
            await elements[0].click()
        await page.wait_for_timeout(random.randint(1000, 3000))
        message_items = await page.query_selector_all(".msg-s-message-list__event")

        result = []

        for item in message_items:
            try:
                sender_name = await item.eval_on_selector(
                    ".msg-s-message-group__name", "node => node.textContent.trim()"
                )
                message_time = await item.eval_on_selector(
                    ".msg-s-message-group__timestamp", "node => node.textContent.trim()"
                )
            except:
                if not sender_name or not message_time:
                    raise Exception()
            message_content = await item.eval_on_selector(
                ".msg-s-event-listitem__body", "node => node.textContent.trim()"
            )

            result.append(
                {"name": sender_name, "time": message_time, "content": message_content}
            )
        print(
            json.dumps(
                {
                    "url": page.url,
                    "messages": result,
                }
            )
        )
        await browser.close()
        return result


asyncio.run(main())
