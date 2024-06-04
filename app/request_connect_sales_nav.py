#from web_agent import WebAgent
from playwright.async_api import async_playwright
from utils.page import get_secure_page
from dotenv import load_dotenv
import random

load_dotenv()

async def request_connect_sales_nav(params, proxy=None, headless=True):
    async with async_playwright() as p:
        try:
            profile_url = params["profile_url"]
            message = params["message"]
            key = params["key"]
        except:
            raise Exception("Missing params")

        # profile_url = "https://www.linkedin.com/sales/lead/ACwAAC8j2XgB9klQz4mACtczFI4opqIqQM4o1fg,NAME_SEARCH,nQAI"
        # message = "Happy to connect!"
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
        await page.goto(profile_url)
        try:
            await page.wait_for_timeout(random.randint(1000, 3000))
            await page.click('button[aria-label="Open actions overflow menu"]')
            await page.wait_for_timeout(random.randint(1000, 3000))
            await page.wait_for_selector("text=Connect", state="visible")
            await page.click("text=Connect")
            await page.wait_for_timeout(random.randint(1000, 3000))
            await page.type(
                f'textarea[id="connect-cta-form__invitation"]',
                message,
            )
            await page.wait_for_timeout(random.randint(1000, 3000))
            await page.wait_for_selector(
                ".button-primary-medium.connect-cta-form__send", state="visible"
            )
            await page.click(".button-primary-medium.connect-cta-form__send")
            await page.wait_for_timeout(random.randint(1000, 3000))
            await browser.close()
            return {"crSent": True}
        except:
            await browser.close()
            return {"crSent": False}
