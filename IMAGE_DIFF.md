# Image Diff Tool for MarkDeck

Visual image comparison tool for detecting and visualizing screenshot changes.

## Overview

MarkDeck now includes a visual diff tool that compares screenshots pixel-by-pixel and generates visual diff images highlighting what changed. This helps determine if screenshots need to be committed by showing exactly what changed.

## Features

- **Visual Diff Generation**: Creates images with changed pixels highlighted in pink/magenta
- **Standalone Tool**: Can be used independently to compare any images
- **Integrated with Screenshot Capture**: Automatically compares new screenshots with previous versions
- **Configurable Threshold**: Adjust sensitivity to ignore minor rendering differences
- **Anti-aliasing Detection**: Optional detection of anti-aliasing differences
- **Directory Comparison**: Compare all images in two directories at once
- **Exit Codes**: Returns meaningful exit codes for automation

## Installation

The image diff dependencies are included in the `screenshots` extra:

```bash
# Install screenshot dependencies (includes pixelmatch and Pillow)
uv pip install -e ".[screenshots]" --python .venv/bin/python
```

## Standalone Usage

### Compare Two Images

```bash
# Basic comparison
.venv/bin/python image_diff.py old.png new.png

# Save visual diff image
.venv/bin/python image_diff.py old.png new.png --output diff.png

# More sensitive comparison
.venv/bin/python image_diff.py old.png new.png --threshold 0.05

# Ignore anti-aliasing differences
.venv/bin/python image_diff.py old.png new.png --no-aa
```

### Compare Directories

```bash
# Compare all PNG files in two directories
.venv/bin/python image_diff.py screenshots/old/ screenshots/new/ --dir-mode

# Compare and save diff images
.venv/bin/python image_diff.py screenshots/old/ screenshots/new/ \
  --dir-mode \
  --output-dir diffs/

# Compare only specific files
.venv/bin/python image_diff.py screenshots/old/ screenshots/new/ \
  --dir-mode \
  --pattern "theme_*.png"
```

### Exit Codes

The tool returns meaningful exit codes for automation:

- `0` - Images are identical
- `1` - Images are different
- `2` - Error (file not found, dimension mismatch, etc.)

This allows you to use it in scripts:

```bash
if .venv/bin/python image_diff.py old.png new.png; then
  echo "No changes detected"
else
  echo "Changes detected - commit needed"
fi
```

## Integrated Screenshot Comparison

The screenshot capture script now supports automatic comparison with previous screenshots:

### Capture Only (Default)

```bash
# Just capture screenshots (no comparison)
.venv/bin/python capture_screenshots.py
```

### Capture and Compare

```bash
# Capture and compare with previous version
.venv/bin/python capture_screenshots.py --compare
```

**Output:**
```
🎬 Capturing screenshots...
✅ All screenshots captured successfully!

============================================================
📊 Comparing screenshots with previous version...
============================================================

✅ 01_normal_view.png: Identical (no changes)
🔄 02_grid_overview.png: 2.15% different (4,462 pixels)
✅ 03_grid_scrolled.png: Identical (no changes)
...

============================================================
Summary:
  ✅ Identical: 7
  🔄 Different: 2
  🆕 New: 0
============================================================

✅ Screenshots have changes - commit recommended
```

### Capture, Compare, and Save Diffs

```bash
# Save visual diff images for review
.venv/bin/python capture_screenshots.py --save-diffs
```

This will:
1. Backup existing screenshots to `screenshots/.backup/`
2. Capture new screenshots
3. Compare new with backup
4. Save diff images to `screenshots/diffs/`
5. Clean up backup directory

**Note:** The `.backup/` and `diffs/` directories are in `.gitignore` and won't be committed.

### Custom Threshold

```bash
# More sensitive comparison (smaller threshold)
.venv/bin/python capture_screenshots.py --compare --threshold 0.05

# Less sensitive (larger threshold)
.venv/bin/python capture_screenshots.py --compare --threshold 0.2
```

## How It Works

### Pixelmatch Algorithm

