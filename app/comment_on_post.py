# from web_agent import WebAgent
from playwright.async_api import async_playwright
import random
from dotenv import load_dotenv

load_dotenv()


async def comment_on_post(params, headless=True):
    async with async_playwright() as p:
        try:
            post_url = params["post_url"]
            comment = params["comment"]
            key = params["key"]
        except:
            raise Exception("Missing params")

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
        # agent = WebAgent(page)
        await context.add_cookies([li_at])
        await page.goto(
            post_url,
            wait_until="domcontentloaded",
        )
        selector = '.ql-editor'
        await page.wait_for_selector(selector)
        await page.fill(selector, comment)
        await page.wait_for_timeout(random.randint(1000, 3000))
        # selector = ".comments-comment-box__submit-button.artdeco-button--primary"
        # await page.click(".comments-comment-box__submit-button.artdeco-button--primary")
        await page.wait_for_timeout(10000)
        await browser.close()


# import asyncio

# asyncio.run(
#     comment_on_post(
#         {"post_url": "https://www.linkedin.com/posts/y-combinator_why-yc-activity-7049158009503051776-N8FG/", "comment": "hi", "key": ""}, headless=False
#     )
# )