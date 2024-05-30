# from web_agent import WebAgent
from playwright.async_api import async_playwright
from dotenv import load_dotenv
import json
import os
import random

load_dotenv()

async def security_code(params, headless=True):
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
            context = await browser.new_context(
                storage_state=saved_context, proxy=proxy, ignore_https_errors=True
            )
        else:
            raise Exception("No saved browser session found")

        page = await context.new_page()

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
