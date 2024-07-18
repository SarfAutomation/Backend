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
        if comment == "[empty message]":
            await browser.close()
            return
        try:
            selector = ".ql-editor"
            await page.wait_for_selector(selector)
            await page.type(selector, comment)
            await page.wait_for_timeout(random.randint(1000, 10000))
            try:
                await page.click(
                    ".comments-comment-box__submit-button.artdeco-button--primary", timeout=5000
                )
            except:
                await page.click('button.m2.artdeco-button.artdeco-button--1.artdeco-button--tertiary.ember-view')
            await page.wait_for_timeout(random.randint(1000, 10000))
        except:
            pass
        await browser.close()
