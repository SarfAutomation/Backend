# from web_agent import WebAgent
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv()


async def login(params, headless=True):
    async with async_playwright() as p:
        try:
            email = params["email"]
            password = params["password"]
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

        context = await browser.new_context(
            proxy=proxy,
            ignore_https_errors=True,
        )

        page = await context.new_page()
        # await page.goto("http://lumtest.com/myip.json")
        # await page.wait_for_timeout(1000000)
        # agent = WebAgent(page)
        await page.goto(
            f"https://www.linkedin.com",
            wait_until="domcontentloaded",
        )
        await page.get_by_role("link", name="Sign in").first.click()
        await page.wait_for_timeout(1000)
        await page.get_by_label("Email or Phone").click()
        await page.wait_for_timeout(1000)
        await page.get_by_label("Email or Phone").type(email)
        await page.wait_for_timeout(1000)
        await page.get_by_label("Password").click()
        await page.wait_for_timeout(1000)
        await page.get_by_label("Password").type(password)
        await page.wait_for_timeout(1000)
        await page.get_by_label("Sign in", exact=True).click()
        await page.wait_for_load_state("domcontentloaded")
        verification_required = await page.query_selector(
            "#input__email_verification_pin"
        )
        await page.wait_for_timeout(3000)
        saved_context = await context.storage_state()
        if verification_required:
            await browser.close()
            return {
                "isLoggedIn": False,
                "cookie": "",
                "url": page.url,
                "savedContext": saved_context,
                "error": "",
            }
        cookies = await context.cookies()
        li_at = ""
        for cookie in cookies:
            if cookie["domain"] == ".www.linkedin.com" and cookie["name"] == "li_at":
                li_at = cookie
        await browser.close()
        if not li_at:
            return {
                "isLoggedIn": False,
                "cookie": "",
                "url": page.url,
                "savedContext": saved_context,
                "error": "Login failed. Please check your credentials.",
            }
        else:
            return {
                "isLoggedIn": True,
                "cookie": li_at,
                "url": page.url,
                "savedContext": saved_context,
                "error": "",
            }


# import asyncio

# print(
#     asyncio.run(
#         login(
#             {"email": "zhanhugo0802@gmail.com", "password": "gogo2001"}, headless=False
#         )
#     )
# )
# print(
#     asyncio.run(
#         login(
#             {"email": "xiaokangzhan6@gmail.com", "password": "kangkang2001"}, headless=False
#         )
#     )
# )
