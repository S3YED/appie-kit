# SKILL.md - YouTube Thumbnail Generator

You can generate YouTube thumbnails for Seyed's channel (@weblyfenl) using Seyed's actual photos and Weblyfe brand guidelines.

## Assets Location
- **Seyed's photos:** `/root/clawd/assets/seyed-photos/`
  - `seyed-closeup-resized.jpg` - Close-up face shot (BEST for thumbnails)
  - `seyed-n8n-speaking.jpg` - Speaking/presenting pose
  - `seyed-n8n-25s.jpg` - n8n video frame
  - `seyed-n8n-40s.jpg` - n8n video frame
  - `seyed-webcam-raw.png` - Webcam screenshot
- **HTML templates:** `/root/clawd/assets/thumbnail-templates/`
  - `client-success.html` - For client story videos (revenue numbers + face)
  - `interview.html` - For interview/conversation videos
  - `educational.html` - For tutorial/how-to videos
- **Generator script:** `/root/clawd/skills/thumbnails/generate-thumbnail.sh`
- **Full brand system:** `/root/clawd/skills/thumbnails/THUMBNAIL-SYSTEM.md`

## How to Generate a Thumbnail

### Method 1: Puppeteer Script (Preferred)
```bash
cd /root/clawd/skills/thumbnails
chmod +x generate-thumbnail.sh
./generate-thumbnail.sh <template> <output> --text-main "TEXT" --text-sub "TEXT" --face "/root/clawd/assets/seyed-photos/seyed-closeup-resized.jpg"
```

**Examples:**
```bash
# Client success story
./generate-thumbnail.sh client-success ./output/new-thumb.jpg \
  --text-main '$0 to $8K' --text-sub 'IN 30 DAYS' \
  --face /root/clawd/assets/seyed-photos/seyed-closeup-resized.jpg

# Interview thumbnail
./generate-thumbnail.sh interview ./output/interview.jpg \
  --text-main 'How I Built 3 AI Agents' --text-sub 'LIVE DEMO' \
  --face /root/clawd/assets/seyed-photos/seyed-n8n-speaking.jpg

# Educational tutorial
./generate-thumbnail.sh educational ./output/tutorial.jpg \
  --text-main 'n8n + AI' --text-sub 'FULL TUTORIAL' \
  --face /root/clawd/assets/seyed-photos/seyed-closeup-resized.jpg
```

### Method 2: AI Image Generation
When the Puppeteer script isn't enough (custom layouts, special effects), use the image_generate tool:

**Prompt formula:**
```
YouTube thumbnail, 1280x720, [SCENE DESCRIPTION]. 
Left side: photo of young Middle Eastern man with short dark hair and stubble, 
wearing [OUTFIT]. Right side: bold white text "[3-5 WORDS]" on dark green 
background (#031D16). Gold accent (#DFB771) highlight on key word. 
Bottom right: small "WEBLYFE" text in gold. High contrast, professional, 
clean composition. No em dashes.
```

## Brand Rules (MANDATORY)
- **Font:** Rethink Sans (800 for headlines, 700 for sub)
- **Colors:** Dark green #031D16, Gold #DFB771, White #F6FEFC, Emerald #247459
- **Face size:** Minimum 40% of frame height
- **Text:** 3-5 words max, 100-200px font size
- **WEBLYFE watermark:** Bottom-right, gold, Rethink Sans 600
- **Safe zone:** Nothing in bottom-right 200x40px (YouTube timestamp)
- **NO EM DASHES. EVER.**

## Thumbnail Categories

### 1. Client Success Stories (Most Important)
- Template: `client-success`
- Formula: Revenue number + client face/Seyed's face + name
- Example text: "$0 to $8K", "IN 30 DAYS"
- Always include the revenue metric

### 2. Interviews / Conversations
- Template: `interview`
- Formula: Key insight + both faces (or Seyed alone)
- Example text: "$50K to $1M+", "ROSLAN"

### 3. Tutorials / Educational
- Template: `educational`
- Formula: Tool name + benefit + Seyed's face
- Example text: "n8n + AI", "AUTOMATE EVERYTHING"

### 4. Vlog / Personal
- Use AI image generation for custom layouts
- More creative freedom, but keep brand colors

## Quick Checklist Before Delivering
- [ ] 1280x720 exactly
- [ ] Under 2MB file size
- [ ] Face visible and large (40%+ of frame)
- [ ] Text readable on mobile (phone-sized preview)
- [ ] Gold accent (#DFB771) on at least one element
- [ ] WEBLYFE watermark present
- [ ] No em dashes anywhere
- [ ] JPG quality 85-90%

## Dependencies
Make sure Puppeteer is installed:
```bash
npm install -g puppeteer
# or if it fails:
apt-get install -y chromium-browser
npm install puppeteer
```
