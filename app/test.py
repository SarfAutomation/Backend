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
        username = "brd-customer-hl_1752fa58-zone-la-ip-46.232.208.187"
        password = "w89q7vd4m95u"

        proxy = {
            "server": server,
            "username": username,
            "password": password,
        }
        context = await browser.new_context(
            proxy=proxy,
            # geolocation={"latitude": 34.0522, "longitude": -118.2437},
            # permissions=["geolocation"],
            ignore_https_errors=True,
        )

        page = await context.new_page()

        # agent = WebAgent(page)

        await page.goto("http://lumtest.com/myip.json")
        return await page.text_content("body")
        


import asyncio


async def main():
    result_dict = defaultdict(int)
    for i in range(1000):
        result = json.loads(await test_ip())
        print(i, result["ip"])
        result_dict[result["ip"]] += 1



print(asyncio.run(main()))
