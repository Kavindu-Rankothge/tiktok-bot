import pandas as pd
from playwright.async_api import async_playwright, Browser

# gets screenshots using url 
async def capture(browser: Browser,  url: str, comments: list):
    # load page
    page = await browser.new_page()
    await page.goto(url)
    # get post screenshot
    post_loc = page.locator("data-testid=post-container")
    await post_loc.first.screenshot(path="post.png")
    # get comment screenshots
    i = 0
    for comment in comments:
        name = comment['name']
        comment_loc = page.locator("id="+name)
        await comment_loc.first.screenshot(path=f"comment{i}.png")
        i += 1

# main method simulates browser
async def get_screenshots(id, url):
    # gets comment list from dataframe for post
    df = pd.read_json('reddit-data.json')
    temp_df = df[df['id'] == id] 
    comments = temp_df.iloc[0]['comments']
    # setups browser
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        await capture(browser, url, comments)
        await browser.close()