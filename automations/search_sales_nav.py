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


async def check_scroll_end_within_element(page, selector):
    is_at_bottom = await page.evaluate(
        f"""(selector) => {{
        const element = document.querySelector(selector);
        return Math.abs(element.scrollTop + element.clientHeight - element.scrollHeight) <= 10;
    }}""",
        selector,
    )
    return is_at_bottom


async def scroll_within_element_and_check(page, selector):
    reached_bottom = False
    while not reached_bottom:
        await page.evaluate(
            f"""(selector) => {{
            const element = document.querySelector(selector);
            element.scrollTop += 500;
        }}""",
            selector,
        )
        await page.wait_for_timeout(500)
        reached_bottom = await check_scroll_end_within_element(page, selector)
        if reached_bottom:
            return


async def main():
    async with async_playwright() as p:
        # # Initialize the parser
        # parser = argparse.ArgumentParser()

        # # Add parameters
        # parser.add_argument("-s", type=str)

        # # Parse the arguments
        # search_url = parser.parse_args().s

        search_url = "https://www.linkedin.com/sales/search/people?recentSearchId=3638734740&sessionId=8nfRO4D1Q9C5yn5bwKzSLw%3D%3D&viewAllFilters=true"
        amount = 20

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
        page_count = 1
        result = []
        open_count = 0
        close_count = 0
        while open_count < amount:
            await page.goto(
                f"{search_url}&page={page_count}",
                wait_until="domcontentloaded",
            )
            selector = "div.artdeco-entity-lockup__content"
            await page.wait_for_selector(selector)
            scrollable_element_selector = "#search-results-container"
            await scroll_within_element_and_check(page, scrollable_element_selector)
            list_items = await page.query_selector_all(selector)
            for item in list_items:
                if open_count >= amount:
                    break
                premium_icon = await item.query_selector(
                    'li-icon[type="linkedin-premium-gold-icon"]'
                )
                if not premium_icon and close_count > amount:
                    continue
                name_element = await item.query_selector(
                    'span[data-anonymize="person-name"]'
                )
                name = await name_element.text_content()
                name = name.strip()
                await page.wait_for_timeout(random.randint(1000, 3000))
                profile_link_selector = 'a.inverse-link-on-a-light-background-without-visited-and-hover:has-text("View profile")'
                dropdown_hidden = True
                while dropdown_hidden:
                    try:
                        selector = f'button[aria-label="See more actions for {name}"]'
                        await page.wait_for_selector(selector)
                        button = await page.query_selector(selector)
                        await button.click(timeout=1000)
                        await page.wait_for_selector(
                            profile_link_selector, timeout=1000
                        )
                        dropdown_hidden = False
                    except Exception as e:
                        pass
                href = await page.get_attribute(profile_link_selector, "href")
                result.append(
                    {
                        "url": "https://www.linkedin.com/" + href,
                        "isOpen": premium_icon is not None,
                    }
                )
                if premium_icon:
                    open_count += 1
            page_count += 1
        print(json.dumps(result))
        await browser.close()


asyncio.run(main())
