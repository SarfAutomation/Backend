# from web_agent import WebAgent
from playwright.async_api import async_playwright
from utils.page import get_secure_page
from dotenv import load_dotenv
import random
from urllib.parse import quote

load_dotenv()


async def get_sales_nav_url(params, proxy=None, headless=True):
    async with async_playwright() as p:
        try:
            linkedin_url = params["linkedin_url"]
            key = params["key"]
            list = params["list"]
        except:
            raise Exception("Missing params")

        # linkedin_url = "https://www.linkedin.com/in/%F0%9F%87%AE%F0%9F%87%B3-vikas-singh-08627326/"
        # key = "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G"

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
        await page.goto(linkedin_url)
        await page.wait_for_selector(
            "h1.text-heading-xlarge.inline.t-24.v-align-middle.break-words"
        )
        name = await page.text_content(
            "h1.text-heading-xlarge.inline.t-24.v-align-middle.break-words"
        )
        link_selector = 'a:has-text("Message in Sales Navigator")'
        try:
            href = await page.get_attribute(link_selector, "href", timeout=5000)
            href = href.split("&")[0]
            await page.goto(href)
        except:
            await page.goto(
                f"https://www.linkedin.com/sales/search/people?query=(spellCorrectionEnabled%3Atrue%2Ckeywords%3A{quote(quote(name))})"
            )
            selector = "div.artdeco-entity-lockup__content"
            await page.wait_for_selector(selector)
            list_items = await page.query_selector_all(selector)
            item = list_items[0]
            name_element = await item.query_selector(
                'span[data-anonymize="person-name"]'
            )
            name = await name_element.text_content()
            name = name.strip()
            await page.wait_for_timeout(random.randint(1000, 10000))
            profile_link_selector = 'a.inverse-link-on-a-light-background-without-visited-and-hover:has-text("View profile")'
            dropdown_hidden = True
            tries = 0
            while dropdown_hidden and tries < 10:
                try:
                    selector = f'button[aria-label="See more actions for {name}"]'
                    await page.wait_for_selector(selector)
                    button = await page.query_selector(selector)
                    await button.click(timeout=1000)
                    await page.wait_for_selector(profile_link_selector, timeout=1000)
                    dropdown_hidden = False
                except Exception as e:
                    pass
                tries += 1
            if dropdown_hidden:
                await browser.close()
                return {"name": "", "url": ""}
            await page.click(profile_link_selector)
        await page.wait_for_timeout(random.randint(1000, 10000))
        if list:
            try:
                selector = 'li[data-x--lead-lists--custom-list-item]'
                elements = await page.query_selector_all(selector)
                for element in elements:
                    text_content = await element.text_content()
                    if list in text_content:
                        await browser.close()
                        return {"name": name, "url": page.url}
            except:
                pass
        await browser.close()
        return {"name": "", "url": ""}



