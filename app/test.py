from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv()


async def test_ip(username, password, key, headless=True):
    async with async_playwright() as p:

        args = ["--disable-gpu", "--single-process"] if headless else []
        browser = await p.chromium.launch(args=args, headless=headless)

        server = "http://brd.superproxy.io:22225"

        proxy = {
            "server": server,
            "username": username,
            "password": password,
        }
        context = await browser.new_context(
            proxy=proxy,
            ignore_https_errors=True,
        )
        li_at = {
            "name": "li_at",
            "value": key,
            "domain": ".www.linkedin.com",
            "path": "/",
            "secure": True,
        }
        await context.add_cookies([li_at])

        page = await context.new_page()

        await page.goto("http://lumtest.com/myip.json")
        await page.wait_for_timeout(2000)

        await page.goto(
            f"https://www.linkedin.com",
            wait_until="domcontentloaded",
        )
        await page.wait_for_timeout(50000000)
        await browser.close()


import asyncio

## Tim
# print(
#     asyncio.run(
#         test_ip(
#             username="brd-customer-hl_1752fa58-zone-la-ip-91.92.216.78",
#             password="w89q7vd4m95u",
#             key="AQEDAQH9rzUFSmdHAAABkCdqW84AAAGQS3bfzk0AayKUHXTMpBe8mQasWOhyKcyJkptW6eF1f0JIkCVhap8Nht9VLXme3Y1VwwpgoC5BVwSGwP2aqg9BdKlf4PAtTaO7uumiBCM1wUWSEm5TYS5tTG_3",
#             headless=False,
#         )
#     )
# )

# Emily
print(
    asyncio.run(
        test_ip(
            username="brd-customer-hl_1752fa58-zone-richmond",
            password="aa5ut349akbg",
            key="AQEDASgGia8FcXfnAAABj_S8d0QAAAGQGMj7RE0ArUfU0TtCUzwmt7KqbIQJmlqDP5ar31dSfD0cGPVlGAnHMpEPSWpKJTjZca3dnNaTpceYEQFt_6_gZ3RJLly7EZiJz0npu596ZDEwHJU25VsEC_ZU",
            headless=False,
        )
    )
)

# # Elliot
# print(
#     asyncio.run(
#         test_ip(
#             username="brd-customer-hl_1752fa58-zone-la-ip-46.232.208.187",
#             password="w89q7vd4m95u",
#             key="AQEDAQDHycUBlupnAAABkEvbAvIAAAGQb-eG8k0Aq7c5WDBMknHjtaxuiZxjpsw6HfvaDtBaGzNve28Z5BlNDye7lOqZ0C-dKQDYGMTfmLrF3mrBWr3i77WQouMHboRGDeBa0HGk004gNKrvUrcrfCoJ",
#             headless=False,
#         )
#     )
# )