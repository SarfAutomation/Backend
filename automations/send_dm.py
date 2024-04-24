import asyncio
from web_agent import WebAgent
from playwright.async_api import async_playwright
import argparse
import requests
import os
from dotenv import load_dotenv
import random

load_dotenv()

port = os.getenv("PORT")


async def main():
    async with async_playwright() as p:
        # # Initialize the parser
        # parser = argparse.ArgumentParser()

        # # Add parameters
        # parser.add_argument("-n", type=str)
        # parser.add_argument("-c", type=str)
        # parser.add_argument("-k", type=str)

        # # Parse the arguments
        # name = parser.parse_args().n
        # content = parser.parse_args().c
        # key = parser.parse_args().k

        name = "Dyllan Liu"
        content = "I am defintely cooking"
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
            f"https://www.linkedin.com/messaging/thread/new/",
            wait_until="domcontentloaded",
        )
        await page.type("input.msg-connections-typeahead__search-field", name)
        await page.wait_for_timeout(1000)
        buttons = await page.query_selector_all(f'button.msg-connections-typeahead__search-result:has-text("{name}")')
        if buttons:
            await buttons[0].click()
        await page.wait_for_timeout(1000)
        selector = 'div[role="textbox"][contenteditable="true"]'
        await page.click(selector)
        await page.type(selector, content)
        send_button_selector = 'button.msg-form__send-button:enabled'
        await page.wait_for_selector(send_button_selector)
        await page.click(send_button_selector)
        await browser.close()

asyncio.run(main())
