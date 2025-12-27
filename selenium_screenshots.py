#!/usr/bin/env python3
"""
Screenshot capture using Selenium and Chrome
"""
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

def capture_screenshots():
    print("Setting up Chrome...")

    # Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.binary_location = '/root/.cache/ms-playwright/chromium-1194/chrome-linux/chrome'

    # Service
    service = Service('/opt/node22/bin/chromedriver')

    # Create driver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_window_size(1920, 1080)

    try:
        # Create screenshots directory
        os.makedirs('screenshots', exist_ok=True)

        # Navigate to presentation
        print("Loading presentation...")
        driver.get('http://127.0.0.1:8888/')

        # Wait for slides to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'slide-content'))
        )
        time.sleep(2)

        # Screenshot 1: Normal presentation view
        print("📸 Capturing normal presentation view...")
        driver.save_screenshot('screenshots/01_normal_view.png')

        # Screenshot 2: Press 'O' to open grid view
        print("📸 Opening grid overview...")
        body = driver.find_element(By.TAG_NAME, 'body')
        body.send_keys('o')
        time.sleep(1)
        driver.save_screenshot('screenshots/02_grid_overview.png')

        # Screenshot 3: Scroll down grid
        print("📸 Capturing scrolled grid view...")
        driver.execute_script("document.querySelector('.grid-overlay').scrollTop = 300")
        time.sleep(0.5)
        driver.save_screenshot('screenshots/03_grid_scrolled.png')

        # Screenshot 4: Click on slide 3
        print("📸 Clicking on slide 3...")
        driver.execute_script("document.querySelector('.grid-overlay').scrollTop = 0")
        time.sleep(0.5)
        slide_3 = driver.find_element(By.CSS_SELECTOR, '.grid-slide:nth-child(3)')
        slide_3.click()
        time.sleep(1)
        driver.save_screenshot('screenshots/04_after_navigation.png')

        # Screenshot 5: Open grid again to show current slide indicator
        print("📸 Opening grid again to show current slide highlight...")
        body.send_keys('o')
        time.sleep(1)
        driver.save_screenshot('screenshots/05_grid_current_highlight.png')

        # Screenshot 6: Hover effect (simulate with JavaScript)
        print("📸 Simulating hover effect...")
        driver.execute_script("""
            const slide = document.querySelector('.grid-slide:nth-child(5)');
            slide.classList.add('hover');
            slide.style.transform = 'translateY(-5px)';
            slide.style.borderColor = '#4a9eff';
            slide.style.boxShadow = '0 8px 20px rgba(74, 158, 255, 0.3)';
        """)
        time.sleep(0.5)
        driver.save_screenshot('screenshots/06_grid_hover_effect.png')

        print("\n✅ All screenshots captured successfully!")
        print("Screenshots saved in: screenshots/\n")
        print("Files created:")
        print("  ✓ 01_normal_view.png - Normal presentation view")
        print("  ✓ 02_grid_overview.png - Grid view opened")
        print("  ✓ 03_grid_scrolled.png - Scrolled grid")
        print("  ✓ 04_after_navigation.png - After clicking slide 3")
        print("  ✓ 05_grid_current_highlight.png - Current slide highlighted")
        print("  ✓ 06_grid_hover_effect.png - Hover effect demonstration")

    finally:
        driver.quit()
        print("\n✓ Browser closed")

if __name__ == '__main__':
    capture_screenshots()
