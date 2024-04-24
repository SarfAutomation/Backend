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
        await page.goto("https://www.linkedin.com/")
        await context.add_cookies([li_at])
        await page.reload()
        await page.goto("https://www.linkedin.com/sales/inbox")

        input_selector = "#left-rail-inbox-search"

        await page.type(input_selector, name)
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(random.randint(1000, 3000))
        link_selector = (
            "li[data-x-conversation-list-item] a.conversation-list-item__link"
        )
        try:
            await page.wait_for_selector(link_selector, timeout=5000)
        except:
            print(json.dumps({"url": "", "messages": []}))
            return
        link_element = await page.query_selector(link_selector)
        href = await link_element.get_attribute("href")
        selector = "article.relative.mt4, article.relative.mb4"
        await page.wait_for_selector(selector)
        articles = await page.query_selector_all(
            "article.relative.mt4, article.relative.mb4"
        )
        result = []
        for article in articles:
            try:
                selector = 'span[aria-label="Message from you"]'
                fromYou = await article.query_selector(selector)
                if fromYou:
                    sender_name = "You"
                else:
                    sender_name = await article.eval_on_selector(
                        'span[data-anonymize="person-name"]',
                        "node => node.textContent.trim()",
                    )

                message_time = await article.eval_on_selector(
                    "time", "node => node.textContent.trim()"
                )
            except:
                if not sender_name or not message_time:
                    raise Exception()
            message_content = await article.eval_on_selector(
                'p[data-anonymize="general-blurb"]', "node => node.textContent.trim()"
            )
            result.append(
                {"name": sender_name, "time": message_time, "content": message_content}
            )
        print(
            json.dumps(
                {
                    "url": "https://www.linkedin.com/sales/inbox/" + href,
                    "messages": result,
                }
            )
        )
        await page.wait_for_timeout(1500)
        await browser.close()
        return result


asyncio.run(main())
