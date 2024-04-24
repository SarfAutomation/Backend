import asyncio
from web_agent import WebAgent
from playwright.async_api import async_playwright
import argparse
from urllib.parse import quote
import requests
import os
from dotenv import load_dotenv
import random
import time
import html
import json

load_dotenv()

port = os.getenv("PORT")


def extract_user_id_from_linkedin_url(url):
    parts = url.rstrip("/").split("/")
    user_id = parts[-1]
    return user_id


async def main():
    async with async_playwright() as p:
        # Initialize the parser
        parser = argparse.ArgumentParser()

        # Add parameters
        parser.add_argument("-p", type=str)
        parser.add_argument("-m", type=str)
        parser.add_argument("-s", type=str)

        # Parse the arguments
        profile_link = parser.parse_args().p
        message = parser.parse_args().m
        subject = parser.parse_args().s

        # profile_link = "https://www.linkedin.com/sales/lead/ACwAAC8j2XgB9klQz4mACtczFI4opqIqQM4o1fg,NAME_SEARCH,nQAI"

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
        await page.goto("https://www.linkedin.com/")
        await context.add_cookies([li_at])
        await page.reload()
        result = []
        await page.goto(
            profile_link,
            wait_until="domcontentloaded",
        )
        selector = 'span[data-anonymize="person-name"]'
        await page.wait_for_selector(selector)
        name_element = await page.query_selector(selector)
        name = await name_element.text_content()
        name = name.strip()
        button_selector = 'button:has-text("Message")'
        await page.click(button_selector)
        subject_selector = "input.compose-form__subject-field"
        message_selector = "textarea.compose-form__message-field"
        try:
            await page.type(subject_selector, subject, timeout=5000)
            await page.wait_for_timeout(random.randint(1000, 3000))
        except:
            pass
        await page.type(message_selector, message)
        await page.wait_for_timeout(random.randint(1000, 3000))
        send_button_selector = 'button:has-text("Send")'
        await page.wait_for_selector(send_button_selector, state="attached")
        await page.wait_for_timeout(random.randint(1000, 3000))
        button_enabled = await page.is_enabled(send_button_selector)
        if button_enabled:
            print(json.dumps("Button is enabled; can click."))
            # await page.click(send_button_selector)
        else:
            print(json.dumps("Button is disabled; cannot click."))
        await page.wait_for_timeout(random.randint(1000, 3000))
        selector = f'button:has(span:has-text("Close conversation with {name}"))'
        await page.click(selector)
        await browser.close()
        return result


asyncio.run(main())
