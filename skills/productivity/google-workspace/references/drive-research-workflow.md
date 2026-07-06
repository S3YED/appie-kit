# Drive Research Workflow — Business Intelligence from Google Drive

End-to-end methodology to systematically explore a client's Google Drive and produce a structured business overview. Uses `gogcli` throughout.

## When to use

- A client says "investigate my Drive" or "find everything about [business name]"
- You need to understand a company's structure, client base, strategy docs, and assets
- You're onboarding as a digital assistant and need to learn the landscape

## Prerequisites

- `gog` installed and authenticated (see `references/gogcli-setup.md`)
- Client's Google account email (e.g. `solaiman@thegrowthexpress.com`)
- `GOG_KEYRING_PASSWORD` set if headless
- `pdftotext` installed for reading document contents:
  ```bash
  apt-get install -y poppler-utils  # Linux
  brew install poppler               # macOS
  ```

## Step-by-step workflow

### 1. Map the full folder structure

For a full recursive scan of the entire Drive, use `--all` + pagination (see **Fast path: recursive scan with `--all` + pagination** below). This is the most reliable way to get a complete view — it lists every file and folder at once, and you reconstruct the hierarchy from the `parents` field.

For a quick folder-only overview without full pagination:

```bash
gog drive ls --json --all --max 200 --client <client> | python3 -c "
import sys,json
d=json.load(sys.stdin)
folders=[f for f in d['files'] if 'folder' in f['mimeType']]
for f in folders: print(f'📁 {f[\"name\"]}  ({f[\"id\"]})')
"

### 2. Identify business-relevant folders

Scan the tree output for names matching the business name, client names, product names, or business functions (Sales, HRM, CRM, Marketing, Meetings, etc.).

Key folders types to flag:
- Direct business folders (`TGE Business`, `TGE 1:1`)
- Client/coaching folders
- Sales/Marketing folders
- Financial/bookkeeping
- Meeting recordings & notes
- Content & creative assets

### 3. Content search for broad coverage

Search across the whole Drive for files mentioning the business name, key products, or relevant keywords:

```bash
gog drive search --client <client> --plain "<business name>"
```

Also search for related keywords: `"coaching"`, `"client"`, `"contract"`, `"package"`, `"strategy"`, `"landing"`.

This catches files **anywhere** in the Drive, not just inside named folders — documents owned by other accounts (info@, team members), docs in non-obvious folders, Gemini-generated meeting notes, etc.

### 4. Drill into key folders

For each interesting folder, list contents:

```bash
gog drive ls --client <client> --plain --parent <FOLDER_ID>
```

For files with nested subfolders, repeat recursively.

### 5. Verify what type of data you're dealing with

Check MIME types to understand what's what:

```bash
gog drive ls --client <client> --json --results-only | python3 -c "
import json,sys
data = json.load(sys.stdin)
mimes = {}
for d in data:
    mt = d['mimeType']
    mimes[mt] = mimes.get(mt, 0) + 1
for m,c in sorted(mimes.items(), key=lambda x:-x[1]):
    print(f'{c:>3}x  {m}')
"
```

This reveals: Google Docs vs. Slides vs. Sheets vs. PDFs vs. videos vs. images. Helps prioritize what to read vs. what's raw media.

### 6. Download and extract Google-native docs

Google Docs/Sheets/Slides can't be read directly — export them:

```bash
gog drive download --client <client> <FILE_ID>
```

This saves to `~/.config/gogcli/drive-downloads/<ID>_<name>.pdf`.

Then extract to text:

```bash
pdftotext <path-to-pdf> -
```

For batch processing:

```python
import subprocess, os
pdfs = sorted(glob.glob("/root/.config/gogcli/drive-downloads/*.pdf"))
for p in pdfs:
    name = os.path.basename(p)
    txt = subprocess.run(["pdftotext", p, "-"], capture_output=True, text=True, timeout=15)
    print(f"=== {name} ===\n{txt.stdout[:2000]}")
```

### 7. Handle multi-account scenarios

Files may appear in search results owned by **different accounts** (e.g. `info@`, `tim@`, `tjoenyleylan@gmail.com`). Check the `owners` field in JSON output:

```bash
gog drive search --client <client> --json --results-only | python3 -c "
import json,sys
data = json.load(sys.stdin)
for d in data:
    owners = ', '.join(o['emailAddress'] for o in d.get('owners', []))
    print(f'{d[\"name\"]} | owner: {owners}')
"
```

To access info@-owned files that are shared with the main account, you'll need to set up `gog` for both accounts separately. Not all files from secondary accounts are downloadable through the primary account's auth.

### 8. Compile findings into a structured overview

Group findings by category:
- **Company identity**: what they do, USP, target audience
- **Products/services**: pricing, packages, tiers
- **Strategy & finance**: revenue targets, growth plans
- **Team & operations**: who's involved, roles, processes
- **Clients**: active coaching clients, testimonials
- **Marketing**: landing pages, content strategy, sales scripts
- **Events**: retreats, masterminds
- **Other projects**: side businesses (flag and confirm with client)

Use markdown tables, sections, and bullet points. End with a "klopt dit?" question to validate.

## Tips

### Fast path: recursive scan with `--all` + pagination

For large Drives (1000+ items), drilling folder-by-folder is too slow. Use `--all` to list **everything** at once, then rebuild the hierarchy from the `parents` field.

**Step 1: Pull all files with pagination**

```bash
# First page — max 1000 items
gog drive ls --json --all --max 1000 --client <client> > page1.json

