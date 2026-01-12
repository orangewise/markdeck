#!/usr/bin/env python3
"""
Screenshot capture script for MarkDeck.
Captures screenshots of grid view feature and theme variations.
Includes visual diff comparison with previous screenshots.

Note: First run the MarkDeck server in another terminal:
    markdeck present examples/features.md --port 8888 --no-browser
"""

import argparse
import asyncio
import shutil
from pathlib import Path

from playwright.async_api import async_playwright

try:
    from image_diff import ImageDiffer

    DIFF_AVAILABLE = True
except ImportError:
    DIFF_AVAILABLE = False
    print("⚠️  image_diff module not available. Install pixelmatch for diff support.")
    print("   uv pip install pixelmatch Pillow --python .venv/bin/python")


async def capture_screenshots():
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})

        # Navigate to presentation
        await page.goto("http://127.0.0.1:8888/")

        # Wait for slides to load
        await page.wait_for_selector(".slide-content", timeout=10000)
        await asyncio.sleep(2)

        # ===== Grid View Screenshots =====
        print("\n=== Capturing Grid View Screenshots ===")

        # Screenshot 1: Normal presentation view
        print("Capturing normal presentation view...")
        await page.screenshot(path="screenshots/01_normal_view.png")

        # Screenshot 2: Press 'O' to open grid view
        print("Opening grid overview...")
        await page.keyboard.press("o")
        await asyncio.sleep(1)
        await page.screenshot(path="screenshots/02_grid_overview.png")

        # Screenshot 3: Scroll down to see more slides in grid
        print("Capturing scrolled grid view...")
        await page.evaluate('document.querySelector(".grid-overlay").scrollTop = 300')
        await asyncio.sleep(0.5)
        await page.screenshot(path="screenshots/03_grid_scrolled.png")

        # Screenshot 4: Click on a slide to navigate
        print("Clicking on slide 3...")
        await page.evaluate('document.querySelector(".grid-overlay").scrollTop = 0')
        await asyncio.sleep(0.5)
        await page.click(".grid-slide:nth-child(3)")
        await asyncio.sleep(1)
        await page.screenshot(path="screenshots/04_after_navigation.png")

        # Screenshot 5: Open grid again to show current slide indicator
        print("Opening grid again to show current slide highlight...")
        await page.keyboard.press("o")
        await asyncio.sleep(1)
        await page.screenshot(path="screenshots/05_grid_current_highlight.png")

        # Close grid view before theme screenshots
        await page.keyboard.press("Escape")
        await asyncio.sleep(0.5)

        # ===== Theme Screenshots =====
        print("\n=== Capturing Theme Screenshots ===")

        # Screenshot 6: Dark theme (default)
        print("Capturing dark theme screenshot...")
        await page.screenshot(path="screenshots/theme_dark.png")

        # Screenshot 7: Switch to light theme
        print("Switching to light theme...")
        await page.keyboard.press("t")
        await asyncio.sleep(1)
        await page.screenshot(path="screenshots/theme_light.png")

        # Screenshot 8: Light theme with grid view
        print("Capturing light theme with grid view...")
        await page.keyboard.press("o")
        await asyncio.sleep(1)
        await page.screenshot(path="screenshots/theme_light_grid.png")

        # Screenshot 9: Dark theme with grid view
        print("Switching back to dark theme with grid...")
        await page.keyboard.press("Escape")
        await asyncio.sleep(0.5)
        # Press 't' twice to cycle: light -> beige -> dark
        await page.keyboard.press("t")
        await asyncio.sleep(0.5)
        await page.keyboard.press("t")
        await asyncio.sleep(1)
        await page.keyboard.press("o")
        await asyncio.sleep(1)
        await page.screenshot(path="screenshots/theme_dark_grid.png")

        # ===== Wide Slide Example Screenshot =====
        print("\n=== Capturing Wide Slide Example Screenshot ===")

        # Navigate back to beginning
        print("Navigating to wide slide example...")
        await page.goto("http://127.0.0.1:8888/")
        await page.wait_for_selector(".slide-content", timeout=10000)
        await asyncio.sleep(1)

        # Navigate to slide 11 (Wide Table Example)
        for i in range(11):
            await page.keyboard.press("ArrowRight")
            await asyncio.sleep(0.2)

        await asyncio.sleep(1)

        # Screenshot 10: Wide slide example
        print("Capturing wide slide example...")
        await page.screenshot(path="screenshots/wide_slide_example.png")

        # ===== Two-Column Layout Screenshots =====
        print("\n=== Capturing Two-Column Layout Screenshots ===")

        # Navigate back to features.md (already on port 8888)
        print("Navigating to two-column example slide...")
        await page.goto("http://127.0.0.1:8888/")
        await page.wait_for_selector(".slide-content", timeout=10000)
        await asyncio.sleep(1)

        # Navigate to slide 26 (Two-Column Example: Code & Explanation)
        for i in range(26):
            await page.keyboard.press("ArrowRight")
            await asyncio.sleep(0.2)

        await asyncio.sleep(1)

        # Screenshot 11: Two-column layout example
        print("Capturing two-column layout (Code & Explanation)...")
        await page.screenshot(path="screenshots/two_column_example.png")

        # ===== Custom Column Width Screenshots =====
        print("\n=== Capturing Custom Column Width Screenshots ===")

        # Navigate to slide 29 (Custom Width Example: 70/30 Split)
        print("Navigating to custom width example (70/30)...")
        await page.goto("http://127.0.0.1:8888/")
        await page.wait_for_selector(".slide-content", timeout=10000)
        await asyncio.sleep(1)

        for i in range(29):
            await page.keyboard.press("ArrowRight")
            await asyncio.sleep(0.2)

        await asyncio.sleep(1)

        # Screenshot 12: Custom column width 70/30
        print("Capturing custom column width (70/30 split)...")
        await page.screenshot(path="screenshots/column_width_70_30.png")

        # Navigate to slide 31 (Custom Width Example: 30/70 Narrow Left)
        print("Navigating to custom width example (30/70)...")
        for i in range(2):
            await page.keyboard.press("ArrowRight")
            await asyncio.sleep(0.2)

        await asyncio.sleep(1)

        # Screenshot 13: Custom column width 30/70
        print("Capturing custom column width (30/70 split)...")
        await page.screenshot(path="screenshots/column_width_30_70.png")

        await browser.close()
        print("\n✅ All screenshots captured successfully!")
        print("\nScreenshots saved in: screenshots/")
        print("\nGrid View Screenshots:")
        print("  - 01_normal_view.png")
        print("  - 02_grid_overview.png")
        print("  - 03_grid_scrolled.png")
        print("  - 04_after_navigation.png")
        print("  - 05_grid_current_highlight.png")
        print("\nTheme Screenshots:")
        print("  - theme_dark.png")
        print("  - theme_light.png")
        print("  - theme_dark_grid.png")
        print("  - theme_light_grid.png")
        print("\nWide Slide Screenshots:")
        print("  - wide_slide_example.png")
        print("\nTwo-Column Layout Screenshots:")
        print("  - two_column_example.png")
        print("\nCustom Column Width Screenshots:")
        print("  - column_width_70_30.png")
        print("  - column_width_30_70.png")


