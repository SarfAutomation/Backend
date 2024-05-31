# from web_agent import WebAgent
from playwright.async_api import async_playwright
from dotenv import load_dotenv
import capsolver
from urllib.parse import urlparse, parse_qs

load_dotenv()

# Change this information
capsolver.api_key = "CAP-1174C9DB788891631E0A4168C50041D2"


def solve_funcaptcha_linkedin(blob_value):
    solution = capsolver.solve(
        {
            "type": "FunCaptchaTaskProxyLess",
            "websiteURL": "https://iframe.arkoselabs.com",
            "websitePublicKey": "3117BF26-4762-4F5A-8ED9-A85E69209A46",
            "funcaptchaApiJSSubdomain": "https://client-api.arkoselabs.com",
            "data": f'{{"blob":"{blob_value}"}}',
        }
    )
    return solution


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

        try:
            await page.wait_for_timeout(3000)
            await page.wait_for_selector("iframe", timeout=5000)
            iframe = await page.query_selector("iframe")
            iframe = await iframe.content_frame()
            await iframe.wait_for_selector("iframe", timeout=5000)
            iframe = await iframe.query_selector("iframe")
            iframe_src = await iframe.get_attribute("src")
            iframe = await iframe.content_frame()
            await iframe.wait_for_selector("iframe", timeout=5000)
            iframe = await iframe.query_selector("iframe")
            iframe = await iframe.content_frame()
            await iframe.wait_for_selector("iframe", timeout=5000)
            iframe = await iframe.query_selector("iframe")
            iframe = await iframe.content_frame()
            await iframe.wait_for_selector("iframe", timeout=5000)
            iframe = await iframe.query_selector("iframe")
            iframe = await iframe.content_frame()

            await iframe.click("button#home_children_button")
            parsed_url = urlparse(iframe_src)
            query_params = parse_qs(parsed_url.query)
            blob_value = query_params["data"][0]

            retries = 0
            while retries < 3:
                try:
                    solution = solve_funcaptcha_linkedin(blob_value)
                    token = solution["token"]
                    break
                except:
                    retries += 1

            await page.evaluate(
                """(token) => {
                const input = document.querySelector('input[name="captchaUserResponseToken"]');
                input.value = token;
                const form = document.querySelector('form#captcha-challenge');
                form.submit();
            }""",
                token,
            )
        except:
            pass

        await page.wait_for_timeout(3000)

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
