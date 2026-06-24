# WebinarNinja Skill

## Overview
Beheer WebinarNinja webinars voor Dubai Property via Playwright automation.

**Account:** admin@dubai-property.nl  
**Subdomain:** dubai-property.webinarninja.com  
**Session opslag:** `~/.auth/webinarninja.json`

---

## ⚠️ WERKWIJZE: Altijd dupliceren, nooit nieuw aanmaken

**Seyed's instructie (16 april 2026):** Maak NOOIT een nieuw webinar aan via "Create New Webinar".  
Dupliceer altijd de meest recente webinar via **More → Clone**. Hiermee worden alle settings correct overgenomen:
- Cover foto (speaker foto van LinkedIn)
- Registratiepagina template met gold-knop
- Omschrijving en teksten in de juiste stijl
- Email notifications
- Registratievragen (interesse, termijn, budget)

**Daarna aanpassen:**
1. Titel (stap 1)
2. Datum (stap 1)
3. Beschrijving/inhoud (stap 2)
4. Embed form aanmaken
5. Webflow CMS updaten

---

## Setup: Login

```python
EMAIL = "admin@dubai-property.nl"
PASSWORD = # zie ~/.openclaw/secrets/webinarninja of WEBINARNINJA_PASSWORD

AUTH_FILE = Path.home() / ".auth" / "webinarninja.json"

# Login script
await page.goto("https://my.webinarninja.com/login")
email_input = page.locator("input[name='email']:visible")
pwd_input = page.locator("input[name='password']:visible")
await email_input.fill(EMAIL)
await pwd_input.fill(PASSWORD)
await page.keyboard.press("Enter")
await page.wait_for_load_state("networkidle")

# Save session
storage = await page.context.storage_state()
AUTH_FILE.write_text(json.dumps(storage))
```

---

## Stap 1: Dupliceer laatste webinar

### Via Browser UI (enige betrouwbare methode)
De clone API (`/api/v1/cloned-webinars`) werkt **niet headless** — geeft altijd "invalid date range".  
Gebruik de UI:

```python
# Click More → Clone → OK
await page.goto("https://dubai-property.webinarninja.com/app/webinars/dashboard")
await page.locator("text=More").first.click()
await page.wait_for_timeout(800)

# Clone via menu
await page.evaluate("""
    () => {
        const btns = document.querySelectorAll('button.btn.-menu');
        for (const btn of btns) {
            if (btn.innerText.trim() === 'Clone') { btn.click(); return; }
        }
    }
""")
await page.wait_for_timeout(1500)

# Click OK in confirmation dialog (gebruik force=True)
ok_btn = page.locator("button.btn.-primary.-fixed:has-text('OK')")
await ok_btn.click(force=True)
await page.wait_for_timeout(10000)  # Clone duurt lang!
```

### Clone ID vinden
Na clone → reload → check `?filter=past` of check de upcoming list via API:

```python
webinars = await page.evaluate("""
    async () => {
        const r = await fetch('/api/v1/users/4632613/webinars?perpage=500&filter[archived]=0&type=all', {
            credentials: 'include', headers: {Accept: 'application/json'}
        });
        const d = await r.json();
        return d.data.map(w => ({id: w.id, title: w.title}));
    }
""")
```

---

## Stap 2: Edit de kloon

Navigeer naar edit URL:
```
https://dubai-property.webinarninja.com/account/creator/webinars/{NEW_ID}/live/update/details
```

### Title aanpassen
```python
await page.evaluate(f"""
    () => {{
        const el = document.querySelector('#live-webinar-0-title');
        el.focus();
        el.value = '{new_title}';
        el.dispatchEvent(new Event('input', {{bubbles: true}}));
        el.dispatchEvent(new Event('change', {{bubbles: true}}));
    }}
""")
```

### Datum aanpassen (format: "May 13, 2026")
```python
date_vis = page.locator("input[name='webinar[0][date]']:visible")
await date_vis.click(click_count=3)
await date_vis.fill("May 13, 2026")
await page.keyboard.press("Tab")
```

### Save & Next door alle 5 stappen
```python
for step in range(5):
    btn = page.locator("button:has-text('Save & Next'), button:has-text('Skip & Finish')")
    if await btn.count() > 0:
        await btn.first.click()
        await page.wait_for_load_state("networkidle", timeout=15000)
        await page.wait_for_timeout(2000)
    else:
        break
```

---

## Stap 3: Embed form aanmaken

