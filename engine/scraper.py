import os
import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

class ScraperAgent:
    def __init__(self, screenshot_dir="screenshots"):
        self.screenshot_dir = screenshot_dir
        os.makedirs(self.screenshot_dir, exist_ok=True)

    async def run(self, url: str) -> dict:
        """
        Launches Playwright, navigates to the target URL, extracts the DOM,
        captures a screenshot, and extracts suspicious assets.
        """
        results = {
            "status": "success",
            "url": url,
            "html": "",
            "screenshot_path": "",
            "title": "",
            "scripts": [],
            "forms": [],
            "links": [],
            "error": None
        }

        async with async_playwright() as p:
            try:
                # Use a headless browser with custom user-agent to look like a normal client
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    viewport={"width": 1280, "height": 800},
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                )
                
                page = await context.new_page()
                
                # Navigate to the page with a 15-second timeout
                print(f"[Scraper] Navigating to {url}...")
                response = await page.goto(url, wait_until="load", timeout=15000)
                
                # Wait an extra 2 seconds for dynamic scripts to load
                await page.wait_for_timeout(2000)
                
                results["title"] = await page.title()
                results["html"] = await page.content()
                
                # Save screenshot
                safe_name = "".join([c if c.isalnum() else "_" for c in url])[:50]
                screenshot_filename = f"{safe_name}.png"
                screenshot_path = os.path.join(self.screenshot_dir, screenshot_filename)
                
                await page.screenshot(path=screenshot_path, full_page=True)
                results["screenshot_path"] = screenshot_path
                
                # Parse DOM details using BeautifulSoup for detailed asset listing
                soup = BeautifulSoup(results["html"], "html.parser")
                
                # Extract script tags and sources
                for idx, script in enumerate(soup.find_all("script")):
                    src = script.get("src")
                    content = script.string or ""
                    results["scripts"].append({
                        "id": idx,
                        "src": src,
                        "inline_content": content[:1000] # Limit content size for LLM analysis
                    })
                    
                # Extract forms
                for idx, form in enumerate(soup.find_all("form")):
                    inputs = []
                    for inp in form.find_all("input"):
                        inputs.append({
                            "type": inp.get("type"),
                            "name": inp.get("name"),
                            "placeholder": inp.get("placeholder"),
                            "id": inp.get("id")
                        })
                    results["forms"].append({
                        "id": idx,
                        "action": form.get("action"),
                        "method": form.get("method"),
                        "inputs": inputs
                    })
                    
                # Extract links
                for link in soup.find_all("a", href=True):
                    href = link.get("href")
                    text = link.get_text(strip=True)
                    if href and not href.startswith(('#', 'javascript:')):
                        results["links"].append({
                            "href": href,
                            "text": text
                        })

                await browser.close()
                print(f"[Scraper] Successfully scanned {url}")
                
            except Exception as e:
                print(f"[Scraper] Error scanning {url}: {str(e)}")
                results["status"] = "error"
                results["error"] = str(e)
                
        return results
