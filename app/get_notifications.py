# from web_agent import WebAgent
from playwright.async_api import async_playwright
from utils.page import get_secure_page
from dotenv import load_dotenv
import random
import re

load_dotenv()


async def get_notifications(params, proxy=None, headless=True):
    async with async_playwright() as p:
        try:
            key = params["key"]
            time_offset = params["time_offset"]
        except:
            raise Exception("Missing params")
        
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
        await page.goto("https://www.linkedin.com/notifications/?filter=all")

        # Wait for the notifications to load
        await page.wait_for_selector('div[data-finite-scroll-hotkey-item="0"]')

        # Initialize previous_height to 0
        previous_height = await page.evaluate("document.body.scrollHeight")
        has_more_content = True

        time_to_value = {
            "m": 60,
            "h": 60 * 60,
            "d": 60 * 60 * 24,
            "w": 60 * 60 * 24 * 7,
        }

        while has_more_content:
            await page.mouse.wheel(0, 100000)
            await page.wait_for_timeout(random.randint(1000, 10000))
            # Check if the scroll position has changed
            current_height = await page.evaluate("document.body.scrollHeight")
            if current_height == previous_height:
                has_more_content = False  # No more content to load
            else:
                previous_height = current_height
            last_notification = await page.query_selector('div[data-finite-scroll-hotkey-item]:last-of-type article.nt-card')
            if last_notification:
                time_ago = await last_notification.query_selector('p.nt-card__time-ago')
                time_ago_text = await time_ago.text_content()
                matches = re.search(
                r"(\d+)\s*(y|m|w|h|d|m)?", time_ago_text
                )
                if matches:
                    number = int(matches.group(1))
                    unit = matches.group(2)
                    if time_to_value[unit] * number > time_offset:
                        has_more_content = False

        # Locate all notification cards
        notifications = await page.query_selector_all(
            "div[data-finite-scroll-hotkey-item] article.nt-card"
        )
        results = []
        for notification in notifications:
            # Extract data from each notification
            headline = await notification.query_selector("a.nt-card__headline")
            headline_text = await headline.text_content() if headline else "No headline"

            # Extract the link from the 'a' tag
            link_element = await last_notification.query_selector('a.nt-card__headline')
            link = await link_element.get_attribute('href') if link_element else "No link"

            time_ago = await notification.query_selector("p.nt-card__time-ago")
            time_ago_text = (
                await time_ago.text_content() if time_ago else "No time info"
            )

            # Extract the name from the headline
            strong_tag = await headline.query_selector('strong')
            if strong_tag:
                name = await strong_tag.text_content()
            else:
                name_span = await headline.query_selector('span')
                if name_span:
                    name = await name_span.inner_text()
                else:
                    name = "No name"

            results.append(
                {
                    "name": name,
                    "headline": headline_text.strip(),
                    "url": link,
                    "time_ago": time_ago_text.strip(),
                }
            )
        await browser.close()
        return results


# import asyncio

# print(
#     asyncio.run(
#         get_notifications(
#             {
#                 "key": "AQEDAUcY98sDLr69AAABkA1loggAAAGQMXImCE0AW_qP6zUvtK1Jc0hQK3oIcIL4exWekbv1B4anqzMzkzAKwAm0pccaEqDvhSFah1gqDVYNwH4VzOo-iTSZyk9bBkcAnGkm4QrncsHPjMHqSET18bqB",
#                 "time_offset": 60 * 60 * 3,
#             },
#             headless=False,
#         )
#     )
# )
