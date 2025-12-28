# Claude Development Notes

This document contains important learnings and tips for Claude Code sessions working on the MarkDeck project.

## Environment Setup

### Virtual Environment

This project uses a Python virtual environment located at `.venv/`. The venv was created using **uv**, a fast Python package manager.

**Important:** The venv does NOT have `pip` installed. Use `uv` for all package management.

### Package Management with uv

```bash
# Install packages
uv pip install <package> --python .venv/bin/python

# Install from requirements
uv pip install -r requirements.txt --python .venv/bin/python

# List installed packages
.venv/bin/python -m pip list
```

### Running Python Scripts

Use the full path to the venv Python interpreter:

```bash
# Good
.venv/bin/python script.py

# Also works (in bash with source)
source .venv/bin/activate && python script.py

# Bad - won't use venv packages
python script.py
```

### Starting MarkDeck Server

```bash
# Start server in background
.venv/bin/markdeck present examples/features.md --port 8888 --no-browser &

# Or with activation
source .venv/bin/activate && markdeck present examples/features.md --port 8888 --no-browser
```

## Network Restrictions

### Blocked Domains

This environment has network restrictions that block the following domains:

- `playwright.dev`
- `cdn.playwright.dev`
- `storage.googleapis.com`
- `playwright.download.prss.microsoft.com`

### Impact

These restrictions prevent:
- Playwright browser binary downloads (Chromium, Firefox, WebKit)
- ChromeDriver downloads
- Some CDN resources

### Workarounds

1. **GitHub Actions** (Recommended): The `.github/workflows/screenshots.yml` workflow runs in GitHub's environment which has full network access
2. **Pre-installed browsers**: Check for system-installed Chrome/Chromium
3. **Alternative tools**: Selenium with pre-installed browsers (if available)

## Screenshot Generation

### Current Status

- ✅ Playwright library can be installed
- ❌ Playwright browsers cannot be downloaded (403 Forbidden)
- ✅ GitHub Actions workflow is configured and working
- ✅ Manual screenshots are possible via browser tools

### Playwright Installation

```bash
# Install Playwright Python package (works)
uv pip install playwright --python .venv/bin/python

# Install browser binaries (FAILS due to network restrictions)
.venv/bin/python -m playwright install chromium
```

Error received:
```
Error: Download failed: server returned code 403 body 'Host not allowed'
```

### GitHub Actions Workflow

The automated screenshot generation works via GitHub Actions:

**File:** `.github/workflows/screenshots.yml`

**How it works:**
1. Installs MarkDeck with screenshot dependencies
2. Installs Playwright browsers (works in GitHub environment)
3. Starts MarkDeck server on port 8888
4. Runs `capture_screenshots.py` script
5. Commits screenshots back to repository

**Manual trigger:**
- Go to repository Actions tab
- Select "Generate Grid View Screenshots"
- Click "Run workflow"

## Project Structure

```
markdeck/
├── .venv/                      # Python virtual environment (uv-based)
├── .github/workflows/          # GitHub Actions workflows
│   └── screenshots.yml        # Screenshot generation workflow
├── markdeck/                   # Main package
│   └── static/                # Static assets (JS, CSS)
│       └── slides.js          # Grid view implementation
├── examples/                   # Example presentations
│   └── features.md            # Demo presentation
├── screenshots/                # Generated screenshots
├── capture_screenshots.py     # Playwright screenshot script
└── CLAUDE.md                  # This file

```

## Testing Grid View Feature

### Start Server

```bash
.venv/bin/markdeck present examples/features.md --port 8888 --no-browser &
```

### Verify Server

```bash
curl -f http://127.0.0.1:8888/ -o /dev/null -w "HTTP Status: %{http_code}\n"
# Should return: HTTP Status: 200
```

### Manual Testing

1. Open browser to http://127.0.0.1:8888
2. Press `O` to toggle grid overview
3. Click on slides to navigate
4. Current slide is highlighted in grid

### Verify JavaScript Loaded

```bash
curl http://127.0.0.1:8888/static/slides.js | grep "toggleGrid"
```

## Common Issues and Solutions

### Issue: `playwright` module not found after installation

**Cause:** Installed with system pip instead of venv

**Solution:**
```bash
uv pip install playwright --python .venv/bin/python
.venv/bin/python script.py
```

### Issue: `markdeck: command not found`

**Cause:** Not using venv binary

**Solution:**
```bash
.venv/bin/markdeck present examples/features.md
```

### Issue: Playwright browser download fails with 403

**Cause:** Network restrictions block CDN domains

**Solution:** Use GitHub Actions workflow instead of local installation

## Git Workflow

**Current Branch:** `claude/playwright-screenshots-OF6Q9`

### Committing Changes

```bash
git add <files>
git commit -m "Description of changes"
```

### Pushing Changes

```bash
git push -u origin claude/playwright-screenshots-OF6Q9
```

**Important:** Branch must start with `claude/` and end with the session ID, otherwise push will fail with 403.

## Useful Commands

### Check uv version
```bash
uv --version
```

### List Python packages in venv
```bash
.venv/bin/python -m pip list
```

### Check if server is running
```bash
curl http://127.0.0.1:8888/ -I
```

### Kill background processes
```bash
pkill -f "markdeck present"
```

## Tips for Future Claude Sessions

1. Always use `uv` for package management, not `pip`
2. Use full path `.venv/bin/python` for running scripts
3. Remember network restrictions - don't try to download browser binaries locally
4. GitHub Actions is the recommended way to generate screenshots
5. Server must be started from venv: `.venv/bin/markdeck`
6. Check if background server is still running before starting new one
7. Branch naming is critical for push permissions

## References

- [uv documentation](https://github.com/astral-sh/uv)
- [Playwright Python](https://playwright.dev/python/)
- [MarkDeck Grid View Feature](GRID_VIEW_FEATURE.md)
- [Screenshot Methods](SCREENSHOT_METHODS.md)
- [Network Configuration Details](PLAYWRIGHT_NETWORK_CONFIG.md)
