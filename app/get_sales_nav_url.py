#from web_agent import WebAgent
from playwright.async_api import async_playwright
from dotenv import load_dotenv
import random
from urllib.parse import quote

load_dotenv()

async def get_sales_nav_url(params, headless=True):
    async with async_playwright() as p:
        try:
            linkedin_url = params["linkedin_url"]
            key = params["key"]
        except:
            raise Exception("Missing params")

        # linkedin_url = "https://www.linkedin.com/in/%F0%9F%87%AE%F0%9F%87%B3-vikas-singh-08627326/"
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
        #agent = WebAgent(page)
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
            await page.wait_for_timeout(random.randint(1000, 3000))
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
        await page.wait_for_timeout(random.randint(1000, 3000))
        button_selector = 'button[aria-label="Add note"]'
        await page.wait_for_selector(button_selector)
        await page.click(button_selector)
        await page.wait_for_timeout(random.randint(1000, 3000))
        try:
            note_selector = (
                ".sharing-entity-notes-vertical-list-widget-card .p2.break-words"
            )
            await page.wait_for_selector(note_selector, timeout=5000)
            contains_new_connection = await page.evaluate(
                """() => {
                const elements = document.querySelectorAll('.sharing-entity-notes-vertical-list-widget-card .p2.break-words');
                return Array.from(elements).some(el => el.textContent.includes("New Connection"));
            }"""
            )
            if contains_new_connection:
                await browser.close()
                return {"name": name, "url": page.url}
        except:
            pass
        await browser.close()
        return {"name": "", "url": ""}
