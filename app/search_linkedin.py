#from web_agent import WebAgent
from playwright.async_api import async_playwright
from utils.page import get_secure_page
from urllib.parse import quote
from dotenv import load_dotenv
import random

load_dotenv()

def extract_user_id_from_linkedin_url(url):
    parts = url.rstrip("/").split("/")
    user_id = parts[-1]
    return user_id


async def search_linkedin(params, proxy=None, headless=True):
    async with async_playwright() as p:
        try:
            searchTerm = params["searchTerm"]
            amount = params["amount"]
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
        #agent = WebAgent(page)
        await context.add_cookies([li_at])
        page_count = 1
        result = []
        while len(result) < amount:
            await page.goto(
                f"https://www.linkedin.com/search/results/people/?keywords={quote(searchTerm)}&page={page_count}",
                wait_until="domcontentloaded",
            )
            for i in range(10):
                await page.wait_for_timeout(random.randint(1000, 3000))
                person_selector = f"//li[contains(@class, 'reusable-search__result-container')][{i+1}]"
                await page.wait_for_selector(person_selector, timeout=5000)
                await page.click(person_selector, force=True, timeout=5000)
                await page.wait_for_timeout(random.randint(1000, 3000))
                # result.append(extract_user_id_from_linkedin_url(page.url))
                result.append(page.url)
                await page.go_back()
                if len(result) >= amount:
                    break
            page_count += 1
        await browser.close()
        return result
