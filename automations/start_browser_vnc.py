import asyncio
from playwright.async_api import Playwright, async_playwright, expect


async def main() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)

        context = await browser.new_context(
            proxy={"server": "http://54.153.52.26:3128"}
        )
        key = "AQEDAUcY98sD5icBAAABjxFCmK0AAAGPNU8crU0APljJ1z6NlzcSRzs1UUwSw3qAAVa8GvE4bv0tWkyGqoM8fGA9Wog9WNdnbwVxIfcwuvXgdcPVUbBpufFI1l6aWcq_Ac58b-CD0HIRh-lT2fL9laOQ"
        li_at = {
            "name": "li_at",
            "value": key,
            "domain": ".www.linkedin.com",
            "path": "/",
            "secure": True,
        }

        await context.add_cookies([li_at])
        page = await context.new_page()

        await page.goto("http://linkedin.com/")

        # await page.screenshot(path="screenshot.jpg")
        # await page.goto("https://www.linkedin.com/")
        await page.wait_for_timeout(999999999)

        # winodw_id = int(run_command('xdotool search --onlyvisible --name "Chromium"'))
        # print(f'x11vnc -id {winodw_id} -rfbport 5902 -viewonly')

        # process = run_command_async(f'x11vnc -id {winodw_id} -rfbport 5902 -viewonly -forever')
        # print(process.pid)

        await page.wait_for_timeout(99999999)


import subprocess


def run_command(command):
    """Run a shell command and return its output"""
    try:
        output = subprocess.check_output(
            command, shell=True, stderr=subprocess.STDOUT, text=True
        )
        return output
    except subprocess.CalledProcessError as e:
        return e.output


def run_command_async(command):
    """Run a shell command and return the process object"""
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        return process
    except Exception as e:
        print("Failed to start process:", e)
        return None


asyncio.run(main())
