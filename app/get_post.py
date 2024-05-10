# from web_agent import WebAgent
from playwright.async_api import async_playwright
import random
from dotenv import load_dotenv

load_dotenv()


async def get_post(params, headless=True):
    async with async_playwright() as p:
        try:
            post_url = params["post_url"]
            key = params["key"]
        except:
            raise Exception("Missing params")

        key = "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G"

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
        # agent = WebAgent(page)
        await context.add_cookies([li_at])
        await page.goto(
            post_url,
            wait_until="domcontentloaded",
        )
        selector = ".feed-shared-update-v2__description-wrapper.mr2"
        await page.wait_for_selector(selector)
        element = await page.query_selector(selector)
        post_description = await element.text_content()
        detail_elements = await page.query_selector("div.update-components-actor")
        name_element = await detail_elements.query_selector(
            ".update-components-actor__name"
        )
        post_user = (
            await name_element.text_content() if name_element else "Name not found"
        )
        time_element = await detail_elements.query_selector(
            ".update-components-actor__sub-description"
        )
        post_time = (
            await time_element.text_content() if time_element else "Time not available"
        )

        comment_containers = await page.query_selector_all(
            "article.comments-comment-item"
        )
        comments = []
        for comment_container in comment_containers:
            name_element = await comment_container.query_selector(
                ".comments-post-meta__name-text"
            )
            name = (
                await name_element.text_content() if name_element else "Name not found"
            )

            # Extract the comment's posting time
            # Adjust the selector based on your HTML structure
            time_element = await comment_container.query_selector(
                ".comments-comment-item__timestamp"
            )
            time = (
                await time_element.text_content()
                if time_element
                else "Time not available"
            )

            # Extract the comment text
            # Adjust the selector based on your HTML structure
            text_element = await comment_container.query_selector(
                "div.update-components-text"
            )
            content = (
                await text_element.text_content()
                if text_element
                else "Comment not available"
            )

            comments.append({"name": name, "time": time, "content": content})
        
        await page.wait_for_timeout(10000)
        await browser.close()
        
        return {
            "post_user": post_user,
            "post_time": post_time,
            "post_description": post_description,
            "comments": comments,
        }


# import asyncio

# asyncio.run(
#     get_post(
#         {
#             "post_url": "https://www.linkedin.com/posts/y-combinator_why-yc-activity-7049158009503051776-N8FG/",
#             "key": "",
#         },
#         headless=False,
#     )
# )
