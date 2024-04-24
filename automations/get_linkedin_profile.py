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
        # parser.add_argument("-k", type=str)

        # # Parse the arguments
        # account = parser.parse_args().a
        # key = parser.parse_args().k

        account = "sevda-jannatirad-427ab434"
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
        await page.goto(f"https://www.linkedin.com/in/{account}/")
        await page.wait_for_timeout(random.randint(1000, 3000))
        await agent.chat(
            """
            give me information about this profile, return in the following JSON format
            {
                "name": "full name",
                "job": "current job title",
                "company": "name of current company",
                "experience": [
                    
                ],
                "education": [
                    "name of education1",
                    "name of education2",
                    ...
                ]
            }            
            """)
        await browser.close()

asyncio.run(main())
