import asyncio
from web_agent import WebAgent
from playwright.async_api import async_playwright
import argparse
import os
from dotenv import load_dotenv
import random
import html

load_dotenv()

port = os.getenv("PORT")


async def main():
    async with async_playwright() as p:
        # # Initialize the parser
        # parser = argparse.ArgumentParser()

        # # Add parameters
        # parser.add_argument("-a", type=str)
        # parser.add_argument("-c", type=str)
        # parser.add_argument("-k", type=str)

        # # Parse the arguments
        # account = parser.parse_args().a
        # content = parser.parse_args().c
        # key = parser.parse_args().k

        account = "sevda-jannatirad-427ab434"
        content = "Happy to connect!"
        key = "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G"

        browser = await p.chromium.launch(headless=False)

        context = await browser.new_context()
        li_at = {
            "name": "li_at",
            "value": key,
            "domain": ".www.linkedin.com",
            "path": "/",
            "secure": True,
        }
        page = await context.new_page()
        agent = WebAgent(page)
        await context.add_cookies([li_at])
        await page.goto(f"https://www.linkedin.com/in/{account}/")
        await page.wait_for_timeout(random.randint(1000, 3000))
        await page.wait_for_selector(
            "h1.text-heading-xlarge.inline.t-24.v-align-middle.break-words",
        )
        name = await page.text_content(
            "h1.text-heading-xlarge.inline.t-24.v-align-middle.break-words",
        )
        more_actions_buttons = await page.query_selector_all(
            f'[aria-label="More actions"]'
        )
        for more_action_button in more_actions_buttons:
            try:
                await more_action_button.click(timeout=5000)
            except Exception as e:
                print(e)
        connect_buttons = await page.query_selector_all(
            f'[aria-label="Invite {html.escape(name)} to connect"]'
        )
        connect_button_clicked = False
        await page.wait_for_timeout(random.randint(1000, 3000))
        for connect_button in connect_buttons:
            try:
                await connect_button.click(timeout=5000)
                connect_button_clicked = True
            except Exception as e:
                print(e)
        if connect_button_clicked:
            await page.wait_for_timeout(random.randint(1000, 3000))
            await page.wait_for_selector('[aria-label="Add a note"]')
            await page.click('[aria-label="Add a note"]')
            await page.wait_for_timeout(random.randint(1000, 3000))
            await page.type(
                'textarea[name="message"]',
                content,
            )
            await page.wait_for_timeout(random.randint(1000, 3000))
            await page.click(
                ".artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view.ml1"
            )

        await browser.close()


asyncio.run(main())
