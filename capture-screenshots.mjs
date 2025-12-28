import puppeteer from 'puppeteer';
import { mkdir } from 'fs/promises';

async function captureScreenshots() {
    console.log('Starting browser...');

    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080 });

    console.log('Navigating to presentation...');
    await page.goto('http://127.0.0.1:8888/', { waitUntil: 'networkidle0' });

    // Wait for slides to load
    await page.waitForSelector('.slide-content', { timeout: 10000 });
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Create screenshots directory
    await mkdir('screenshots', { recursive: true });

    // Screenshot 1: Normal presentation view
    console.log('📸 Capturing normal presentation view...');
    await page.screenshot({
        path: 'screenshots/01_normal_view.png',
        fullPage: false
    });

    // Screenshot 2: Press 'O' to open grid view
    console.log('📸 Opening grid overview...');
    await page.keyboard.press('o');
    await new Promise(resolve => setTimeout(resolve, 1000));
    await page.screenshot({
        path: 'screenshots/02_grid_overview.png',
        fullPage: false
    });

    // Screenshot 3: Scroll down to see more slides in grid
    console.log('📸 Capturing scrolled grid view...');
    await page.evaluate(() => {
        document.querySelector('.grid-overlay').scrollTop = 300;
    });
    await new Promise(resolve => setTimeout(resolve, 500));
    await page.screenshot({
        path: 'screenshots/03_grid_scrolled.png',
        fullPage: false
    });

    // Screenshot 4: Click on slide 3
    console.log('📸 Clicking on slide 3...');
    await page.evaluate(() => {
        document.querySelector('.grid-overlay').scrollTop = 0;
    });
    await new Promise(resolve => setTimeout(resolve, 500));
    await page.click('.grid-slide:nth-child(3)');
    await new Promise(resolve => setTimeout(resolve, 1000));
    await page.screenshot({
        path: 'screenshots/04_after_navigation.png',
        fullPage: false
    });

    // Screenshot 5: Open grid again to show current slide indicator
    console.log('📸 Opening grid again to show current slide highlight...');
    await page.keyboard.press('o');
    await new Promise(resolve => setTimeout(resolve, 1000));
    await page.screenshot({
        path: 'screenshots/05_grid_current_highlight.png',
        fullPage: false
    });

    // Screenshot 6: Hover effect demonstration
    console.log('📸 Capturing hover effect...');
    await page.hover('.grid-slide:nth-child(5)');
    await new Promise(resolve => setTimeout(resolve, 500));
    await page.screenshot({
        path: 'screenshots/06_grid_hover_effect.png',
        fullPage: false
    });

    await browser.close();

    console.log('\n✅ All screenshots captured successfully!');
    console.log('Screenshots saved in: screenshots/\n');
    console.log('Files created:');
    console.log('  - 01_normal_view.png (Normal presentation)');
    console.log('  - 02_grid_overview.png (Grid view opened)');
    console.log('  - 03_grid_scrolled.png (Scrolled grid)');
    console.log('  - 04_after_navigation.png (After clicking slide 3)');
    console.log('  - 05_grid_current_highlight.png (Current slide highlighted)');
    console.log('  - 06_grid_hover_effect.png (Hover effect on slide)');
}

captureScreenshots().catch(console.error);