```python
embed_url = f"https://dubai-property.webinarninja.com/account/creator/integrations/registration-forms/create/step-1?webinar_id={new_id}&webinar_type=live"
await page.goto(embed_url)
await page.wait_for_timeout(2000)

save_btn = page.locator("button:has-text('Save')")
await save_btn.first.click()
await page.wait_for_timeout(2000)

# Get embed ID
source = await page.content()
embed_ids = re.findall(r'embedding-form[/-](\d+)', source)
# embed_ids[0] is het embed ID (bijv. 10431, 10432)
```

**Embed code template:**
```html
<div data-rt-embed-type="true">
  <!-- WebinarNinja embedding registration form -->
  <iframe style="min-width: 320px; width: 100%; height: 420px; border: 0; overflow: hidden;"
          class="webinarninja-embedding-registration-form-{EMBED_ID}"
          src="https://my.webinarninja.com/embedding-form/{EMBED_ID}"></iframe>
  <script>
    function updateIframe(e){switch(e.type){case"resizeIframe":this.style.height=e.height+"px";break;case"iframeDownloadFailed":this.hidden=!0;break;default:return}}
    window.addEventListener("message",function(e){var a=document.querySelectorAll(e.data.id);[].forEach.call(a,function(a){updateIframe.call(a,e.data)})});
  </script>
</div>
```

---

## Stap 4: Webflow CMS updaten

**Webinars collectie ID:** `680a6e5211acc5d3f7e89a0b`

### Bestaand item updaten (PATCH)
```bash
curl -X PATCH "https://api.webflow.com/v2/collections/680a6e5211acc5d3f7e89a0b/items/{ITEM_ID}" \
  -H "Authorization: Bearer $WEBFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "fieldData": {
      "name": "...",
      "slug": "...",
      "heading": "...",
      "datum": "...",
      "tijd": "...",
      "webinar-code-rich": "...",
      "cover": {"fileId": "...", "url": "..."}
    }
  }'
```

### Nieuw item aanmaken (POST) + publiceren
```bash
# Create
curl -X POST ".../items" -d '{...}'

# Publish
curl -X POST ".../items/publish" -d '{"itemIds": [...]}'

# Site publish (wacht 35s na rate limit)
sleep 35 && curl -X POST ".../sites/{site_id}/publish" \
  -d '{"publishToWebflowSubdomain": true, "customDomains": ["690ce65abb41e489c9bc35e1", "690ce659bb41e489c9bc35b7"]}'
```

---

## Cover Image maken

### Via MiniMax image-01
```bash
MINIMAX_KEY="sk-cp-..." # zie ~/.openclaw/secrets/.env
curl -X POST "https://api.minimax.io/v1/image_generation" \
  -H "Authorization: Bearer $MINIMAX_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "image-01",
    "prompt": "Professional webinar cover...",
    "aspect_ratio": "16:9",
    "response_format": "url",
    "n": 1,
    "prompt_optimizer": true
  }'
```

---

## Registratielink patroon
`https://dubai-property.webinarninja.com/live-webinars/{WEBINAR_ID}/register`

---

## Bekende valkuilen

1. **Clone API werkt niet headless** — altijd via browser UI (More → Clone → OK)
2. **Embed ID ≠ Webinar ID** — embed ID is een aparte korte nummering (bijv. 10431)
3. **Rate limit Webflow publish** — wacht 35+ seconden tussen calls
4. **Session verloopt** — check altijd of je op login page belandt, zo ja herlogin
5. **Confirm dialogs** — WebinarNinja heeft Angular overlays die normale clicks blokkeren, gebruik `force=True`
6. **Datum format** — altijd "May 07, 2026" (niet "05/07/2026")

---

## Webflow Webinar CMS Velden

| Field | Type | Beschrijving |
|-------|------|-------------|
| name | PlainText | Interne naam |
| slug | PlainText | URL slug |
| heading | PlainText | Hoofdtitel op pagina |
| subheading | PlainText | Ondertitel |
| paragraph-1 | RichText | Intro tekst |
| date-time | PlainText | Datum + tijd (leesbaar) |
| datum | PlainText | Alleen datum |
| tijd | PlainText | Alleen tijd |
| cover | Image | Cover afbeelding |
| heading-2 | PlainText | "Wat bespreken we?" |
| paragraph-2 | PlainText | Spreker bio |
| paragraph-2-picture | Image | Spreker foto |
| bullet-1 t/m bullet-5, bulet-6 | PlainText | Onderwerpen |
| webinar-code-rich | RichText | Embed iframe code |
| seo-meta | PlainText | SEO beschrijving |
| webinar-passed | Switch | true = verlopen |
