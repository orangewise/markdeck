# Playwright Browser Download Blocked in Claude Code on the Web

## Issue Summary

Playwright browser binaries cannot be downloaded in Claude Code on the web sessions due to missing domains in the egress proxy allowlist.

**Status:** Blocked
**Date Reported:** 2025-12-28
**Affects:** Claude Code on the web sessions
**Does NOT affect:** Regular Claude.ai chat sessions (confirmed to have access)

## The Problem

When attempting to install Playwright browsers in Claude Code on the web:

```bash
.venv/bin/python -m playwright install chromium
```

**Error received:**
```
Error: Download failed: server returned code 403 body 'Host not allowed'
URL: https://cdn.playwright.dev/dbazure/download/playwright/builds/chromium/1200/chromium-linux.zip
URL: https://playwright.download.prss.microsoft.com/dbazure/download/playwright/builds/chromium/1200/chromium-linux.zip
```

## Root Cause

Claude Code on the web uses an **Envoy proxy** with JWT-based allowlist for egress traffic. The proxy configuration is controlled by:

- **Service:** `anthropic-egress-control`
- **Proxy server:** `21.0.0.89:15004` (container-specific)
- **Authentication:** JWT token embedded in environment variables
- **Blocking mechanism:** `x-deny-reason: host_not_allowed`

### Current Allowlist Status

The JWT's `allowed_hosts` field includes hundreds of development-related domains:
- ✅ `storage.googleapis.com`
- ✅ `github.com`, `raw.githubusercontent.com`
- ✅ `npmjs.com`, `registry.npmjs.org`
- ✅ `pypi.org`, `pypi.python.org`
- ✅ `microsoft.com`, `packages.microsoft.com`
- ✅ Many others (npm, maven, docker, gradle, rust, ruby, etc.)

**But missing:**
- ❌ `cdn.playwright.dev`
- ❌ `playwright.download.prss.microsoft.com`
- ❌ `*.playwright.dev` (wildcard)

## Key Discovery: Different Proxies for Different Services

**Regular Claude sessions (claude.ai):**
- Confirmed to have Playwright domains in allowlist
- Different proxy infrastructure

**Claude Code on the web:**
- Separate proxy configuration
- More restrictive allowlist (security for code execution)
- **Playwright domains NOT YET added to this specific allowlist**

## Evidence

### 1. Fresh JWT Token Analysis
After forcing environment refresh (exec bash):
- New JWT issued: `iat: 1766917369`
- Container changed: `sad-drab-flaky-comb`
- Proxy changed: `21.0.0.89:15004`
- **Playwright domains still missing from `allowed_hosts`**

### 2. Direct Network Tests
```bash
curl -I https://cdn.playwright.dev
# Result: HTTP/1.1 403 Forbidden
# Header: x-deny-reason: host_not_allowed
```

### 3. Playwright Installation Attempts
Multiple attempts across different containers and JWT tokens - all failed with identical 403 errors.

## Requested Domains to Add

Please add the following domains to the **Claude Code on the web** egress proxy allowlist:

1. `cdn.playwright.dev` - Primary CDN for Playwright browsers
2. `playwright.download.prss.microsoft.com` - Microsoft CDN mirror
3. `*.playwright.dev` (optional wildcard) - Future-proofing for any new subdomains

## Impact

**Users affected:**
- Anyone trying to use Playwright for browser automation in Claude Code on the web
- Screenshot generation workflows
- E2E testing scenarios
- Web scraping projects

**Current workarounds:**
1. ✅ GitHub Actions workflow (has full network access)
2. ❌ Local browser installation (no Chrome/Chromium in container)
3. ❌ Alternative CDNs (none available for Playwright)

## Reproduction Steps

1. Start Claude Code on the web session
2. Install Playwright: `uv pip install playwright --python .venv/bin/python`
3. Attempt browser download: `.venv/bin/python -m playwright install chromium`
4. Observe 403 errors from both CDN URLs

## Environment Details

- **Platform:** Claude Code on the web
- **Container OS:** Linux 4.4.0
- **Python:** 3.11
- **Playwright version:** 1.57.0
- **Chromium build:** 1200 (143.0.7499.4)

## Technical Details

### JWT Token Structure
```json
{
  "iss": "anthropic-egress-control",
  "organization_uuid": "[redacted]",
  "iat": 1766917369,
  "exp": 1766931769,
  "allowed_hosts": "[comma-separated list - missing playwright domains]",
  "is_hipaa_regulated": "false",
  "use_egress_gateway": "false",
  "session_id": "[session_id]",
  "container_id": "[container_id]"
}
```

### Environment Variables Affected
- `HTTPS_PROXY`
- `HTTP_PROXY`
- `GLOBAL_AGENT_HTTP_PROXY`
- `YARN_HTTPS_PROXY`
- `YARN_HTTP_PROXY`

All contain the JWT-authenticated proxy URL with the restricted allowlist.

## Recommendation

Add the Playwright CDN domains to the Claude Code on the web egress proxy allowlist to enable browser automation workflows. This is a standard development tool similar to the npm, pip, and maven registries already in the allowlist.

## Related Files in This Repository

- `/home/user/markdeck/CLAUDE.md` - Documents the network restrictions
- `/home/user/markdeck/.github/workflows/screenshots.yml` - Working GitHub Actions workaround
- `/home/user/markdeck/capture_screenshots.py` - Playwright screenshot script

## Contact

Repository: orangewise/markdeck
Branch: claude/fix-screenshot-generation-N9Uhn
Session: Claude Code on the web

---

**Note:** This issue is specific to Claude Code on the web infrastructure and does not affect regular Claude.ai chat sessions, which reportedly have access to these domains.
