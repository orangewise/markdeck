#!/usr/bin/env python3
"""
Screenshot capture script for MarkDeck grid view feature.
"""
import asyncio
import time
from playwright.async_api import async_playwright


async def capture_screenshots():
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1920, 'height': 1080})

        # Navigate to presentation
        await page.goto('http://127.0.0.1:8888/')

        # Wait for slides to load
        await page.wait_for_selector('.slide-content', timeout=10000)
        await asyncio.sleep(2)

        # Screenshot 1: Normal presentation view
        print("Capturing normal presentation view...")
        await page.screenshot(path='screenshots/01_normal_view.png')

        # Screenshot 2: Press 'O' to open grid view
        print("Opening grid overview...")
        await page.keyboard.press('o')
        await asyncio.sleep(1)
        await page.screenshot(path='screenshots/02_grid_overview.png')

        # Screenshot 3: Scroll down to see more slides in grid
        print("Capturing scrolled grid view...")
        await page.evaluate('document.querySelector(".grid-overlay").scrollTop = 300')
        await asyncio.sleep(0.5)
        await page.screenshot(path='screenshots/03_grid_scrolled.png')

        # Screenshot 4: Click on a slide to navigate
        print("Clicking on slide 3...")
        await page.evaluate('document.querySelector(".grid-overlay").scrollTop = 0')
        await asyncio.sleep(0.5)
        await page.click('.grid-slide:nth-child(3)')
        await asyncio.sleep(1)
        await page.screenshot(path='screenshots/04_after_navigation.png')

        # Screenshot 5: Open grid again to show current slide indicator
        print("Opening grid again to show current slide highlight...")
        await page.keyboard.press('o')
        await asyncio.sleep(1)
        await page.screenshot(path='screenshots/05_grid_current_highlight.png')

        await browser.close()
        print("\n✅ All screenshots captured successfully!")
        print("Screenshots saved in: screenshots/")


if __name__ == '__main__':
    import os
    os.makedirs('screenshots', exist_ok=True)
    asyncio.run(capture_screenshots())
