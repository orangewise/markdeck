#!/usr/bin/env python3
"""
Screenshot capture using existing Chromium installation
"""

import asyncio
import os

from playwright.async_api import async_playwright

# Use existing Chromium installation
CHROMIUM_PATH = "/root/.cache/ms-playwright/chromium-1194/chrome-linux/chrome"


async def capture_screenshots():
    async with async_playwright() as p:
        print("Launching browser with existing Chromium...")

        browser = await p.chromium.launch(
            executable_path=CHROMIUM_PATH,
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"],
        )

        page = await browser.new_page(viewport={"width": 1920, "height": 1080})

        print("Navigating to presentation...")
        await page.goto("http://127.0.0.1:8888/", wait_until="networkidle")

        # Wait for slides to load
        await page.wait_for_selector(".slide-content", timeout=10000)
        await asyncio.sleep(2)

        # Create screenshots directory
        os.makedirs("screenshots", exist_ok=True)

        # Screenshot 1: Normal presentation view
        print("📸 1/6: Capturing normal presentation view...")
        await page.screenshot(path="screenshots/01_normal_view.png")

        # Screenshot 2: Press 'O' to open grid view
        print("📸 2/6: Opening grid overview...")
        await page.keyboard.press("o")
        await asyncio.sleep(1.5)
        await page.screenshot(path="screenshots/02_grid_overview.png")

        # Screenshot 3: Scroll down grid
        print("📸 3/6: Capturing scrolled grid view...")
        await page.evaluate('document.querySelector(".grid-overlay").scrollTop = 400')
        await asyncio.sleep(0.5)
        await page.screenshot(path="screenshots/03_grid_scrolled.png")

        # Screenshot 4: Click on slide 3
        print("📸 4/6: Clicking on slide 3...")
        await page.evaluate('document.querySelector(".grid-overlay").scrollTop = 0')
        await asyncio.sleep(0.5)
        await page.click(".grid-slide:nth-child(3)")
        await asyncio.sleep(1.5)
        await page.screenshot(path="screenshots/04_after_navigation.png")

        # Screenshot 5: Open grid again to show current slide indicator
        print("📸 5/6: Opening grid to show current slide highlight...")
        await page.keyboard.press("o")
        await asyncio.sleep(1.5)
        await page.screenshot(path="screenshots/05_grid_current_highlight.png")

        # Screenshot 6: Hover effect
        print("📸 6/6: Capturing hover effect...")
        await page.evaluate("""
            const slide = document.querySelector('.grid-slide:nth-child(5)');
            if (slide) {
                slide.style.transform = 'translateY(-5px)';
                slide.style.borderColor = '#4a9eff';
                slide.style.boxShadow = '0 8px 20px rgba(74, 158, 255, 0.3)';
            }
        """)
        await asyncio.sleep(0.5)
        await page.screenshot(path="screenshots/06_grid_hover_effect.png")

        await browser.close()

        print("\n" + "=" * 60)
        print("✅ All screenshots captured successfully!")
        print("=" * 60)
        print("\nScreenshots saved in: ./screenshots/\n")

        # List files
        for i in range(1, 7):
            filename = f"screenshots/0{i}_*.png"
            import glob

            files = glob.glob(filename)
            if files:
                size = os.path.getsize(files[0]) / 1024
                print(f"  ✓ {os.path.basename(files[0])}: {size:.1f} KB")


if __name__ == "__main__":
    asyncio.run(capture_screenshots())
