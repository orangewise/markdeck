# GitHub Actions Workflows

## Screenshots Workflow

Automatically generates screenshots of the MarkDeck grid view feature using Playwright in a CI environment.

### How to Use

#### Method 1: Manual Trigger (Recommended)

1. Go to **Actions** tab in GitHub
2. Select **"Generate Grid View Screenshots"** workflow
3. Click **"Run workflow"**
4. Screenshots will be:
   - Generated automatically
   - Uploaded as artifacts (downloadable for 90 days)
   - Committed back to the repository in `screenshots/` directory

#### Method 2: Automatic Trigger

The workflow runs automatically when you push changes to:
- `markdeck/static/**` (HTML/CSS/JS changes)
- `examples/**` (Example presentation changes)

### What Gets Generated

The workflow creates 6 screenshots:

1. **01_normal_view.png** - Normal presentation view
2. **02_grid_overview.png** - Grid view opened showing all slides
3. **03_grid_scrolled.png** - Scrolled grid view
4. **04_after_navigation.png** - After clicking to navigate to slide 3
5. **05_grid_current_highlight.png** - Grid showing current slide highlighted
6. **06_grid_hover_effect.png** - Hover effect demonstration

### Downloading Screenshots

**From GitHub UI:**
1. Go to the **Actions** tab
2. Click on the completed workflow run
3. Scroll down to **Artifacts**
4. Download **grid-view-screenshots.zip**

**Using GitHub CLI:**
```bash
gh run download <run-id> -n grid-view-screenshots
```

### Why This Works

This workflow solves the network restriction issue because:
- ✅ GitHub Actions has full internet access
- ✅ Can download Playwright browser binaries
- ✅ Runs in a clean Ubuntu environment
- ✅ No corporate firewall restrictions
- ✅ Automated and reproducible

### Local Testing

To test the workflow locally with `act`:

```bash
# Install act (GitHub Actions local runner)
brew install act  # macOS
# or
sudo snap install act  # Linux

# Run the workflow
act workflow_dispatch -W .github/workflows/screenshots.yml
```

### Troubleshooting

**If the workflow fails:**

1. **Server not starting:**
   - Check MarkDeck installation succeeded
   - Verify port 8888 is available
   - Check server logs in workflow output

2. **Screenshots not captured:**
   - Ensure Playwright installed correctly
   - Check browser binary installation
   - Verify `capture_screenshots.py` exists

3. **Commit fails:**
   - Check repository permissions
   - Ensure GITHUB_TOKEN has write access
   - Verify branch protection rules

### Environment Details

**OS:** Ubuntu Latest (GitHub-hosted runner)
**Node.js:** v20
**Python:** 3.11
**Browser:** Chromium (via Playwright)
**Resolution:** 1920x1080

### Cost

GitHub Actions is free for public repositories and includes:
- 2,000 minutes/month for private repos (free tier)
- Unlimited minutes for public repos

This workflow uses approximately **2-3 minutes** per run.
