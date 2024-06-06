# from web_agent import WebAgent
from playwright.async_api import async_playwright
from utils.page import get_secure_page
from dotenv import load_dotenv
import random
import html

load_dotenv()


async def request_connect_linkedin(params, proxy=None, headless=True):
    async with async_playwright() as p:
        try:
            linkedin_url = params["linkedin_url"]
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
        # agent = WebAgent(page)
        await context.add_cookies([li_at])
        await page.goto(linkedin_url)
        await page.wait_for_timeout(random.randint(1000, 3000))
        await page.wait_for_selector(
            "h1.text-heading-xlarge.inline.t-24.v-align-middle.break-words",
        )
        name = await page.text_content(
            "h1.text-heading-xlarge.inline.t-24.v-align-middle.break-words",
        )
        more_actions_buttons = await page.query_selector_all(
            f'[aria-label="More actions"]'
        )
        for more_action_button in more_actions_buttons:
            try:
                await more_action_button.click(timeout=5000)
            except Exception as e:
                print(e)
        connect_buttons = await page.query_selector_all(
            f'[aria-label="Invite {html.escape(name)} to connect"]'
        )
        connect_button_clicked = False
        await page.wait_for_timeout(random.randint(1000, 3000))
        for connect_button in connect_buttons:
            try:
                await connect_button.click(timeout=5000)
                connect_button_clicked = True
            except Exception as e:
                print(e)
        if connect_button_clicked:
            await page.wait_for_timeout(random.randint(1000, 3000))
            await page.wait_for_selector('[aria-label="Add a note"]')
            await page.click('[aria-label="Add a note"]')
            await page.wait_for_timeout(random.randint(1000, 3000))
            await page.type(
                'textarea[name="message"]',
                content,
            )
            await page.wait_for_timeout(random.randint(1000, 3000))
            # await page.click(
            #     ".artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view.ml1"
            # )
            await page.wait_for_timeout(10000)

        await browser.close()
