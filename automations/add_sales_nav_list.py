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
        parser.add_argument("-l", type=str)

        # Parse the arguments
        profile_link = parser.parse_args().p
        list = parser.parse_args().l

        # profile_link = "https://www.linkedin.com/sales/lead/ACwAAAMVEXABsl8VD2KrgEnF-_i5p5-91p_FB6Y,NAME_SEARCH,sNNr"

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
        await page.goto(
            profile_link,
            wait_until="domcontentloaded",
        )
        await page.wait_for_timeout(random.randint(1000, 3000))
        await page.click('button[aria-label*="Save to list"]')
        await page.wait_for_timeout(random.randint(1000, 3000))
        await page.wait_for_selector(f'text={list}', state='visible')
        await page.click(f'text={list}')
        print(json.dumps("Done"))
        await page.wait_for_timeout(1500)
        await browser.close()

asyncio.run(main())
