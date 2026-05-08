#!/bin/bash
# Weblyfe Thumbnail Generator
# Uses Puppeteer to render HTML templates to 1280x720 PNG/JPG
#
# Usage:
#   ./generate-thumbnail.sh <template> <output> [--text-main "TEXT"] [--text-sub "TEXT"] [--face "path.png"]
#
# Templates: client-success, interview, educational, vlog, series
#
# Examples:
#   ./generate-thumbnail.sh client-success ./output/roslan.jpg --text-main '$0 to $8K' --text-sub 'IN 30 DAYS'
#   ./generate-thumbnail.sh interview ./output/roslan-interview.jpg --text-main '$50K to $1M+' --text-sub 'ROSLAN'

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TEMPLATE="$1"
OUTPUT="$2"
shift 2

TEXT_MAIN=""
TEXT_SUB=""
FACE=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --text-main) TEXT_MAIN="$2"; shift 2 ;;
    --text-sub) TEXT_SUB="$2"; shift 2 ;;
    --face) FACE="$2"; shift 2 ;;
    *) shift ;;
  esac
done

TEMPLATE_FILE="$SCRIPT_DIR/templates/${TEMPLATE}.html"

if [ ! -f "$TEMPLATE_FILE" ]; then
  echo "Error: Template '$TEMPLATE' not found at $TEMPLATE_FILE"
  echo "Available: client-success, interview, educational"
  exit 1
fi

# Generate using Puppeteer
node -e "
const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 720, deviceScaleFactor: 1 });
  
  let html = fs.readFileSync('${TEMPLATE_FILE}', 'utf8');
  
  // Replace text placeholders
  const textMain = '${TEXT_MAIN}';
  const textSub = '${TEXT_SUB}';
  const face = '${FACE}';
  
  if (textMain) {
    html = html.replace(/(<div class=\"text-main\">)(.*?)(<\/div>)/, \`\$1\${textMain}\$3\`);
  }
  if (textSub) {
    html = html.replace(/(<div class=\"text-sub\">)(.*?)(<\/div>)/, \`\$1\${textSub}\$3\`);
  }
  if (face && fs.existsSync(face)) {
    const faceBase64 = fs.readFileSync(face).toString('base64');
    const ext = path.extname(face).slice(1);
    const dataUri = \`data:image/\${ext};base64,\${faceBase64}\`;
    html = html.replace(
      /<div class=\"face-placeholder\">.*?<\/div>/,
      \`<img src=\"\${dataUri}\" style=\"max-height:680px;max-width:560px;object-fit:contain;\">\`
    );
  }
  
  await page.setContent(html, { waitUntil: 'networkidle0' });
  await new Promise(r => setTimeout(r, 1500)); // Wait for fonts
  
  const output = '${OUTPUT}';
  if (output.endsWith('.jpg') || output.endsWith('.jpeg')) {
    await page.screenshot({ path: output, type: 'jpeg', quality: 90 });
  } else {
    await page.screenshot({ path: output, type: 'png' });
  }
  
  await browser.close();
  const stats = fs.statSync(output);
  console.log(\`Thumbnail saved: \${output} (\${(stats.size/1024).toFixed(0)}KB)\`);
})();
" 2>&1
