# from web_agent import WebAgent
from playwright.async_api import async_playwright
from utils.page import get_secure_page
from dotenv import load_dotenv
import re
import random

load_dotenv()


async def get_recent_connections(params, proxy=None, headless=True):
    async with async_playwright() as p:
        try:
            key = params["key"]
            time_offset = params["time_offset"]
        except:
            raise Exception("Missing params")

        # key = "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G"

        args = ["--disable-gpu", "--single-process"] if headless else []
        browser = await p.chromium.launch(args=args, headless=headless)

        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"

        context, page = await get_secure_page(browser, user_agent, proxy)

        li_at = {
            "name": "li_at",
            "value": key,
            "domain": ".www.linkedin.com",
            "path": "/",
            "secure": True,
        }
        # agent = WebAgent(page)
        await context.add_cookies([li_at])
        await page.goto(
            f"https://www.linkedin.com/mynetwork/invite-connect/connections/",
            wait_until="domcontentloaded",
        )
        await page.wait_for_timeout(random.randint(1000, 10000))

        time_to_value = {
            "minute": 60,
            "hour": 60 * 60,
            "day": 60 * 60 * 24,
            "week": 60 * 60 * 24 * 7,
            "month": 60 * 60 * 24 * 30,
            "year": 60 * 60 * 24 * 365,
        }

        # Initialize previous_height to 0
        previous_height = await page.evaluate("document.body.scrollHeight")
        has_more_content = True

        while has_more_content:
            await page.mouse.wheel(0, 100000)
            await page.wait_for_timeout(random.randint(1000, 10000))
            # Check if the scroll position has changed
            current_height = await page.evaluate("document.body.scrollHeight")
            if current_height == previous_height:
                has_more_content = False  # No more content to load
            else:
                previous_height = current_height
            last_connection_card = await page.query_selector(
                "li.mn-connection-card:last-of-type"
            )
            if last_connection_card:
                time_element = await last_connection_card.query_selector("time")
                time_text = await time_element.text_content() if time_element else ""
                matches = re.search(r"(\d+)\s*(y|m|w|h|d|m)?", time_text)
                if matches:
                    number = int(matches.group(1))
                    unit = matches.group(2)
                    if unit == "y":
                        time_in_days = number * 365
                    elif unit == "m":
                        time_in_days = number * 30
                    elif unit == "w":
                        time_in_days = number * 7
                    elif unit == "d":
                        time_in_days = number
                    else:
                        time_in_days = (
                            number / 24 if unit == "h" else number / 1440
                        )  # hours to days or minutes to days

                    if time_in_days > time_offset:
                        has_more_content = False

            selector = ".mn-connection-card__details"
            await page.wait_for_selector(selector)
            connection_cards = await page.query_selector_all(selector)

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

                    if time_to_value[unit] * number < time_offset:
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

            await page.wait_for_timeout(1500)
            await browser.close()
            return result


# import asyncio

# print(
#     asyncio.run(
#         get_recent_connections(
#             {
#                 "time_offset": 604800,
#                 "key": "AQEDAUcY98sDtbmOAAABj-HmvAAAAAGQBfNAAFYAdr7zDsd59vbrHUV2bV3lMzGRyvkcTbM_CIN4QcC5KCn-jn3EzY7avkPFJDbN2FvsPBrcoXWfle5exbZrORzw8gUYFdox8PFaniEQzlcId1q6_lvn",
#             },
#             headless=False,
#         )
#     )
# )
