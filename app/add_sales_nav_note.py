#from web_agent import WebAgent
from playwright.async_api import async_playwright
from utils.page import get_secure_page
from dotenv import load_dotenv
import random

load_dotenv()

def extract_user_id_from_linkedin_url(url):
    parts = url.rstrip("/").split("/")
    user_id = parts[-1]
    return user_id


async def add_sales_nav_note(params, proxy=None, headless=True):
    async with async_playwright() as p:
        try:
            profile_link = params["profile_link"]
            note = params["note"]
            key = params["key"]
        except:
            raise Exception("Missing params")

        # profile_link = "https://www.linkedin.com/sales/lead/ACwAAAMVEXABsl8VD2KrgEnF-_i5p5-91p_FB6Y,NAME_SEARCH,sNNr"

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
            profile_link,
            wait_until="domcontentloaded",
        )
        selector = 'span[data-anonymize="person-name"]'
        await page.wait_for_selector(selector)
        name_element = await page.query_selector(selector)
        name = await name_element.text_content()
        name = name.strip()
        await page.wait_for_timeout(random.randint(1000, 3000))
        button_selector = 'button[aria-label="Add note"]'
        await page.click(button_selector)
        await page.wait_for_timeout(random.randint(1000, 3000))
        button_selector = 'text="Add note"'
        button = await page.query_selector(button_selector)
        if button:
            await button.click()
            await page.wait_for_timeout(random.randint(1000, 3000))
        textarea_selector = 'textarea[name="sharing-entity-notes-vertical-list-widget-card__textarea-name"]'
        await page.type(textarea_selector, note)
        await page.wait_for_timeout(random.randint(1000, 3000))
        button_selector = (
            'button[aria-label="Done making changes to note, save these edits"]'
        )
        await page.wait_for_selector(f"{button_selector}:not([disabled])")
        await page.click(button_selector)
        await page.wait_for_timeout(1500)
        await browser.close()
