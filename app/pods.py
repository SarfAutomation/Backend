# from web_agent import WebAgent
from playwright.async_api import async_playwright
from dotenv import load_dotenv
import random

load_dotenv()


async def comment_on_post(params, proxy=None, headless=True):
    async with async_playwright() as p:
        try:
            post_url = params["post_url"]
            comment = params["comment"]
            key = params["key"]
            ip = params["ip"]
        except:
            raise Exception("Missing params")        

        args = ["--disable-gpu", "--single-process"] if headless else []
        browser = await p.chromium.launch(args=args, headless=headless)

        if ip:
            server = "http://brd.superproxy.io:22225"
            username = f"brd-customer-hl_1752fa58-zone-residential_proxy1-ip-{ip}"
            password = "c1fyk3kmxt8u"

            server = "http://brd.superproxy.io:22225"
            username = "brd-customer-hl_1752fa58-zone-residential_proxy1-gip-18fc1db942000000"
            password = "c1fyk3kmxt8u"

            proxy = {
                "server": server,
                "username": username,
                "password": password,
            }
            context = await browser.new_context(proxy=proxy, ignore_https_errors=True)
        else:
            context = await browser.new_context()

        page = await context.new_page()

        li_at = {
            "name": "li_at",
            "value": key,
            "domain": ".www.linkedin.com",
            "path": "/",
            "secure": True,
        }
        # agent = WebAgent(page)

        await page.goto("http://lumtest.com/myip.json")
        await page.wait_for_timeout(10000)

        await context.add_cookies([li_at])

        await page.goto(
            post_url,
            wait_until="domcontentloaded",
        )
        await page.wait_for_timeout(1000000)

        selector = ".ql-editor"
        await page.wait_for_selector(selector)
        await page.fill(selector, comment)
        await page.wait_for_timeout(random.randint(1000, 3000))
        await page.wait_for_timeout(1000000)
        # selector = ".comments-comment-box__submit-button.artdeco-button--primary"
        # await page.click(".comments-comment-box__submit-button.artdeco-button--primary")
        await browser.close()


import asyncio


async def main():
    # Create task objects for each function
    tasks = [
        # comment_on_post(
        #     {
        #         "post_url": "https://www.linkedin.com/posts/y-combinator_why-yc-activity-7049158009503051776-N8FG/",
        #         "comment": "good",
        #         "key": "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G",
        #         "ip": None,
        #     },
        #     headless=False,
        # ),
        comment_on_post(
            {
                "post_url": "https://www.linkedin.com/",
                "comment": "excellent",
                "key": "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G",
                "ip": "161.77.194.240",
            },
            headless=False,
        ),
        # comment_on_post(
        #     {
        #         "post_url": "https://www.linkedin.com/posts/y-combinator_why-yc-activity-7049158009503051776-N8FG/",
        #         "comment": "impressive",
        #         "key": "AQEDASy_h8kCCaUHAAABjptS_jkAAAGPVmNT9E0AZZT2gfCk6kVmp_3nybVyOouQZDkXKnkaLeGqdGLXKc7QtD_u7ctpXzbsfRaaIN61FluyEjvogS4GX9m5MkInF9esmxOxeUj3CnZENBZp4rykXO8z",
        #         "ip": "161.77.196.235",
        #     },
        #     headless=False,
        # ),
    ]
    # Wait for all tasks to complete
    await asyncio.gather(*tasks)


# asyncio.run(main())
