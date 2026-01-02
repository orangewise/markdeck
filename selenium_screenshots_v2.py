#!/usr/bin/env python3
"""
Screenshot capture using Selenium with webdriver-manager
"""

import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType


def capture_screenshots():
    print("Setting up Chrome with webdriver-manager...")

    # Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.binary_location = "/root/.cache/ms-playwright/chromium-1194/chrome-linux/chrome"

    try:
        # Try to use webdriver-manager to get compatible driver
        print("Downloading compatible ChromeDriver...")
        service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    except Exception as e:
        print(f"webdriver-manager failed: {e}")
        print("Falling back to system chromedriver...")
        service = Service("/opt/node22/bin/chromedriver")

    # Create driver
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_window_size(1920, 1080)
    except Exception as e:
        print(f"Failed to create Chrome driver: {e}")
        print("\nTrying with version check disabled...")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Create screenshots directory
        os.makedirs("screenshots", exist_ok=True)

        # Navigate to presentation
        print("Loading presentation...")
        driver.get("http://127.0.0.1:8888/")

        # Wait for slides to load
        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.CLASS_NAME, "slide-content"))
        )
        time.sleep(2)

        # Screenshot 1: Normal presentation view
        print("📸 1/6: Capturing normal presentation view...")
        driver.save_screenshot("screenshots/01_normal_view.png")

        # Screenshot 2: Press 'O' to open grid view
        print("📸 2/6: Opening grid overview...")
        body = driver.find_element(By.TAG_NAME, "body")
        body.send_keys("o")
        time.sleep(1.5)
        driver.save_screenshot("screenshots/02_grid_overview.png")

        # Screenshot 3: Scroll down grid
        print("📸 3/6: Capturing scrolled grid view...")
        driver.execute_script("document.querySelector('.grid-overlay').scrollTop = 400")
        time.sleep(0.5)
        driver.save_screenshot("screenshots/03_grid_scrolled.png")

        # Screenshot 4: Click on slide 3
        print("📸 4/6: Clicking on slide 3...")
        driver.execute_script("document.querySelector('.grid-overlay').scrollTop = 0")
        time.sleep(0.5)
        slide_3 = driver.find_element(By.CSS_SELECTOR, ".grid-slide:nth-child(3)")
        slide_3.click()
        time.sleep(1.5)
        driver.save_screenshot("screenshots/04_after_navigation.png")

        # Screenshot 5: Open grid again to show current slide indicator
        print("📸 5/6: Opening grid to show current slide highlight...")
        body.send_keys("o")
        time.sleep(1.5)
        driver.save_screenshot("screenshots/05_grid_current_highlight.png")

        # Screenshot 6: Hover effect (simulate with JavaScript)
        print("📸 6/6: Capturing hover effect...")
        driver.execute_script("""
            const slide = document.querySelector('.grid-slide:nth-child(5)');
            if (slide) {
                slide.style.transform = 'translateY(-5px)';
                slide.style.borderColor = '#4a9eff';
                slide.style.boxShadow = '0 8px 20px rgba(74, 158, 255, 0.3)';
            }
        """)
        time.sleep(0.5)
        driver.save_screenshot("screenshots/06_grid_hover_effect.png")

        print("\n" + "=" * 60)
        print("✅ All screenshots captured successfully!")
        print("=" * 60)
        print("\nScreenshots saved in: ./screenshots/\n")
        print("Files created:")
        print("  ✓ 01_normal_view.png - Normal presentation view")
        print("  ✓ 02_grid_overview.png - Grid view opened with all slides")
        print("  ✓ 03_grid_scrolled.png - Scrolled grid showing more slides")
        print("  ✓ 04_after_navigation.png - After clicking slide 3")
        print("  ✓ 05_grid_current_highlight.png - Current slide (3) highlighted")
        print("  ✓ 06_grid_hover_effect.png - Hover effect demonstration")
        print()

        # Show file sizes
        print("File sizes:")
        for i in range(1, 7):
            filename = f"screenshots/0{i}_*.png"
            try:
                import glob

                files = glob.glob(filename)
                if files:
                    size = os.path.getsize(files[0])
                    print(f"  {os.path.basename(files[0])}: {size / 1024:.1f} KB")
            except Exception:
                pass

    except Exception as e:
        print(f"\n❌ Error during screenshot capture: {e}")
        import traceback

        traceback.print_exc()

    finally:
        driver.quit()
        print("\n✓ Browser closed")


if __name__ == "__main__":
    capture_screenshots()
