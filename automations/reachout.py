import asyncio
from web_agent import WebAgent
from playwright.async_api import async_playwright
from urllib.parse import quote
import os
from dotenv import load_dotenv
import random
import html
from datetime import date
from utils.google_sheet_utils import add_to_google_sheet
import argparse

load_dotenv()

port = os.getenv("PORT")


async def main():
    async with async_playwright() as p:
        # Initialize the parser
        parser = argparse.ArgumentParser()

        # Add parameters
        parser.add_argument("-k", type=str)
        parser.add_argument("-q", type=str)
        parser.add_argument("-l", type=str)
        parser.add_argument("-t", type=str)
        parser.add_argument("-s", type=str)
        parser.add_argument("-c", type=str)

        # Parse the arguments
        keyword = parser.parse_args().k
        question = parser.parse_args().q
        last_page = int(parser.parse_args().l)
        target_amount_reachout = int(parser.parse_args().t)
        school = parser.parse_args().s
        customized_message = parser.parse_args().c

        print(keyword, question, last_page, target_amount_reachout, customized_message)

        # keyword = "software qa"
        # question = "What are your biggest painpoints"
        # last_page = 0
        # target_amount_reachout = 5
        # customized_message = ""

        sheet_id = "1d1vSneXk6BHMnVRpssHe1Y_H4_pJBVAQUxUyyvZCeMk"

        browser = await p.chromium.launch(headless=False)

        context = await browser.new_context()
        li_at = {
            "name": "li_at",
            "value": "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G",
            "domain": ".www.linkedin.com",
            "path": "/",
            "secure": True,
        }
        page = await context.new_page()
        try:
            # await page.goto(
            #     "http://whatismyipaddress.com/"
            # )  # Navigate to a site to test the proxy
            # await page.screenshot(path="screenshot.jpg")
            # await page.goto("https://www.linkedin.com/")
            # await page.wait_for_timeout(999999999)
            agent = WebAgent(page)

            page_count = last_page

            ###### login logic #######
            await page.goto("https://www.linkedin.com/")
            await context.add_cookies([li_at])
            await page.reload()
            count = 0
            while count < target_amount_reachout:
                await page.goto(
                    f"https://www.linkedin.com/search/results/people/?keywords={quote(keyword)}&page={page_count}",
                    wait_until="domcontentloaded",
                )
                button_selector = 'button.artdeco-pill--choice[aria-label="Show all filters. Clicking this button displays all available filter options."]'
                await page.wait_for_selector(button_selector, state="visible")
                await page.click(button_selector)
                await page.wait_for_timeout(random.randint(1000, 3000))
                button_selector = 'button.reusable-search-filters-advanced-filters__add-filter-button >> text="Add a school"'
                await page.wait_for_selector(button_selector, state="visible")
                await page.click(button_selector)
                await page.wait_for_timeout(random.randint(1000, 3000))
                await page.type(
                    'input[role="combobox"][placeholder="Add a school"]', school
                )
                button_selector = '.basic-typeahead__triggered-content >> [role="option"]:nth-of-type(1)'
                await page.wait_for_selector(button_selector, state="visible")
                first_element = await page.query_selector(button_selector)
                await first_element.click()
                await page.wait_for_timeout(random.randint(1000, 3000))
                button_selector = '[data-test-reusables-filters-modal-show-results-button="true"] >> text="Show results"'
                await page.wait_for_selector(button_selector, state="visible")
                await page.click(button_selector)
                for i in range(10):
                    try:
                        await page.wait_for_timeout(random.randint(1000, 3000))
                        person_selector = f"//li[contains(@class, 'reusable-search__result-container')][{i+1}]"
                        await page.wait_for_selector(person_selector, timeout=5000)
                        await page.click(person_selector, force=True, timeout=5000)
                        await page.wait_for_selector(
                            "div.pv-top-card-v2-ctas", timeout=5000
                        )
                    except Exception as e:
                        print(e)
                        await page.mouse.click(0, 0)
                        continue
                    try:
                        await page.wait_for_timeout(random.randint(1000, 3000))
                        await page.wait_for_selector(
                            "h1.text-heading-xlarge.inline.t-24.v-align-middle.break-words",
                            timeout=5000,
                        )
                        name = await page.text_content(
                            "h1.text-heading-xlarge.inline.t-24.v-align-middle.break-words",
                            timeout=5000,
                        )
                        more_actions_buttons = await page.query_selector_all(
                            f'[aria-label="More actions"]'
                        )
                        for more_action_button in more_actions_buttons:
                            try:
                                await more_action_button.click(timeout=5000)
                            except Exception as e:
                                print(e)
                        connect_buttons = await page.query_selector_all(
                            f'[aria-label="Invite {html.escape(name)} to connect"]'
                        )
                        connect_button_clicked = False
                    except Exception as e:
                        print(e)
                        continue
                    await page.wait_for_timeout(random.randint(1000, 3000))
                    for connect_button in connect_buttons:
                        try:
                            await connect_button.click(timeout=5000)
                            connect_button_clicked = True
                        except Exception as e:
                            print(e)
                    if connect_button_clicked:
                        try:
                            await page.wait_for_timeout(random.randint(1000, 3000))
                            await page.wait_for_selector(
                                '[aria-label="Add a note"]', timeout=5000
                            )
                            await page.click('[aria-label="Add a note"]', timeout=5000)
                            await page.wait_for_timeout(random.randint(1000, 3000))

                            if customized_message:
                                # MANUAL INPUT
                                first_name = name.split(" ")[0]
                                await page.type(
                                    'textarea[name="message"]',
                                    f"Hi {first_name}, saw that we both of us graduated from UC Berkeley recently. "
                                    + customized_message,
                                )
                                message = customized_message
                            else:
                                # AGENT INPUT
                                message = await agent.chat(
                                    f"""In the 'Add a note' text box, within 250 characters, write a quick introduction including the person's name if possible and ask the question: '{question}'. 
                                    Be concise, don't include any placeholder text, this will be the message sent to the recipient. 
                                    Somtimes you might accidentally select the search bar (usually with ID 13), usually the textbox has a smaller ID, such as 5. 
                                    Don't do anything else because it will disrupt the next step. 
                                    If there is text in the textbox already, it means you have already filled in the message, don't try to fill in the message again"""
                                )

                            await page.wait_for_timeout(random.randint(1000, 3000))
                            await page.click(
                                ".artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view.ml1",
                                timeout=5000,
                            )
                            count += 1
                            row_data = [
                                name,
                                message,
                                date.today().__str__(),
                                "pending",
                            ]
                            add_to_google_sheet(row_data, sheet_id)
                            if count >= target_amount_reachout:
                                break
                        except Exception as e:
                            print(e)
                    print("back")
                    await page.go_back(wait_until="domcontentloaded", timeout=5000)
                page_count += 1
        except Exception as e:
            print(e)
        
        await browser.close()


asyncio.run(main())
