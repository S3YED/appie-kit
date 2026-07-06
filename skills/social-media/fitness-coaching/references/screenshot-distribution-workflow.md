# Screenshot Distribution Workflow

Covers two distinct delivery patterns:
- **Pattern A: Zip file** — user uploads a zip of screenshots (e.g. "MOHAMMED -10KG.zip")
- **Pattern B: Direct images via chat** — user sends multiple individual images via Telegram with text instructions

## Key Lesson

The zip filename (e.g. "MOHAMMED -10KG.zip") does NOT mean all screenshots belong to that person. The user may have batch-saved screenshots from multiple client video calls into one zip. Every screenshot could be a different person.

## Pattern A: Zip File Distribution

### Step 1: Extract & optimize

```bash
apt-get install -y unzip -q
unzip -o "path/to/file.zip" -d /tmp/screenshots/
```

Convert all to web-optimized JPGs:

```python
import os
from PIL import Image

src = "/tmp/screenshots"
dst = "/root/ibrahim/public/transformations"
os.makedirs(dst, exist_ok=True)

for fname in sorted(os.listdir(src)):
    path = os.path.join(src, fname)
    img = Image.open(path).convert("RGB")
    out = os.path.join(dst, fname.replace('.png', '.jpg').replace('.PNG', '.jpg'))
    img.save(out, "JPEG", quality=82, optimize=True)
    print(f"Saved {out}")
```

Then rename them to proper person names once you know the mapping (see step 2).

### Step 2: Identify which screenshot is which person

**You cannot determine this from pixel analysis or OCR alone.** The screenshots are body transformation photos with no embedded text labels. You must ask the user:

> "Can you tell me which screenshot number goes to which person's card?"

When the user provides the mapping, rename files accordingly:

```bash
cd /root/ibrahim/public/transformations
cp 1.jpg pangina.jpg
cp 2.jpg steven.jpg
# ... etc
```

### Step 3: Update each person's card

Replace the placeholder div (gradient + initial letter) with an `<img>` tag:

```html
<!-- Pangina -->
<div class="trans-card">
  <div class="trans-placeholder" style="background: linear-gradient(135deg, #0F2D55, #072A42); display:flex; flex-direction:column; align-items:center; justify-content:center; gap:8px;">
    <img src="/transformations/pangina.jpg" alt="Pangina before and after" loading="lazy" style="width:100%;height:100%;object-fit:cover;border-radius:0;">
  </div>
  <p class="trans-name">Pangina, London UK</p>
  <p class="trans-result">⬇ 20kg in 12 weeks · 30 push-ups unlocked</p>
</div>
```

The `<img>` goes INSIDE the `.trans-placeholder` div — this maintains the card's aspect-ratio and overflow styling. Key attributes: `width:100%;height:100%;object-fit:cover;border-radius:0;` — fills the placeholder area exactly.

### Step 4: Add new people as new cards

If a screenshot shows someone not in the current grid, add a new card between the appropriate existing cards. Maintain the grid structure with the same `trans-card` class. Ask the user for the person's location and results text if not provided.

```html
<!-- Konstantin -->
<div class="trans-card">
  <div class="trans-placeholder" style="background: linear-gradient(135deg, #0F2D55, #072A42); display:flex; flex-direction:column; align-items:center; justify-content:center; gap:8px;">
    <img src="/transformations/konstantin.jpg" alt="Konstantin transformation" loading="lazy" style="width:100%;height:100%;object-fit:cover;border-radius:0;">
  </div>
  <p class="trans-name">Konstantin</p>
  <p class="trans-result">-10kg transformation</p>
</div>
```

The grid uses `grid-template-columns: repeat(auto-fit, minmax(200px, 1fr))` — new cards fit automatically. No CSS changes needed.

### Step 5: Cards that still have no screenshot

Leave as placeholder initials. Replace with images only when the user provides them.

## Pattern B: Direct Images via Chat (Telegram)

The user sends multiple images directly through Telegram chat, often with text instructions alongside. This is common when they have new screenshots from recent client video calls.

### Step 1: Acknowledge you cannot see the images

The Hermes image-parse system does not render Telegram images inline. State this plainly:

> "I can't see the images you sent — my system doesn't display Telegram photos inline."

Do NOT try to deduce content from file hash names, pixel data, or OCR (all unreliable for body transformation photos).

### Step 2: Ask for the image-to-person mapping

Since images arrive in a specific order on Telegram, ask the user to reference them by position:

> "Can you tell me which image goes where? For example: 'Image 1 → Pangina, Image 2 → Steven...'"

If the user says "I've named each of the images for you" — they mean the content of each image corresponds to the person's name. But you STILL can't see them. Ask for the mapping explicitly.

### Step 3: Handle name swaps and custom result text

The user will often say things like:

- "Swap with Fatuma and write that she lost 5 kg and completed her first half marathon in 90 days."
- "Omar, swap with Asmund who added 4 kg of muscle with bodyweight training from home."

When this happens:
1. The name before "swap" is the NEW person being added (e.g., Fatuma, Omar)
2. The name after "swap" (often "Asmund" = Asmond, "Fatuma" = replacing Ashley or another placeholder) is who they're replacing
3. The text after "write that" or implied in the sentence is the result text for the new person's `<p class="trans-result">`
4. Replace the replaced person's card entirely — delete the old card, insert the new one in its grid position
5. If the replaced card was in the middle of the grid, maintain grid order

Apply step 3 (update card HTML) and step 4 (add new cards) from Pattern A above.

### Step 4: Download & optimize the chat images

The images are cached at `/root/.hermes/image_cache/img_<hash>.jpg`. Copy them to the transformations directory with the correct person name:

```bash
cp /root/.hermes/image_cache/img_a0360eb48929.jpg /root/ibrahim/public/transformations/fatuma.jpg
cp /root/.hermes/image_cache/img_28a297898b37.jpg /root/ibrahim/public/transformations/omar.jpg
```

No re-compression needed — Telegram already compresses images on send.

### Step 5: Clean up and deploy

```bash
# Clean up old numbered files from the zip extraction
rm -f /root/ibrahim/public/transformations/[0-9]*.jpg

# Rename the zip-origin images that have better names now
# Deploy
cd /root/ibrahim && vercel --prod --token ...
```

## Pitfalls

- **Do NOT create a featured gallery card** with all screenshots in one person's card. The user will correct you. Each screenshot goes to one person's individual card.
- **Zip names are misleading.** "MOHAMMED -10KG.zip" may contain screenshots of Mohammed, Pangina, Steven, Davide, etc. Never assume.
- **Ask the user for the mapping** if you can't identify the person in each screenshot. Don't guess. One correct question is faster than rebuilding after a wrong guess.
- **Direct images via Telegram have no visible filenames.** The hash-based filenames (`img_a0360eb48929.jpg`) contain zero information about the content. Never attempt to infer content from the hash.
- **Pixel analysis and OCR do NOT work** for identifying which body transformation photo belongs to which person. The images are skin-tone photographs with no embedded labels.
- **Clean up old numbered files** after renaming: `rm -f /root/ibrahim/public/transformations/[0-9]*.jpg`
- **Do NOT add CSS** for gallery layouts (`.trans-card-featured`, `.trans-gallery`, `.trans-img`). The standard card grid handles individual images fine with `object-fit:cover`.
- **When user says "I've named each of the images for you"** — they mean the content is labeled (e.g. each image shows a different named client). You still cannot see this. Ask for the mapping.
- **When user gives swap instructions** ("Swap X with Y"), the first name is the NEW person, the second name is the person being REPLACED in the grid. Their result text should use the user's exact wording.