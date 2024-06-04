#from web_agent import WebAgent
from playwright.async_api import async_playwright
from utils.page import get_secure_page
from dotenv import load_dotenv
import re

load_dotenv()

async def get_recent_connections(params, proxy=None, headless=True):
    async with async_playwright() as p:
        try:
            key = params["key"]
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
        #agent = WebAgent(page)
        await context.add_cookies([li_at])
        await page.goto(
            f"https://www.linkedin.com/mynetwork/invite-connect/connections/",
            wait_until="domcontentloaded",
        )
        selector = ".mn-connection-card__details"
        await page.wait_for_selector(selector)
        connection_cards = await page.query_selector_all(selector)

        time_to_value = {
            "minute": 60,
            "hour": 60 * 60,
            "day": 60 * 60 * 24,
            "week": 60 * 60 * 24 * 7,
            "month": 60 * 60 * 24 * 30,
            "year": 60 * 60 * 24 * 365,
        }

        time_offset = time_to_value["day"]

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
