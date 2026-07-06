# Generate a VA-Ready Process Doc (PDF)

When Ibrahim needs a process doc for Lindsay or another VA, generate a clean PDF using fpdf2. The PDF replaces the raw markdown doc because macOS Finder can't open `.md` files natively.

## Tool

`fpdf2` (install: `pip3 install fpdf2 --break-system-packages`)

## Template Pattern

Use this structure in every VA process doc PDF:

1. **Title page** — "CREED GIVEAWAY — Lead Management Process" with For/From/Updated
2. **Your Role** — what they do + what they DON'T do (explicit boundaries)
3. **The Three Tiers** — commitment score table (Tier/Score/Action)
4. **Where Leads Come From** — Telegram, Ishan blast, Typeform
5. **Per-Tier Scripts** — exact WhatsApp messages, by day. Use `script_box()` for message previews and `note()` for instructions (when to send, what to attach, what to do on no reply)
6. **Daily Checklist** — numbered routine they follow every morning
7. **Quick Reference Table** — Day x Tier x Action matrix

## Best Practices

- **No call scripts.** VA docs are operational messaging only. Ibrahim handles all calls himself. Never write "what to say on the call" — that's his domain.
- **Use `"I am"` not `"I'm"`** in quote boxes — avoids apostrophe issues within single-quoted Python strings. The user reads these as normal WhatsApp messages.
- **fpdf2 uses latin-1 encoding** — bullet characters (•), em dashes (—), and curly quotes fail. Replace with: `"-"` for bullets, `" - "` for dashes.
- **Deprecation warnings** from fpdf2's `ln=` parameter are harmless. Script still produces valid PDFs.
- **Page overflow:** Use `if y + h > 270: pdf.add_page()` before drawing boxes that might run off the page.

## Quick Script Template

Save the Python script to `/tmp/make_pdf.py`, run it, output goes to `/root/<name>.pdf`. Send to user via `MEDIA:/root/<name>.pdf`.