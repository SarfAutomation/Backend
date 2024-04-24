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

load_dotenv()

port = os.getenv("PORT")


def extract_user_id_from_linkedin_url(url):
    parts = url.rstrip("/").split("/")
    user_id = parts[-1]
    return user_id


async def main():
    async with async_playwright() as p:
        # # Initialize the parser
        # parser = argparse.ArgumentParser()

        # # Add parameters
        # parser.add_argument("-s", type=str)
        # parser.add_argument("-a", type=str)
        # parser.add_argument("-k", type=str)

        # # Parse the arguments
        # searchTerm = parser.parse_args().s
        # amount = parser.parse_args().a
        # key = parser.parse_args().k

        searchTerm = "software QA"
        amount = 5
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
        page_count = 1
        result = []
        while len(result) < amount:
            await page.goto(
                f"https://www.linkedin.com/search/results/people/?keywords={quote(searchTerm)}&page={page_count}",
                wait_until="domcontentloaded",
            )
            for i in range(10):
                await page.wait_for_timeout(random.randint(1000, 3000))
                person_selector = f"//li[contains(@class, 'reusable-search__result-container')][{i+1}]"
                await page.wait_for_selector(person_selector, timeout=5000)
                await page.click(person_selector, force=True, timeout=5000)
                await page.wait_for_timeout(random.randint(1000, 3000))
                result.append(extract_user_id_from_linkedin_url(page.url))
                await page.go_back()
                if len(result) >= amount:
                    break
            page_count += 1
        print(result)
        await browser.close()
        return result


asyncio.run(main())
