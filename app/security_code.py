# from web_agent import WebAgent
from playwright.async_api import async_playwright
from utils.page import get_secure_page
from dotenv import load_dotenv
import random

load_dotenv()

async def security_code(params, proxy=None, headless=True):
    async with async_playwright() as p:
        try:
            url = params["url"]
            code = params["code"]
            saved_context = params["savedContext"]
            proxy_server = params["proxyServer"]
            proxy_username = params["proxyUsername"]
            proxy_password = params["proxyPassword"]
        except:
            raise Exception("Missing params")

        args = ["--disable-gpu", "--single-process"] if headless else []
        browser = await p.chromium.launch(args=args, headless=headless)
        proxy = {
            "server": proxy_server,
            "username": proxy_username,
            "password": proxy_password,
        }
        if saved_context:
            user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
            
            context, page = await get_secure_page(browser, user_agent, proxy, saved_context=saved_context)
        else:
            raise Exception("No saved browser session found")

        # agent = WebAgent(page)
        try:
            await page.goto(
                url,
                wait_until="domcontentloaded",
            )
        except:
            # clear db of the saved browser stuff
            raise Exception("Browser session expired")
        await page.fill("input#input__email_verification_pin", code)
        await page.wait_for_timeout(random.randint(1000, 3000))
        await page.click("button#email-pin-submit-button")
        await page.wait_for_timeout(random.randint(1000, 3000))
        cookies = await context.cookies()
        li_at = ""
        for cookie in cookies:
            if cookie["domain"] == ".www.linkedin.com" and cookie["name"] == "li_at":
                li_at = cookie
        await browser.close()
        if not li_at:
            return {"cookie": "", "error": "Invalid security code"}
        else:
            return {"cookie": li_at, "error": ""}


# import asyncio

# print(
#     asyncio.run(
#         security_code(
#             {
#                 "url": "https://www.linkedin.com/checkpoint/challenge/AgE7noLMz3gEagAAAY-TLd5m3f_uXM8vImXLL6iYwo1_SGo8yokCoUXT10ckD5gCm-xNWwLiCczRQH2_4p0BbRizjCSdlw?ut=02ln4509E-srg1",
#                 "code": "305033",
#             },
#             headless=False,
#         )
#     )
# )
