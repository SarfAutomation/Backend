import asyncio
from web_agent import WebAgent
from playwright.async_api import async_playwright
import argparse
import os
from dotenv import load_dotenv
import random
import html
import json

load_dotenv()

port = os.getenv("PORT")


async def main():
    async with async_playwright() as p:
        # Initialize the parser
        parser = argparse.ArgumentParser()

        # Add parameters
        parser.add_argument("-l", type=str)

        # Parse the arguments
        linkedinUrl = parser.parse_args().l

        # linkedinUrl = "https://www.linkedin.com/in/adriennekfong"
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
        await page.goto(linkedinUrl)
        await page.wait_for_selector(
            "h1.text-heading-xlarge.inline.t-24.v-align-middle.break-words"
        )
        name = await page.text_content(
            "h1.text-heading-xlarge.inline.t-24.v-align-middle.break-words"
        )
        link_selector = 'a:has-text("Message in Sales Navigator")'
        href = await page.get_attribute(link_selector, 'href')
        await page.goto(href)
        await page.wait_for_timeout(random.randint(1000, 3000))
        selector = f'button:has(span:has-text("Close conversation with {name}"))'
        await page.wait_for_selector(selector)
        await page.click(selector)
        button_selector = 'button[aria-label="Add note"]'
        await page.wait_for_selector(button_selector)
        await page.click(button_selector)
        await page.wait_for_timeout(random.randint(1000, 3000))
        try:
            note_selector = (
                ".sharing-entity-notes-vertical-list-widget-card .p2.break-words"
            )
            await page.wait_for_selector(note_selector, 5000)
            contains_new_connection = await page.evaluate(
                """() => {
                const elements = document.querySelectorAll('.sharing-entity-notes-vertical-list-widget-card .p2.break-words');
                return Array.from(elements).some(el => el.textContent.includes("New Connection"));
            }"""
            )
            if contains_new_connection:
                print(json.dumps({"name": name, "url": page.url}))
                return
        except:
            pass
        print(json.dumps({"name": "", "url": ""}))
        await browser.close()


asyncio.run(main())
