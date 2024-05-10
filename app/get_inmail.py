#from web_agent import WebAgent
from playwright.async_api import async_playwright
from dotenv import load_dotenv
import random

load_dotenv()

async def get_inmail(params, headless=True):
    async with async_playwright() as p:
        try:
            name = params["name"]
            key = params["key"]
        except:
            raise Exception("Missing params")

        key = "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G"

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
        #agent = WebAgent(page)
        await context.add_cookies([li_at])
        await page.goto("https://www.linkedin.com/sales/inbox")

        input_selector = "#left-rail-inbox-search"

        await page.fill(input_selector, name)
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(random.randint(1000, 3000))
        link_selector = (
            "li[data-x-conversation-list-item] a.conversation-list-item__link"
        )
        try:
            await page.wait_for_selector(link_selector, timeout=5000)
        except:
            await browser.close()
            return {"url": "", "messages": []}
        link_element = await page.query_selector(link_selector)
        href = await link_element.get_attribute("href")
        selector = "articl_e.relative.mt4, article.relative.mb4"
        await page.wait_for_selector(selector)
        articles = await page.query_selector_all(
            "article.relative.mt4, article.relative.mb4"
        )
        result = []
        for article in articles:
            try:
                selector = 'span[aria-label="Message from you"]'
                fromYou = await article.query_selector(selector)
                if fromYou:
                    sender_name = "You"
                else:
                    sender_name = await article.eval_on_selector(
                        'span[data-anonymize="person-name"]',
                        "node => node.textContent.trim()",
                    )

                message_time = await article.eval_on_selector(
                    "time", "node => node.textContent.trim()"
                )
            except:
                if not sender_name or not message_time:
                    raise Exception()
            message_content = await article.eval_on_selector(
                'p[data-anonymize="general-blurb"]', "node => node.textContent.trim()"
            )
            result.append(
                {"name": sender_name, "time": message_time, "content": message_content}
            )
        await page.wait_for_timeout(1500)
        await browser.close()
        return {
            "url": "https://www.linkedin.com/" + href,
            "messages": result,
        }
