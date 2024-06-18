# from web_agent import WebAgent
from playwright.async_api import async_playwright
from dotenv import load_dotenv
import json
from collections import defaultdict

load_dotenv()


async def test_ip(headless=True):
    async with async_playwright() as p:

        args = ["--disable-gpu", "--single-process"] if headless else []
        browser = await p.chromium.launch(args=args, headless=headless)

        server = "http://brd.superproxy.io:22225"
        username = "brd-customer-hl_1752fa58-zone-la-ip-91.92.216.78"
        password = "w89q7vd4m95u"

        key = "AQEDAQH9rzUFSmdHAAABkCdqW84AAAGQS3bfzk0AayKUHXTMpBe8mQasWOhyKcyJkptW6eF1f0JIkCVhap8Nht9VLXme3Y1VwwpgoC5BVwSGwP2aqg9BdKlf4PAtTaO7uumiBCM1wUWSEm5TYS5tTG_3"

        proxy = {
            "server": server,
            "username": username,
            "password": password,
        }
        context = await browser.new_context(
            proxy=proxy,
            ignore_https_errors=True,
        )
        li_at = {
            "name": "li_at",
            "value": key,
            "domain": ".www.linkedin.com",
            "path": "/",
            "secure": True,
        }
        await context.add_cookies([li_at])

        page = await context.new_page()

        await page.goto("http://lumtest.com/myip.json")
        await page.wait_for_timeout(2000)

        await page.goto(
            f"https://www.linkedin.com",
            wait_until="domcontentloaded",
        )
        await page.wait_for_timeout(50000000)
        await browser.close()


import asyncio


async def main():
    return await test_ip(headless=False)


print(asyncio.run(main()))