The tool uses the [pixelmatch](https://github.com/mapbox/pixelmatch) algorithm, which:

1. Compares images pixel-by-pixel
2. Accounts for anti-aliasing differences
3. Highlights changed pixels in a diff image
4. Returns the number of different pixels

### Threshold

The threshold parameter (0-1) controls matching sensitivity:

- **0.0** - Exact match required (very sensitive)
- **0.1** - Default, ignores minor rendering differences
- **0.3** - More tolerant, good for ignoring subtle changes
- **1.0** - Very tolerant (not recommended)

**Recommended values:**
- Screenshots: `0.1` (default)
- Pixel-perfect comparison: `0.05`
- Ignore minor changes: `0.2-0.3`

### Visual Diff Output

Changed pixels are highlighted in **pink/magenta** (#FF0080) by default. The diff image shows:

- **Black** - Identical pixels
- **Pink** - Changed pixels
- **Original colors** - Context around changes

## Programmatic Usage

You can also use the tool programmatically in Python:

```python
from image_diff import ImageDiffer

# Create differ instance
differ = ImageDiffer(threshold=0.1, include_anti_aliasing=False)

# Compare two images
mismatch, total, percentage, match = differ.compare(
    "old.png",
    "new.png",
    diff_output_path="diff.png"
)

if match:
    print("Images are identical!")
else:
    print(f"{percentage:.2f}% different ({mismatch:,} pixels)")

# Compare directories
results = differ.compare_directory(
    "screenshots/old/",
    "screenshots/new/",
    diff_output_dir="diffs/",
    pattern="*.png"
)

for filename, result in results.items():
    if result["status"] == "different":
        print(f"{filename}: {result['diff_percentage']:.2f}% different")
```

## GitHub Actions Integration

The screenshot workflow can be updated to only commit screenshots when they've changed:

```yaml
- name: Capture screenshots with diff
  run: |
    .venv/bin/python capture_screenshots.py --compare

- name: Check for changes
  id: check_changes
  run: |
    if git diff --quiet screenshots/; then
      echo "changed=false" >> $GITHUB_OUTPUT
    else
      echo "changed=true" >> $GITHUB_OUTPUT
    fi

- name: Commit screenshots
  if: steps.check_changes.outputs.changed == 'true'
  run: |
    git add screenshots/
    git commit -m "Update screenshots [skip ci]"
    git push
```

## Use Cases

### 1. Prevent Unnecessary Commits

```bash
# Compare first to see if commit is needed
.venv/bin/python capture_screenshots.py --compare

# Only commit if changes detected
if git diff --quiet screenshots/; then
  echo "No changes - skipping commit"
else
  git add screenshots/
  git commit -m "Update screenshots"
fi
```

### 2. Review Visual Changes

```bash
# Generate diff images for review
.venv/bin/python capture_screenshots.py --save-diffs

# Review diffs before committing
ls -la screenshots/diffs/
```

### 3. CI/CD Integration

```bash
# Capture and compare in CI
.venv/bin/python capture_screenshots.py --compare

# Exit code 1 if differences found (can fail CI if desired)
```

### 4. Manual Image Comparison

```bash
# Compare any two images
.venv/bin/python image_diff.py \
  designs/mockup.png \
  screenshots/actual.png \
  --output review/diff.png
```

## Troubleshooting

### "pixelmatch module not available"

Install the screenshot dependencies:

```bash
uv pip install pixelmatch Pillow --python .venv/bin/python
```

### "Image dimensions don't match"

The images must have the same dimensions. Ensure both images are from the same viewport size.

### "Too many false positives"

Increase the threshold to be less sensitive:

```bash
.venv/bin/python image_diff.py old.png new.png --threshold 0.2
```

Or ignore anti-aliasing:

```bash
.venv/bin/python image_diff.py old.png new.png --no-aa
```

### "Not detecting changes"

Decrease the threshold to be more sensitive:

```bash
.venv/bin/python image_diff.py old.png new.png --threshold 0.05
```

## Technical Details

**Dependencies:**
- `pixelmatch>=0.3.0` - Image comparison algorithm
- `Pillow>=10.0.0` - Image processing

**Supported Formats:**
- PNG (recommended)
- JPEG
- BMP
- GIF
- Any format supported by Pillow

**Performance:**
- Fast for typical screenshot sizes (1920x1080)
- ~100-500ms per comparison depending on image size
- Directory mode processes images sequentially

**Memory Usage:**
- Loads both images into memory
- Creates third image for diff
- ~3x image size in memory

## Examples

### Example 1: Detect Theme Changes

```bash
.venv/bin/python image_diff.py \
  screenshots/theme_dark.png \
  screenshots/theme_light.png \
  --output theme_diff.png
```

Output:
```
📊 Comparing images:
  Image 1: screenshots/theme_dark.png
  Image 2: screenshots/theme_light.png
  Threshold: 0.1

🔄 Images are different!
  Different pixels: 2,073,393 / 2,073,600
  Difference: 99.99%

💾 Diff image saved: theme_diff.png
```

### Example 2: Verify Identical Renders

```bash
.venv/bin/python image_diff.py \
  screenshots/render1.png \
  screenshots/render2.png
```

Output:
```
📊 Comparing images:
  Image 1: screenshots/render1.png
  Image 2: screenshots/render2.png
  Threshold: 0.1

✅ Images are identical!
```

### Example 3: Directory Comparison

```bash
.venv/bin/python image_diff.py \
  screenshots/v1/ \
  screenshots/v2/ \
  --dir-mode \
  --output-dir review/diffs/
```

Output:
```
📊 Comparing directories: screenshots/v1/ vs screenshots/v2/
Pattern: *.png
Threshold: 0.1

✅ 01_normal_view.png: Identical
🔄 02_grid_overview.png: 1.23% different (2,552 pixels)
   Diff saved: review/diffs/diff_02_grid_overview.png
✅ 03_grid_scrolled.png: Identical
...

============================================================
Summary:
  Identical: 7
  Different: 2
  Errors: 0
============================================================
```

## Best Practices

1. **Use in CI/CD**: Automatically compare screenshots before committing
2. **Review Diffs**: Always review visual diffs for unexpected changes
3. **Set Appropriate Threshold**: Balance sensitivity vs. false positives
4. **Ignore Anti-aliasing**: Use `--no-aa` for cross-browser comparisons
5. **Version Control Diffs**: Consider committing important diff images for historical review
6. **Document Changes**: Reference diff images in commit messages or PRs

## Future Enhancements

- [ ] Support for different diff colors
- [ ] HTML report generation with side-by-side comparison
- [ ] Animated GIF output showing before/after
- [ ] Perceptual diff mode (SSIM algorithm)
- [ ] Parallel directory processing
- [ ] Integration with GitHub Actions as a dedicated action

---

**Last Updated:** 2026-01-02
**Version:** 1.0
