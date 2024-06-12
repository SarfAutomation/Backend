# #from web_agent import WebAgent
from playwright.async_api import async_playwright
from utils.page import get_secure_page
from dotenv import load_dotenv
import random

load_dotenv()

async def get_linkedin_profile(params, proxy=None, headless=True):
    async with async_playwright() as p:
        try:
            linkedin_url = params["linkedin_url"]
            key = params["key"]
        except:
            raise Exception("Missing params")

        # linkedin_url = "https://www.linkedin.com/in/jasonciment/"
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

        # #agent = WebAgent(page)
        await context.add_cookies([li_at])
        await page.goto(linkedin_url)
        await page.wait_for_timeout(random.randint(1000, 10000))

        # name
        selector = "h1.text-heading-xlarge.inline.t-24.v-align-middle.break-words"
        await page.wait_for_selector(selector)
        name = await page.inner_text(selector)
        await page.wait_for_timeout(random.randint(1000, 10000))

        try:
            await page.click('button:has-text("Posts")', timeout=5000)
            await page.wait_for_timeout(random.randint(1000, 10000))
            # Select the main container elements by their class
            container_elements = await page.query_selector_all('.profile-creator-shared-feed-update__mini-update.display-flex.flex-column')
            recent_posts = []
            for container in container_elements:
                # Within each container, find all anchor tags and extract their href attributes
                link_elements = await container.query_selector_all('a.app-aware-link')
                link = link_elements[0]
                url = await link.get_attribute('href')
                type = await link.get_attribute("aria-label")
                if url:  # Ensure the link is not None or empty
                    recent_posts.append({"url": url, "type": type})
        except:
            recent_posts = []

        try:
            # mutual
            selector = "a.app-aware-link.inline-flex.align-items-center.link-without-hover-visited.pt2 span[aria-hidden='true'] strong"

            # Find all strong elements that might contain names
            mutuals = await page.query_selector_all(selector)

            # Check if names elements exist and extract the first name
            if mutuals:
                mutual = await mutuals[0].text_content()
            else:
                mutual = None
        except:
            mutual = None

        try:
            # about
            selector = (
                'div[data-generated-suggestion-target*="urn:li:fsu_profileActionDelegate"] '
                '.full-width.t-14.t-normal.t-black.display-flex.align-items-center span[aria-hidden="true"]'
            )
            await page.wait_for_selector(selector, timeout=5000)
            about = await page.inner_text(selector)
        except:
            about = ""

        # experiences
        try:
            try:
                await page.click("#navigation-index-see-all-experiences", timeout=5000)
            except:
                pass

            selector = 'div[data-view-name="profile-component-entity"]'
            await page.wait_for_selector(selector, timeout=5000)
            containers = await page.query_selector_all(selector)
            all_experiences = []

            for container in containers:
                title_element = await container.query_selector(".t-bold")
                title = await title_element.text_content() if title_element else "N/A"

                employment_type_element = await container.query_selector(".t-14.t-normal")
                employment_type = (
                    await employment_type_element.text_content()
                    if employment_type_element
                    else "N/A"
                )

                duration_element = await container.query_selector(
                    ".pvs-entity__caption-wrapper"
                )
                duration = (
                    await duration_element.text_content() if duration_element else "N/A"
                )

                location_element = await container.query_selector(
                    ".t-14.t-normal.t-black--light"
                )
                location = (
                    await location_element.text_content() if location_element else "N/A"
                )

                description_element = await container.query_selector(
                    ".t-14.t-normal.t-black"
                )
                description = (
                    await description_element.text_content()
                    if description_element
                    else "N/A"
                )

                experience = {
                    "title": title.strip(),
                    "employment_type": employment_type.strip(),
                    "duration": duration.strip(),
                    "location": location.strip(),
                    "description": description.strip(),
                }

                all_experiences.append(experience)
        except:
            all_experiences = []

        await page.wait_for_timeout(5000)
        await browser.close()
       
        return {
            "name": name,
            "recent_posts": recent_posts,
            "mutual": mutual,
            "about": about,
            "experiences": all_experiences[:3],
        }

# import asyncio
# print(asyncio.run(
#     get_linkedin_profile(
#         {
#             "linkedin_url": "https://www.linkedin.com/in/jasonciment/",
#             "key": "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G",
#         },
#         headless=False,
#     )
# ))