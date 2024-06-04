#from web_agent import WebAgent
from playwright.async_api import async_playwright
from utils.page import get_secure_page
from dotenv import load_dotenv
import random

load_dotenv()

def extract_user_id_from_linkedin_url(url):
    parts = url.rstrip("/").split("/")
    user_id = parts[-1]
    return user_id


async def check_scroll_end_within_element(page, selector):
    is_at_bottom = await page.evaluate(
        f"""(selector) => {{
        const element = document.querySelector(selector);
        return Math.abs(element.scrollTop + element.clientHeight - element.scrollHeight) <= 10;
    }}""",
        selector,
    )
    return is_at_bottom


async def scroll_within_element_and_check(page, selector):
    reached_bottom = False
    while not reached_bottom:
        await page.evaluate(
            f"""(selector) => {{
            const element = document.querySelector(selector);
            element.scrollTop += 500;
        }}""",
            selector,
        )
        await page.wait_for_timeout(500)
        reached_bottom = await check_scroll_end_within_element(page, selector)
        if reached_bottom:
            return


async def search_sales_nav(params, proxy=None, headless=True):
    async with async_playwright() as p:
        try:
            search_url = params["search_url"] 
            key = params["key"]
        except:
            raise Exception("Missing params")

        # search_url = "https://www.linkedin.com/sales/search/people?recentSearchId=3638734740&sessionId=8nfRO4D1Q9C5yn5bwKzSLw%3D%3D&viewAllFilters=true"
        amount = 15
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
        #agent = WebAgent(page)
        await context.add_cookies([li_at])
        page_count = 1
        result = []
        open_count = 0
        close_count = 0
        while open_count < amount:
            await page.goto(
                f"{search_url}&page={page_count}",
                wait_until="domcontentloaded",
            )
            selector = "div.artdeco-entity-lockup__content"
            await page.wait_for_selector(selector)
            scrollable_element_selector = "#search-results-container"
            await scroll_within_element_and_check(page, scrollable_element_selector)
            list_items = await page.query_selector_all(selector)
            for item in list_items:
                if open_count >= amount:
                    break
                premium_icon = await item.query_selector(
                    'li-icon[type="linkedin-premium-gold-icon"]'
                )
                if not premium_icon and close_count > amount:
                    continue
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
                        await page.wait_for_selector(
                            profile_link_selector, timeout=1000
                        )
                        dropdown_hidden = False
                    except Exception as e:
                        pass
                    tries += 1
                if dropdown_hidden:
                    continue
                href = await page.get_attribute(profile_link_selector, "href")
                result.append(
                    {
                        "name": name,
                        "url": "https://www.linkedin.com" + href,
                        "isOpen": premium_icon is not None,
                    }
                )
                if premium_icon:
                    open_count += 1
                else:
                    close_count += 1
            page_count += 1
        await browser.close()
        return result
