import asyncio
from web_agent import WebAgent
from playwright.async_api import async_playwright
import argparse
import requests
import os
from dotenv import load_dotenv
import random
import re
import json

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
        await page.goto("https://www.linkedin.com/")
        await context.add_cookies([li_at])
        await page.reload()

        await page.goto(
            f"https://www.linkedin.com/mynetwork/invite-connect/connections/",
            wait_until="domcontentloaded",
        )
        selector = ".mn-connection-card__details"
        await page.wait_for_selector(selector)
        # Select all elements with the time information and their respective details container
        connection_cards = await page.query_selector_all(selector)

        time_offset = 60 * 60 * 24

        time_to_value = {
            "minute": 60,
            "hour": 60 * 60,
            "day": 60 * 60 * 24,
            "week": 60 * 60 * 24 * 7,
            "month": 60 * 60 * 24 * 30,
            "year": 60 * 60 * 24 * 365,
        }

        result = []

        for card in connection_cards:
            time_element = await card.query_selector("time")
            time_text = await time_element.text_content() if time_element else ""

            matches = re.search(
                r"(\d+)\s*(year|month|week|hour|day|minute)s? ago", time_text
            )
            if matches:
                number = int(matches.group(1))
                unit = matches.group(2)

                if time_to_value[unit] * number <= time_offset:
                    link_element = await card.query_selector(
                        "a.mn-connection-card__link"
                    )
                    href = (
                        await link_element.get_attribute("href")
                        if link_element
                        else None
                    )
                    if href:
                        result.append("https://www.linkedin.com" + href)
                else:
                    break

        # Output filtered connections
        print(json.dumps(result))
        await page.wait_for_timeout(1500)
        await browser.close()


asyncio.run(main())
