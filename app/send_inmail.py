#from web_agent import WebAgent
from playwright.async_api import async_playwright
from dotenv import load_dotenv
import random

load_dotenv()

def extract_user_id_from_linkedin_url(url):
    parts = url.rstrip("/").split("/")
    user_id = parts[-1]
    return user_id


async def send_inmail(params, headless=True):
    async with async_playwright() as p:
        try:
            profile_link = params["profile_link"]
            message = params["message"]
            subject = params["subject"]
            key = params["key"]
        except:
            raise Exception("Missing params")

        # profile_link = "https://www.linkedin.com/sales/lead/ACwAAC8j2XgB9klQz4mACtczFI4opqIqQM4o1fg,NAME_SEARCH,nQAI"
        # message = "Hello"
        # subject = "Hello"

        # key = "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G"

        args = ["--disable-gpu", "--single-process"] if headless else []
        browser = await p.chromium.launch(args=args, headless=headless)

        context = await browser.new_context()
        li_at = {
            "name": "li_at",
            "value": key,
            "domain": ".www.linkedin.com",
            "path": "/",
            "secure": True,
        }
        page = await context.new_page()
        #agent = WebAgent(page)
        await context.add_cookies([li_at])
        await page.goto(
            profile_link,
            wait_until="domcontentloaded",
        )
        await page.wait_for_timeout(random.randint(1000, 3000))
        selector = 'span[data-anonymize="person-name"]'
        await page.wait_for_selector(selector)
        name_element = await page.query_selector(selector)
        name = await name_element.text_content()
        name = name.strip()
        button_selector = '[data-anchor-send-inmail]'
        await page.wait_for_selector(button_selector, state='visible')
        await page.click(button_selector)
        subject_selector = "input.compose-form__subject-field"
        message_selector = "textarea.compose-form__message-field"
        try:
            await page.type(subject_selector, subject, timeout=5000)
            await page.wait_for_timeout(random.randint(1000, 3000))
        except:
            pass
        await page.type(message_selector, message)
        await page.wait_for_timeout(random.randint(1000, 3000))
        send_button_selector = 'button:has-text("Send")'
        await page.wait_for_selector(send_button_selector, state="attached")
        await page.wait_for_timeout(random.randint(1000, 3000))
        button_enabled = await page.is_enabled(send_button_selector)
        if button_enabled:
            await page.click(send_button_selector)
        else:
            raise Exception("Failed to click send button")
        await page.wait_for_timeout(random.randint(1000, 3000))
        selector = f'button:has(span:has-text("Close conversation with {name}"))'
        await page.click(selector)
        await browser.close()
