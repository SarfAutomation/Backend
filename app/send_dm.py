#from web_agent import WebAgent
from playwright.async_api import async_playwright
from utils.page import get_secure_page
from dotenv import load_dotenv

load_dotenv()

async def send_dm(params, proxy=None, headless=True):
    async with async_playwright() as p:
        try:
            name = params["name"]
            content = params["content"]
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
        #agent = WebAgent(page)
        await context.add_cookies([li_at])
        await page.goto(
            f"https://www.linkedin.com/messaging/thread/new/",
            wait_until="domcontentloaded",
        )
        await page.type("input.msg-connections-typeahead__search-field", name)
        await page.wait_for_timeout(1000)
        buttons = await page.query_selector_all(f'button.msg-connections-typeahead__search-result:has-text("{name}")')
        if buttons:
            await buttons[0].click()
        await page.wait_for_timeout(1000)
        selector = 'div[role="textbox"][contenteditable="true"]'
        await page.click(selector)
        await page.type(selector, content)
        send_button_selector = 'button.msg-form__send-button:enabled'
        await page.wait_for_selector(send_button_selector)
        await page.click(send_button_selector)
        await browser.close()
