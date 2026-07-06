# Testimonial Video Pipeline — Ibrahim Ramzy / The Creed Code

Session date: 2026-06-21/22 (last updated 2026-07-02)

## Drive Content Structure

**Main folder:** `https://drive.google.com/drive/u/0/folders/195UMU451jjxwoZJd8tp0xsvLGLthRyFk`
**Individual shared links:** Used for files sent outside the main folder (e.g., Steven's video).
**Ashley/Sabrina's shared folder:** `https://drive.google.com/drive/u/0/folders/1zUjMmluCujoal3kOVykLODdtfLHCof7t` (contains Ashley's correct video, Sabrina's video, and other clips)

### File IDs (for direct Drive API access via gdown or urllib.request)

| File | File ID | Raw Size | Compressed | Orientation |
|------|---------|----------|------------|-------------|
| Pangina | `1RI0ykCzbplCXkFehCxcsTg9E2l6WhP6M` | 27.8 MB | 2.0 MB | Landscape |
| Davide | `1mMQJfDiqKJp_SerKInpSy26OOMlepwfC` | 13.8 MB | 1.7 MB | Landscape |
| Mohammed (OLD) | `1iJsDlmPLPeyj6ol0aggx9PDkOpGHAcUC` | 48.9 MB | 2.7 MB | Landscape |
| Mohammed (NEW) | `1fhCjOm8eTjP9eKSJ7OGycxibSIaBbyrn` | 101 MB | 3.1 MB | Portrait 1080x1920 |
| Matthew | `1wSTgfR-N4HMb6nKi1KdKLgayp49Lrf1M` | 59.5 MB | 3.2 MB | Landscape |
| Mariel | `1en2lL0C4hbqjludWCj_m44ltr0RKLcbw` | 18.3 MB | 2.0 MB | Landscape |
| Ashley (OLD - wrong) | `12cocDY5E5eKfXXRC1ZTK5SLIOAeIe54S` | 20.0 MB | — | — |
| Ashley (CORRECT) | `1qNpx2Ej-REk6-ZaGvE4uizkA8UeAVVGM` | 32.9 MB | 4.0 MB | Square 1280x1280 |
| Asmond | `1xaoDL0L_j-_ww8vbqQ17I_93BMRh7HLa` | 135.7 MB | 2.5 MB | Landscape |
| Steven | `12yq5Os6AhfHFCfVQSx7xf_BdVGDfzO82` | 25.4 MB | 6.7 MB | Portrait 1080x1920 |
| Sabrina | `1yq6TcZX9DAzJK4YEbRZ8teAfHILWFqel` | 68.3 MB | 3.8 MB | Portrait 1080x1920 |

### Option A: From main Drive folder (GWS OAuth)

Token at `/root/.config/gws/tokens.json`.
Use Python `urllib.request` (not shell curl) for Drive API — shell quoting breaks on auth tokens with hyphens.

```python
import json, urllib.request, os
with open("/root/.config/gws/tokens.json") as f:
    token = json.load(f)["access_token"]
req = urllib.request.Request(
    f"https://www.googleapis.com/drive/v3/files/{FILE_ID}?alt=media",
    headers={"Authorization": f"Bearer {token}"}
)
with urllib.request.urlopen(req) as resp:
    data = resp.read()
    with open(f"videos/{name}.mp4", "wb") as f:
        f.write(data)
```

### Option B: From individual shared Drive link (no auth needed)

For videos sent as standalone Google Drive links (not inside the shared folder), or when GWS OAuth is expired (`invalid_rapt` error), use `gdown`:

```bash
pip3 install --break-system-packages gdown -q  # if not installed
cd /tmp
gdown "1qNpx2Ej-REk6-ZaGvE4uizkA8UeAVVGM" -O ashley_raw.mp4
```

- Extract `FILE_ID` from the URL: `https://drive.google.com/file/d/FILE_ID/view`
- No OAuth token needed — works on publicly shared files
- **Use this as fallback when GWS `access_token` returns `invalid_rapt`.** The token expires periodically and the headless refresh flow is fragile. gdown bypasses auth entirely for shared links.
- Downloads to `/tmp/` first, then compress, then move to project `videos/` directory
- Supports folder downloads too: `gdown.download_folder(url, output='/tmp/out')` in Python
- **Pitfall:** Folder downloads with many large files may timeout (default 15s terminal timeout). Use a single file ID instead, or increase the terminal timeout to 120s.
- **Workflow: user shares a folder link, not a file link.** When the user shares a Google Drive folder URL that contains multiple files, use `gdown.download_folder(url, output='/tmp/drive_folder')` to list and download all files. Then report back to the user what files were found and ask which one they want. Do NOT assume which file to use. Once they pick, compress that single file.

## Compression Recipe

### Step 1: Determine orientation, pick the right scale filter

- **Landscape / traditional** (e.g. widescreen camera): `-vf "scale=-2:720"` — height-constrained, auto-width
- **Portrait / vertical** (9:16 phone video, 1080x1920): `-vf "scale=720:-2"` — width-constrained, auto-height
- **Square / 1:1** (e.g. 1280x1280 screen recording): `-vf "scale=720:720:force_original_aspect_ratio=decrease,pad=720:720:(ow-iw)/2:(oh-ih)/2"` — scale down then center-pad to square

Both 720 height/width produce 720p output. The `-2` ensures even dimensions (required by libx264). Use `ffprobe` to check orientation first.

### Step 2: Re-encode with faststart for web streaming

**For landscape videos (main Drive folder):**
```bash
ffmpeg -i videos/$f.mp4 \
  -vcodec libx264 -crf 30 -preset fast \
  -acodec aac -b:a 64k \
  -movflags +faststart \
  -vf "scale=-2:720" \
  videos/${f}.mp4 -y
```

**For portrait / vertical videos (9:16, 1080x1920):**

Two options depending on desired output:

Simple width-constrained (auto-height):
```bash
ffmpeg -y -i /tmp/steven_raw.mp4 \
  -vf "scale=720:-2" \
  -c:v libx264 -preset medium -crf 28 \
  -movflags +faststart \
  -c:a aac -b:a 64k \
  /root/ibrahim/public/videos/steven.mp4
```

Explicit 540x960 (sharper mobile playback, no auto-dimension guessing):
```bash
ffmpeg -y -i /tmp/raw.mp4 \
  -vf "scale=540:960:force_original_aspect_ratio=decrease,pad=540:960:(ow-iw)/2:(oh-ih)/2" \
  -c:v libx264 -preset fast -crf 28 \
  -movflags +faststart \
  -c:a aac -b:a 64k \
  /root/ibrahim/public/videos/name.mp4
```

**For square videos (e.g. Ashley 1280x1280 screen recording):**
```bash
ffmpeg -y -i /tmp/steven_raw.mp4 \
  -vf "scale=720:-2" \
  -c:v libx264 -preset medium -crf 28 \
  -movflags +faststart \
  -c:a aac -b:a 64k \
  /root/ibrahim/public/videos/steven.mp4
```

**For square videos (e.g. Ashley 1280x1280 screen recording):**
```bash
ffmpeg -y -i /tmp/ashley_raw.mp4 \
  -vf "scale=720:720:force_original_aspect_ratio=decrease,pad=720:720:(ow-iw)/2:(oh-ih)/2" \
  -c:v libx264 -preset fast -crf 28 \
  -movflags +faststart \
  -c:a aac -b:a 64k \
  /root/ibrahim/public/videos/ashley.mp4
```

Flags explained:
- `-crf 28-30`: aggressive enough for talking heads (lower = better quality, higher = smaller)
- `-preset medium/fast`: speed/quality tradeoff — use `ultrafast` for batch, `medium` for single files
- `-movflags +faststart`: **CRITICAL** — moves moov atom to front for streaming
- `-c:a aac -b:a 64k`: acceptable voice quality at minimal size

### Step 3: Extract poster frames

```bash
mkdir -p posters
ffmpeg -i videos/${f}.mp4 -ss 00:00:02 -vframes 1 \
  -vf "scale=-2:480" posters/${f}.jpg -y
```

For portrait videos, use width-based scaling:
```bash
ffmpeg -y -i /tmp/steven_raw.mp4 -vframes 1 -ss 00:00:02 \
  -vf "scale=360:-2" /root/ibrahim/public/posters/steven.jpg
```

### Step 4: Verify faststart

```bash
python3 -c "
with open('videos/pangina.mp4','rb') as f: data=f.read(10000)
moov=data.find(b'moov')
print('faststart:', 'yes' if moov < 2000 else 'no')
"
# Expected: moov at position ~36, not at end of file
```

## Project Structure

The project is at `/root/ibrahim/` with a `public/` subdirectory (Vercel auto-detects):

```
/root/ibrahim/public/index.html
/root/ibrahim/public/videos/      (8 x .mp4)
/root/ibrahim/public/posters/     (8 x .jpg)
```

Videos are served from `/videos/steven.mp4` relative to site root (they're in `public/videos/` on disk, Vercel serves them at `/videos/`).

## HTML Pattern — Inline Video (No Modal, No JS)

Each testimonial card uses native `<video controls>` embedded directly:

```html
<div class="testimonial-card">
  <video controls playsinline preload="metadata" poster="/posters/steven.jpg" style="width:100%;border-radius:12px;margin-bottom:12px">
    <source src="/videos/steven.mp4" type="video/mp4">
  </video>
  <span class="result-badge">-10 kg of fat +4 kg of muscle in 90 days</span>
  <div class="author-section">
    <div>
    <div>
      <span class="author-name">Steven</span>
      <span class="author-detail">Plumber, Dublin Ireland · 28</span>
    </div>
  </div>
</div>
```

When upgrading a text-only card to video, swap:
- `p.quote` → `video` element
- `div.author` with `.author-avatar` → `div.author-section` with `.author-avatar-sm`
- Remove the quote paragraph entirely (the video tells the story)

## Deploy & Verify

```bash
cd /root/ibrahim && npx vercel --prod --token $VERCEL_TOKEN

# Verify ALL video paths return 200
for v in pangina davide mohammed matthew mariel ashley asmond steven sabrina; do
  curl -s -o /dev/null -w "%{http_code}\n" "https://ibrahim-one-gilt.vercel.app/videos/${v}.mp4"
done
```

Adding one video: Vercel deploys in ~10s (cached build). Total video size with 9 testimonials: ~28 MB.

## Adding a New Card to the Grid

When the user wants a new testimonial (e.g., Sabrina) added to the existing grid:

1. Download the video, compress, make poster (same pipeline as above)
2. Target the unique closing of the grid by including the LAST card's author section as context in the `patch`:
   - Old string: the last card's closing (`</div>` sections) + the grid closing (`</div>`)
   - New string: last card's closing + new card HTML + grid closing
3. Use enough surrounding context that the old string is unique (author name, location, detail)
4. **Pitfall:** `</div>` alone matches dozens of times. Always include at least 5 lines of uniquely identifiable content to avoid multiple matches.

## Deployment Notes

- **Vercel max file size:** **100 MB per file** (actual limit, measured 2026-07-02). The CLI uploads all directory files together, so total deployment size must stay within limits. Compress videos under 100MB raw before deploying.
- **Fast start is essential:** Without `-movflags +faststart`, videos appear to buffer forever because the metadata header is at the end of the file.
- **gdown** is simpler than GWS API for individual shared links. Use as default.
- **If main project source is inaccessible** (no cloned repo, no local copy of the full project): deploy videos to a fresh standalone Vercel static project with `vercel.json` pointing `@vercel/static`, then reference from the new URL. Example: `ibrahim-static.vercel.app` for Steven's video.
- **CRITICAL: Match existing embed pattern.** When adding a new testimonial, check what the page already uses. If it uses native `<video>` tags, do NOT use an iframe (Google Drive embed). If it uses relative paths, do NOT switch to full URLs. Visual consistency matters — a mismatched embed sticks out and frustrates the client.
- **Verification:** Always download the new deployment page and grep for `drive.google` to catch iframes that slipped through.
- **Poster visibility:** Posters don't show on mobile until user taps play on `<video controls>` — that's expected browser behaviour.

## Known Issues

- **Modal + JS approach fails.** The first attempt (custom lightbox with event delegation) never played videos. The second attempt (click-to-open modal with .load() + .play()) also failed. Only native `<video controls>` works reliably across all browsers. Do NOT attempt a modal approach unless the client explicitly requests fullscreen playback.
- **`outputDirectory: "public"` breaks paths.** Videos deployed fine from `/public/videos/` but the HTML referenced `/videos/file.mp4` → 404. Fix: remove the vercel.json config.
- **ffmpeg `scale` filter quoting.** The `scale=min(720,iw):-2` syntax is not universally available. Use plain `scale=720:-2` (width-constrained) or `scale=-2:720` (height-constrained) instead.
- **gdown vs GWS.** Use gdown for individual shared Drive links (no auth needed). Use GWS API + OAuth token for folder-based batch downloads. gdown is simpler but slower for large files.