# If there's a nextPageToken, keep going
next_token=$(python3 -c "import json; d=json.load(open('page1.json')); print(d.get('nextPageToken',''))")
page=2
while [ -n "$next_token" ]; do
    gog drive ls --json --all --max 1000 --page "$next_token" --client <client> > "page${page}.json"
    next_token=$(python3 -c "import json; d=json.load(open('page${page}.json')); print(d.get('nextPageToken',''))")
    ((page++))
done
```

**Step 2: Merge and analyze**

```python
import json, glob
from collections import Counter

all_files = []
for f in sorted(glob.glob("page*.json")):
    all_files.extend(json.load(open(f))['files'])

# Type breakdown
types = Counter()
for f in all_files:
    mt = f['mimeType']
    if 'folder' in mt: types['folder'] += 1
    elif 'video' in mt or 'quicktime' in mt: types['video'] += 1
    elif 'image' in mt or any(x in mt for x in ['jpeg','png','heic','arw']): types['image'] += 1
    elif 'document' in mt or 'wordprocessing' in mt: types['document'] += 1
    elif 'pdf' in mt: types['pdf'] += 1
    elif 'audio' in mt or 'm4a' in mt: types['audio'] += 1
    elif 'presentation' in mt: types['presentation'] += 1
    elif 'spreadsheet' in mt: types['spreadsheet'] += 1
    else: types['other'] += 1

print(f"Total: {len(all_files)}")
for t, c in types.most_common():
    print(f"  {t}: {c}")
```

**Step 3: Rebuild folder hierarchy**

The `parents` array on each file tells you which folder it lives in. Build a parent→children map:

```python
parent_map = {}
for f in all_files:
    for p in f.get('parents', []):
        parent_map.setdefault(p, []).append(f)

# Find root files (no parent, or parent not in the set of file IDs)
all_ids = {f['id'] for f in all_files}
roots = [f for f in all_files if not f.get('parents') or f['parents'][0] not in all_ids]

def print_tree(folder_id, depth=0):
    for child in parent_map.get(folder_id, []):
        prefix = "  " * depth
        print(f"{prefix}{'📁' if 'folder' in child['mimeType'] else '📄'} {child['name']}")
        if 'folder' in child['mimeType']:
            print_tree(child['id'], depth + 1)

for root in roots:
    print_tree(root['id'])
```

**Step 4: Save as compact index**

Write results to `/root/drive-index.md` (human-readable markdown) and `/root/drive-index.json` (full data). The markdown version should include:
- Total counts and type breakdown (table)
- Top-level folder structure with descriptions
- Folder hierarchy for deepest branches (Peak Physique, Content drives, etc.)
- Notable items: largest files, duplicate names, business-critical docs

**One-liner hybrid (quick structure scan)**

For fast folder mapping without full pagination:

```bash
gog drive ls --json --all --max 200 --client <client> 2>&1 | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(f'Items: {len(d[\"files\"])}')
folders=[f for f in d['files'] if 'folder' in f['mimeType']]
for f in folders: print(f'  📁 {f[\"name\"]}  ({f[\"id\"]})')
"

This hits the first 200 items — enough to map the folder structure — without pagination overhead.

- **JSON output is better for scripting** — use `--json --results-only` and pipe to `python3 -c` for analysis
- **Flat root = mixed files** — `gog drive ls` without `--parent` only shows root. Many files live in folders.
- **Gemini meeting notes** are auto-generated and often contain structured summaries/decisions/next steps — goldmine for understanding operations
- **Sheets export as CSV** — read with standard CSV parsing
- **Sales docs** often reveal pitch structure, objections, and closing frameworks
- **Coach contracts** show team structure, commission models, and role definitions

## Pitfalls

| Problem | Fix |
|---------|------|
| `gog drive ls` without `--parent` or `--all` only shows root | Use `--parent FOLDER_ID` to list subfolders, or `--all` for a full recursive sweep |
| 5,000+ item Drives hit pagination loops | Cap at 10 pages or use `--max 1000` to minimise round-trips |
| `nextPageToken` key may appear as `next_page_token` | Check both key names when parsing paginated responses |
| `--folder` flag doesn't exist on gog drive ls | Use `--parent` instead |
| Google Docs export permissions fail on some file types | Not all docs export cleanly — try `--export-mime text/plain` |
| Large meetings recordings (GBs) waste time downloading | Skip `.mov`/`.mp4` files unless the Gemini notes aren't enough; check notes first |
| Files owned by other accounts may not download | Note the ownership and check if the main account has edit/view access; re-auth under the owner account if needed |