def backup_existing_screenshots(screenshots_dir: Path, backup_dir: Path) -> bool:
    """
    Backup existing screenshots for comparison.

    Args:
        screenshots_dir: Directory containing current screenshots
        backup_dir: Directory to backup screenshots to

    Returns:
        True if backup was created, False if no screenshots exist
    """
    if not screenshots_dir.exists():
        return False

    # Find screenshot files
    screenshot_files = list(screenshots_dir.glob("*.png"))
    if not screenshot_files:
        return False

    # Create backup directory
    backup_dir.mkdir(parents=True, exist_ok=True)

    # Copy screenshots to backup
    for screenshot in screenshot_files:
        shutil.copy2(screenshot, backup_dir / screenshot.name)

    print(f"✅ Backed up {len(screenshot_files)} screenshots to {backup_dir}")
    return True


def compare_screenshots(
    screenshots_dir: Path,
    backup_dir: Path,
    diff_output_dir: Path,
    only_changed: bool = False,
    threshold: float = 5.0,
) -> dict:
    """
    Compare new screenshots with backup and generate visual diffs.

    Args:
        screenshots_dir: Directory with new screenshots
        backup_dir: Directory with backup screenshots
        diff_output_dir: Directory to save diff images
        only_changed: If True, restore unchanged images from backup so only
                     changed images appear in git diffs
        threshold: Minimum percentage difference to consider images changed.
                  Filters out minor rendering noise like anti-aliasing.

    Returns:
        Dictionary with comparison results
    """
    if not DIFF_AVAILABLE:
        print("❌ Diff comparison not available (missing dependencies)")
        return {}

    if not backup_dir.exists():
        print("ℹ️  No backup found - all screenshots are new")
        return {}

    print(f"\n{'=' * 60}")
    print("📊 Comparing screenshots with previous version...")
    print(f"{'=' * 60}\n")

    differ = ImageDiffer(threshold=0.1, include_anti_aliasing=False)

    results = differ.compare_directory(
        backup_dir, screenshots_dir, diff_output_dir, pattern="*.png"
    )

    # Print detailed results
    identical = []
    different = []
    new_files = []

    for filename in sorted(screenshots_dir.glob("*.png")):
        if filename.name not in results:
            new_files.append(filename.name)
            print(f"🆕 {filename.name}: New screenshot")
            continue

        result = results[filename.name]
        diff_pct = result.get("diff_percentage", 0)

        # Treat as identical if below threshold
        is_identical = result["status"] == "identical" or (
            result["status"] == "different" and diff_pct < threshold
        )

        if is_identical:
            identical.append(filename.name)
            if result["status"] == "identical":
                print(f"✅ {filename.name}: Identical (no changes)")
            else:
                print(
                    f"✅ {filename.name}: {diff_pct:.2f}% different (below {threshold}% threshold)"
                )
        elif result["status"] == "different":
            different.append(filename.name)
            diff_pixels = result["diff_pixels"]
            print(f"🔄 {filename.name}: {diff_pct:.2f}% different ({diff_pixels:,} pixels)")
            if result.get("diff_image"):
                print(f"   📸 Diff image: {result['diff_image']}")
        else:
            print(f"❌ {filename.name}: {result.get('error', 'Unknown error')}")

    # Summary
    print(f"\n{'=' * 60}")
    print("Summary:")
    print(f"  ✅ Identical: {len(identical)}")
    print(f"  🔄 Different: {len(different)}")
    print(f"  🆕 New: {len(new_files)}")
    print(f"{'=' * 60}\n")

    # Restore unchanged images if --only-changed is set
    if only_changed and identical:
        print("🔄 Restoring unchanged images from backup...")
        for filename in identical:
            backup_file = backup_dir / filename
            target_file = screenshots_dir / filename
            if backup_file.exists():
                shutil.copy2(backup_file, target_file)
        print(f"   Restored {len(identical)} unchanged image(s)")
        print(f"   Only {len(different) + len(new_files)} file(s) will appear in git diff\n")

    if len(different) > 0 or len(new_files) > 0:
        print("✅ Screenshots have changes - commit recommended")
    else:
        print("ℹ️  No changes detected - commit not necessary")

    return {"identical": identical, "different": different, "new": new_files, "results": results}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Capture MarkDeck screenshots with optional diff comparison.\n\n"
        "Note: First run the MarkDeck server in another terminal:\n"
        "  markdeck present examples/features.md --port 8888 --no-browser",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Capture screenshots only
  python capture_screenshots.py

  # Capture and compare with previous version
  python capture_screenshots.py --compare

  # Capture, compare, and save diff images
  python capture_screenshots.py --compare --save-diffs

  # Only update changed images (useful for clean PRs)
  python capture_screenshots.py --only-changed

  # More strict: only consider >10% difference as changed
  python capture_screenshots.py --only-changed --threshold 10
        """,
    )

    parser.add_argument(
        "--compare",
        action="store_true",
        help="Compare with previous screenshots and show differences",
    )
    parser.add_argument(
        "--save-diffs", action="store_true", help="Save visual diff images (implies --compare)"
    )
    parser.add_argument(
        "--backup-dir",
        type=Path,
        default=Path("screenshots/.backup"),
        help="Directory for screenshot backup (default: screenshots/.backup)",
    )
    parser.add_argument(
        "--diff-dir",
        type=Path,
        default=Path("screenshots/diffs"),
        help="Directory for diff images (default: screenshots/diffs)",
    )
    parser.add_argument(
        "--only-changed",
        action="store_true",
        help="Only keep changed images; restore unchanged from backup (implies --compare)",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.1,
        help="Minimum %% difference to consider images changed (default: 0.1). "
        "Filters out minor rendering noise like anti-aliasing",
    )

    args = parser.parse_args()

    screenshots_dir = Path("screenshots")
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    # Backup existing screenshots if comparison requested
    backed_up = False
    if args.compare or args.save_diffs or args.only_changed:
        backed_up = backup_existing_screenshots(screenshots_dir, args.backup_dir)

    # Capture new screenshots
    print("\n🎬 Capturing screenshots...")
    asyncio.run(capture_screenshots())

    # Compare if requested
    if (args.compare or args.save_diffs or args.only_changed) and backed_up:
        diff_output = args.diff_dir if args.save_diffs else None
        comparison = compare_screenshots(
            screenshots_dir, args.backup_dir, diff_output, args.only_changed, args.threshold
        )

        # Clean up backup
        print("\n🗑️  Cleaning up backup directory...")
        shutil.rmtree(args.backup_dir)
    elif args.compare or args.save_diffs or args.only_changed:
        print("\nℹ️  No previous screenshots to compare - skipping comparison")
