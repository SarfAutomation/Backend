# from web_agent import WebAgent
from playwright.async_api import async_playwright
from dotenv import load_dotenv
import random

load_dotenv()


async def get_dm(params, headless=True):
    async with async_playwright() as p:
        try:
            name = params["name"]
            key = params["key"]
        except:
            raise Exception("Missing params")

        # name = "Dyllan Liu"
        # key = "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G"

        args = ["--disable-gpu", "--single-process"] if headless else []
        browser = await p.chromium.launch(args=args, headless=headless)

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
        await context.add_cookies([li_at])
        await page.goto(
            f"https://www.linkedin.com/messaging/",
            wait_until="domcontentloaded",
        )
        input_selector = "#search-conversations"
        await page.wait_for_selector(input_selector, state="visible")
        await page.type(input_selector, name)
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(random.randint(1000, 3000))
        selector = "a.msg-conversation-listitem__link.msg-conversations-container__convo-item-link.pl3"
        try:
            await page.wait_for_selector(
                selector,
                timeout=5000,
            )
        except:
            await browser.close()
            return {"url": "", "messages": []}
        elements = await page.query_selector_all(selector)
        if elements:
            await elements[0].click()
        await page.wait_for_timeout(random.randint(1000, 3000))
        message_items = await page.query_selector_all(".msg-s-message-list__event")

        result = []

        for item in message_items:
            try:
                sender_name = await item.eval_on_selector(
                    ".msg-s-message-group__name", "node => node.textContent.trim()"
                )
                message_time = await item.eval_on_selector(
                    ".msg-s-message-group__timestamp", "node => node.textContent.trim()"
                )
            except:
                if not sender_name or not message_time:
                    raise Exception()
            message_content = await item.eval_on_selector(
                ".msg-s-event-listitem__body", "node => node.textContent.trim()"
            )

            result.append(
                {"name": sender_name, "time": message_time, "content": message_content}
            )
        url = page.url
        await browser.close()
        return {
            "url": url,
            "messages": result,
        }


import asyncio

asyncio.run(get_dm({"name": "dyllan liu", "key": ""}, headless=False))
