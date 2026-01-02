#!/usr/bin/env python3
"""
Screenshot capture script for MarkDeck themes.
Captures screenshots of both dark and light themes.
"""
import asyncio
import time
from playwright.async_api import async_playwright


async def capture_theme_screenshots():
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1920, 'height': 1080})

        # Navigate to presentation
        await page.goto('http://127.0.0.1:8888/')

        # Wait for slides to load
        await page.wait_for_selector('.slide-content', timeout=10000)
        await asyncio.sleep(2)

        # Screenshot 1: Dark theme (default)
        print("Capturing dark theme screenshot...")
        await page.screenshot(path='screenshots/theme_dark.png')

        # Screenshot 2: Switch to light theme
        print("Switching to light theme...")
        await page.keyboard.press('t')
        await asyncio.sleep(1)
        await page.screenshot(path='screenshots/theme_light.png')

        # Screenshot 3: Dark theme with grid view
        print("Switching back to dark theme...")
        await page.keyboard.press('t')
        await asyncio.sleep(1)
        await page.keyboard.press('o')
        await asyncio.sleep(1)
        await page.screenshot(path='screenshots/theme_dark_grid.png')

        # Screenshot 4: Light theme with grid view
        print("Switching to light theme with grid...")
        await page.keyboard.press('Escape')
        await asyncio.sleep(0.5)
        await page.keyboard.press('t')
        await asyncio.sleep(1)
        await page.keyboard.press('o')
        await asyncio.sleep(1)
        await page.screenshot(path='screenshots/theme_light_grid.png')

        await browser.close()
        print("\n✅ All theme screenshots captured successfully!")
        print("Screenshots saved in: screenshots/")
        print("  - theme_dark.png")
        print("  - theme_light.png")
        print("  - theme_dark_grid.png")
        print("  - theme_light_grid.png")


if __name__ == '__main__':
    import os
    os.makedirs('screenshots', exist_ok=True)
    asyncio.run(capture_theme_screenshots())
