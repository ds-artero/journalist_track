from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from typing import List
from app.models.result_model import SearchResult

async def scrape_site(url: str, query: str) -> List[SearchResult]:
    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto(url, timeout=60000)

        # Try to find a search input (English or Spanish)
        search_selectors = [
            "input[name='q']",
            "input[name='s']",
            "input[name='buscador']",
            "input[placeholder*='Buscar']",
            "input[placeholder*='buscar']",
        ]

        search_box = None
        for selector in search_selectors:
            try:
                search_box = await page.query_selector(selector)
                if search_box:
                    break
            except:
                continue

        if not search_box:
            await browser.close()
            return []

        # Type query and submit
        await search_box.fill(query)
        await search_box.press("Enter")

        # Wait for page to load
        await page.wait_for_timeout(3000)

        html = await page.content()
        soup = BeautifulSoup(html, "html.parser")

        # Extract potential results
        for a in soup.find_all("a", href=True):
            text = a.get_text(strip=True)
            href = a["href"]
            if len(text) > 5 and query.lower() in text.lower():
                results.append(SearchResult(title=text, url=href, date=None))

        await browser.close()

    return results

