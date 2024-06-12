# from web_agent import WebAgent
from playwright.async_api import async_playwright
from utils.page import get_secure_page
from dotenv import load_dotenv
import random

load_dotenv()


async def get_linkedin_url(params, proxy=None, headless=True):
    async with async_playwright() as p:
        try:
            sales_nav_url = params["sales_nav_url"]
            key = params["key"]
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
        await page.goto(sales_nav_url)
        await page.wait_for_timeout(random.randint(1000, 10000))
        await page.click('button[aria-label="Open actions overflow menu"]')
        linkedin_profile_href = await page.get_attribute(
            'a._item_1xnv7i[href*="linkedin.com/in"]', "href"
        )
        await page.wait_for_timeout(random.randint(1000, 10000))
        await browser.close()
        return {"url": linkedin_profile_href}


# import asyncio

# print(
#     asyncio.run(
#         get_linkedin_url(
#             {
#                 "sales_nav_url": "https://www.linkedin.com/sales/lead/ACwAAAEEI3IBmp8jHBArVc6xzUAu5HZZFEdQpxo,NAME_SEARCH,Kxdu?_ntb=iWPfJTyQQkSan6%2B6oe0FLQ%3D%3D",
#                 "key": "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G",
#             },
#             headless=False,
#         )
#     )
# )
