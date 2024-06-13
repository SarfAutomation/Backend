# from web_agent import WebAgent
from playwright.async_api import async_playwright
from utils.page import get_secure_page
import random
from dotenv import load_dotenv

load_dotenv()


async def comment_on_post(params, proxy=None, headless=True):
    async with async_playwright() as p:
        try:
            post_url = params["post_url"]
            comment = params["comment"]
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
        await page.goto(
            post_url,
            wait_until="domcontentloaded",
        )
        selector = 'button[aria-label="React Like"]'
        await page.wait_for_selector(selector)
        await page.click(selector)
        await page.wait_for_timeout(random.randint(1000, 10000))
        try:
            selector = ".ql-editor"
            await page.wait_for_selector(selector)
            await page.fill(selector, comment)
            await page.wait_for_timeout(random.randint(1000, 10000))
            selector = ".comments-comment-box__submit-button.artdeco-button--primary"
            await page.click(
                ".comments-comment-box__submit-button.artdeco-button--primary"
            )
            await page.wait_for_timeout(random.randint(1000, 10000))
        except:
            pass
        await browser.close()


# import asyncio

# key = "AQEDAUcY98sDtbmOAAABj-HmvAAAAAGQBfNAAFYAdr7zDsd59vbrHUV2bV3lMzGRyvkcTbM_CIN4QcC5KCn-jn3EzY7avkPFJDbN2FvsPBrcoXWfle5exbZrORzw8gUYFdox8PFaniEQzlcId1q6_lvn"

# asyncio.run(
#     comment_on_post(
#         {
#             "post_url": "https://www.linkedin.com/posts/songanglu_big-news-brewit-yc-w23-now-supports-activity-7204157548009050113-Jhwd/?utm_source=share&utm_medium=member_desktop",
#             "comment": "hi",
#             "key": key,
#         },
#         headless=False,
#     )
# )
