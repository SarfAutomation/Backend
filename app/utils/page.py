from playwright_stealth import stealth_async


async def get_secure_page(browser, user_agent, proxy, saved_context=None):
    context = await browser.new_context(
        user_agent=user_agent,
        storage_state=saved_context,
        proxy=proxy,
        ignore_https_errors=True,
    )
    page = await context.new_page()
    await stealth_async(page)
    return context, page
