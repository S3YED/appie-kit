---
name: soleiman-brand-assets
description: Manage Soleiman Advocatuur brand assets — final branding kit, logo variants, fonts, brand guidelines PDF, business card specs, and premium printer contacts. Activate when working with Soleiman website, print materials, or brand applications.
argument-hint: "[inventory|update|print] [args]"
---

# Soleiman Brand Assets

Brand asset management, business card production, and website deployment for **Soleiman Advocatuur** (mr. Ferdows Soleiman, Rotterdam).

## When to Use

- Applying brand to new materials (web, print, social)
- Updating the Soleiman website with correct brand files
- Specifying/ordering premium business cards or stationery
- Auditing brand consistency across touchpoints
- Searching for specific logo variant or font file

## Brand Asset Location

**Root:** `/root/soleiman-brand2/Branding 2/`

### Logo Variants (SVG)

| Variant | Path | Colors Available |
|---------|------|------------------|
| **Brandmark icon** (SA monogram) | `Brandmark Logo Icon svg/` | Black, gold, white, stone gray |
| **Main logo** (SA + SOLEIMAN ADVOCATUUR) | `Main Logo svg/` | black.svg, gold.svg, white.svg |
| **Horizontal logo** (+ "business") | `Horizontal Logo svg/` | Black, Gold, White |

### Logo Variants (PNG)

| Variant | Description |
|---------|-------------|
| `horisontal dark night.png` | Deep Navy background variant |
| `horisontal Ivory.png` | Ivory/white background variant |
| `horisontal gold.png` | Gold variant |
| `horizontal stone gray.png` | Stone gray variant |

### Brand Guidelines & Monogram

- **PDF:** `soleiman_a v02_compressed.pdf` — full brand guidelines
- **JPG:** `SA soleiman 02.jpg` — SA monogram high-res image

### Fonts

Located in `Fonts/`:

| Font | Files | Use |
|------|-------|-----|
| **Cinzel** (serif) | `Cinzel/` — variable + static weights (Regular → Black, SemiBold, Bold, ExtraBold) | Koppen, titels, naam, kernstatements |
| **Montserrat** (sans-serif) | `Montserrat/` — variable + static weights + italic variants (Thin → Black, Light, Medium, SemiBold, Bold, ExtraBold + italics) | Bodytekst, contactgegevens, ondersteunende content |

**Rule:** Cinzel voor kop/nadruk, Montserrat voor alle lopende tekst.

### Brand Colors

| Name | Hex | Use |
|------|-----|-----|
| Deep Navy | `#0D1B2A` | Basiskleur, vertrouwen en autoriteit |
| Heritage Gold | `#C9A062` | Accent, integriteit en waarde |
| Sandstone | `#EDE6DA` | Zacht neutraal, kalm en verfijnd |
| Stone Gray | `#B7B1A6` | Gegrond grijs, diepte en balans |
| Ivory White | `#F7F5F2` | Achtergrond, ruimte en licht |

**Baseline (NL):** "Recht. Vertrouwen. Resultaat."
**Baseline (EN):** "Advocacy with integrity. Results with purpose."

## Premium Business Cards — Specifications

### Design

| Element | Spec |
|---------|------|
| **Format** | 85 × 55 mm |
| **Front** | Deep Navy (`#0D1B2A`), SA monogram in Heritage Gold foil, "SOLEIMAN ADVOCATUUR" (Cinzel, gold), baseline "Recht. Vertrouwen. Resultaat.", thin gold border |
| **Back** | Ivory White (`#F7F5F2`), contact in Deep Navy: mr. Ferdows Soleiman, Stationsplein 45, 3013 AJ Rotterdam, +31 6 87996596, soleiman-advocatuur.vercel.app, QR code |
| **Fonts** | Cinzel (naam/titel), Montserrat (contact) |

### Paper & Finishing

| Element | Spec |
|---------|------|
| **Stock** | 600-800gsm, matte couche |
| **Front** | Heritage Gold foliedruk |
| **Back** | Deep Navy opdruk op Ivory White |
| **Finish** | Matte laminaat, optioneel verhoogde reliëf voor monogram |

### Premium Printers

| Printer | Specialty | Contact |
|---------|-----------|---------|
| **Speciaaldrukkerij Douma** (Friesland) | Letterpress, foliedruk, pregen, kleur op snee, maatwerk — topkeus | drukkerijdouma.nl, 0519 29 23 74 |
| **Drukbedrijf** (NL) | Goudfolie, soft-touch, 7 papiersoorten, online bestelsysteem | drukbedrijf.nl |
| **MOO** (International) | Letterpress business cards, premium stock, internationaal | moo.com/nl |
| **Lynx All-in** (Uitgeest) | Veredeling: folie, reliëf, soft-touch, begeleiding | lynxallin.nl |
| **Jukebox Print** (UK) | Painted edges, soft-touch, foil, extra thick stock | jukeboxprint.com |

## Website Deployment Workflow

The site is a Next.js app at `/root/soleiman-advocatuur/`. Deploy via GitHub:

```bash
cd /root/soleiman-advocatuur
git pull
# make changes in src/
git add -A && git commit -m "description" && git push
# Vercel auto-deploys within 1-2 min
```

**Live URL:** https://soleiman-advocatuur.vercel.app
**GitHub:** `github.com/S3YED/soleiman-advocatuur.git`

## Brand Update Workflow

When delivering new brand materials:

1. Check `/root/soleiman-brand2/Branding 2/` for existing assets
2. Copy new files into the brand directory
3. Update `/root/.hermes/BRAND.md` with new file paths and contact info
4. If website needs updating: copy SVG logos to `src/` under `public/` directory
5. Commit and push to deploy