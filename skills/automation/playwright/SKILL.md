# SKILL.md - Playwright Browser Automation

**Owner:** Appie-3 (CTO)
**Created:** 2026-04-07
**Purpose:** Browser automation for web scraping, form filling, testing, and repetitive web tasks

---

## What is Playwright?

Microsoft's browser automation framework. Gives your agent full control of a real browser — click buttons, fill forms, scrape content, take screenshots, test websites.

**Works with:** Chromium, Firefox, WebKit (all three browsers)

---

## Installation

```bash
# As npm package
npm install playwright

# Install browsers
npx playwright install chromium
npx playwright install firefox
npx playwright install webkit

# MCP server (for agent integration)
npx @playwright/mcp@latest
```

---

## Core Capabilities

| Capability | What It Does |
|------------|-------------|
| **Navigation** | Go to URLs, click links, navigate back/forward |
| **Interaction** | Click buttons, fill inputs, select dropdowns, checkboxes |
| **Extraction** | Scrape text, images, tables, JSON from any page |
| **Screenshots** | Full page or element screenshots |
| **PDF Generation** | Save pages as PDF |
| **Network Interception** | Block requests, mock responses |
| **Authentication** | Login to sites, handle cookies |
| **File Upload** | Upload files to web forms |

---

## Python SDK (Recommended for Agents)

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # Navigate
    page.goto("https://example.com")
    
    # Interact
    page.fill("#search-input", "my search query")
    page.click("#search-button")
    
    # Extract
    results = page.query_selector_all(".result-item")
    for result in results:
        title = result.query_selector("h3").inner_text()
        link = result.query_selector("a").get_attribute("href")
        print(f"{title}: {link}")
    
    # Screenshot
    page.screenshot(path="screenshot.png", full_page=True)
    
    browser.close()
```

---

## JavaScript/Node.js SDK

```javascript
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  await page.goto('https://example.com');
  await page.fill('#search', 'query');
  await page.click('#submit');
  
  const results = await page.$$eval('.result', els => 
    els.map(el => ({ title: el.textContent, url: el.href }))
  );
  
  console.log(results);
  await browser.close();
})();
```

---

## Common Use Cases for Appie

### 1. Web Scraping
```python
# Scrape job listings from a site
page.goto("https://jobs.company.com")
page.fill("#keyword", "engineer")
page.click(".search-btn")
page.wait_for_selector(".job-card")

jobs = []
for card in page.query_selector_all(".job-card"):
    jobs.append({
        "title": card.query_selector("h3").inner_text(),
        "company": card.query_selector(".company").inner_text(),
        "url": card.query_selector("a").get_attribute("href")
    })
```

### 2. Form Automation
```python
# Fill and submit a contact form
page.goto("https://example.com/contact")
page.fill("#name", "Seyed Hosseini")
page.fill("#email", "seyed@weblyfe.nl")
page.fill("#message", "Interested in your services")
page.select_option("#budget", "$5,000-10,000")
page.click("#submit")
page.wait_for_selector(".confirmation")
```

### 3. Login + Authenticated Actions
```python
# Login to a site
page.goto("https://app.example.com/login")
page.fill("#username", "user@example.com")
page.fill("#password", "password123")
page.click(".login-btn")
page.wait_for_selector(".dashboard")

# Now do authenticated actions
page.click(".new-project-btn")
```

### 4. Screenshot for Verification
```python
# Take screenshot of a page
page.goto("https://staging.example.com")
page.screenshot(path="staging-homepage.png", full_page=True)

# Take element screenshot
element = page.query_selector(".pricing-card.highlight")
element.screenshot(path="pricing-highlighted.png")
```

### 5. Test a Deployed Website
```python
# Verify page loads without errors
page.goto("https://new-site.vercel.app")
assert page.title() == "Expected Title"
assert page.query_selector(".hero") is not None
console_errors = []
page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
page.reload()
assert len(console_errors) == 0, f"Console errors: {console_errors}"
```

### 6. Extract Data from Tables
```python
# Pull data from a data table
page.goto("https://analytics.example.com/reports")
page.wait_for_selector(".data-table")

headers = [th.inner_text() for th in page.query_selector_all(".data-table th")]
rows = []
for tr in page.query_selector_all(".data-table tbody tr"):
    cells = [td.inner_text() for td in tr.query_selector_all("td")]
    rows.append(dict(zip(headers, cells)))
```

---

## Agent Integration Patterns

### Pattern 1: Direct Tool Use
Appie writes and executes Playwright scripts directly. Best for one-off tasks.

### Pattern 2: MCP Server
Run `npx @playwright/mcp@latest` — Appie can call browser tools via MCP protocol. Better for recurring tasks.

### Pattern 3: Skill Files
Create reusable SKILL.md patterns for common browser tasks. Appie reads and follows.

---

## Best Practices

| Practice | Why |
|----------|-----|
| **Always `wait_for_selector`** | DOM might not be ready |
| **Use `page.goto(..., wait_until='networkidle')`** | Wait for page to fully load |
| **Close browser when done** | Prevent resource leaks |
| **Use headless=True for automation** | Faster, no UI needed |
| **Set reasonable timeouts** | `page.set_default_timeout(30000)` |
| **Handle popups** | `page.on("dialog", lambda d: d.accept())` |

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Element not found | Add `wait_for_selector()` before interacting |
| Page not loading | Check URL, add longer timeout |
| Login failing | Check for hidden inputs, CSRF tokens |
| Screenshot blank | Use `full_page=True` or wait for content |
| Memory leak | Always `browser.close()` in finally block |

---

## See Also

- **Playwright MCP server** — Connect to agents via Model Context Protocol
- **browser-use** — Higher-level browser automation
- **web-automation patterns** — Common workflows

---

*Learn more: https://playwright.dev*
