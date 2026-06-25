#!/usr/bin/env python3
"""Regenerate skills/INDEX.md from SKILL.md frontmatter."""
import os, re, datetime

REPO = os.path.expanduser("~/clawd/projects/appie-kit")
SKILLS_DIR = os.path.join(REPO, "skills")

CATEGORY_ORDER = [
    "automation", "communication", "content", "ecc",
    "integrations", "knowledge", "meta", "ops", "personal"
]

CATEGORY_LABELS = {
    "automation": "Automation & AI Agents",
    "communication": "Communication",
    "content": "Content & Media",
    "ecc": "ECC (External Skill Collection)",
    "integrations": "Integrations",
    "knowledge": "Knowledge & Research",
    "meta": "Meta & Utility",
    "ops": "Operations & DevOps",
    "personal": "Personal & Lifestyle",
}

def extract_frontmatter(path):
    """Return (name, description) from a SKILL.md file."""
    with open(path, 'r') as f:
        content = f.read()
    # Match YAML frontmatter between --- delimiters
    m = re.match(r'^---\s*\n(.*?)\n(?:---|\.\.\.)', content, re.DOTALL)
    if not m:
        # Try without trailing delimiter
        m = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if m:
        yaml = m.group(1)
        name = None
        desc = None
        desc_lines = []
        in_desc = False
        desc_indent = None
        desc_block_scalar = False
        for line in yaml.split('\n'):
            if line.startswith('name:'):
                name = line.split(':', 1)[1].strip().strip('"\'')
            # Detect description start
            if line.startswith('description:'):
                rest = line.split(':', 1)[1]
                stripped = rest.strip()
                if stripped in ('>', '|', '>-', '|-', '>+', '|+'):
                    desc_block_scalar = True
                    in_desc = True
                    desc_indent = None
                    desc_lines = []
                elif stripped:
                    desc = stripped.strip('"\'')
                    in_desc = False
                else:
                    in_desc = True
                    desc_indent = None
                    desc_lines = []
                continue
            # Collect block scalar continuation lines
            if in_desc and desc_block_scalar:
                if desc_indent is None and line.strip():
                    desc_indent = len(line) - len(line.lstrip())
                    desc_lines.append(line.strip())
                elif desc_indent is not None:
                    # Check if still indented enough
                    if line.strip() and (len(line) - len(line.lstrip()) >= desc_indent):
                        desc_lines.append(line.strip())
                    elif line.strip() == '':
                        continue  # blank lines in block scalar
                    else:
                        # Less indented = end of block scalar
                        desc = ' '.join(desc_lines)
                        in_desc = False
                        desc_block_scalar = False
        # Flush any remaining block scalar
        if in_desc and desc_lines:
            desc = ' '.join(desc_lines)
        return (name, desc or name)
    # Fallback: no YAML frontmatter — use H1 heading as name, first non-empty line as desc
    lines = content.strip().split('\n')
    name = None
    desc = None
    for i, line in enumerate(lines):
        if line.startswith('# ') and not name:
            name = line[2:].strip()
            # Strip trailing " Skill", " skill" etc for a cleaner name
            name = re.sub(r'\s+Skill$', '', name, flags=re.IGNORECASE)
            name = name.lower().replace(' ', '-')
            # Use first non-heading paragraph as description
            for j in range(i+1, min(i+10, len(lines))):
                candidate = lines[j].strip()
                if candidate and not candidate.startswith('#'):
                    desc = candidate[:200]  # first 200 chars
                    break
            break
    return (name, desc or name)

def get_skill_rel_link(path):
    """Get the relative link for a skill: category/subdir1/subdir2/"""
    rel = os.path.relpath(path, SKILLS_DIR)
    parts = rel.split(os.sep)
    # parts is like ['automation', 'autonomous-ai-agents', 'claude-code', 'SKILL.md']
    # Return everything except the filename: automation/autonomous-ai-agents/claude-code/
    return '/'.join(parts[:-1]) + '/'

def main():
    # Collect skills by category
    skills_by_cat = {}
    for root, dirs, files in os.walk(SKILLS_DIR):
        # Skip INDEX.md files themselves, quarantine, private
        if 'INDEX.md' in files:
            files.remove('INDEX.md')  # don't treat INDEX as a skill
        for f in files:
            if f != 'SKILL.md':
                continue
            path = os.path.join(root, f)
            # Skip quarantine/private
            if '/quarantine/' in path or '/private/' in path:
                continue
            cat = get_skill_rel_link(path).split('/')[0]
            if cat not in CATEGORY_ORDER:
                continue
            name, desc = extract_frontmatter(path)
            if not name:
                continue
            # Get the relative link: category/subdir1/subdir2/
            rel_link = get_skill_rel_link(path)
            skills_by_cat.setdefault(cat, []).append((name, desc, rel_link))

    total = sum(len(s) for s in skills_by_cat.values())
    unique_names = set()
    for cat in skills_by_cat:
        for name, _, _ in skills_by_cat[cat]:
            unique_names.add(name)

    lines = []
    lines.append("# Appie Kit Skills Index")
    lines.append("")
    lines.append(f"**Production skills in appie-kit:** {total}")
    lines.append("")
    lines.append(f"**Unique skill names:** {len(unique_names)}")
    lines.append("")
    utc_now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines.append(f"_Regenerated {utc_now}_")
    lines.append("")
    lines.append("## Categories")
    lines.append("")
    for cat in CATEGORY_ORDER:
        count = len(skills_by_cat.get(cat, []))
        lines.append(f"- [{CATEGORY_LABELS[cat]}]({cat}/INDEX.md): {count} skills")
    lines.append("")
    lines.append("## Skills")
    lines.append("")

    for cat in CATEGORY_ORDER:
        skills = skills_by_cat.get(cat, [])
        if not skills:
            continue
        # Sort skills by name
        skills.sort(key=lambda x: x[0].lower())
        lines.append(f"### {cat} ({len(skills)})")
        lines.append("")
        for name, desc, link in skills:
            desc_clean = (desc or '').replace('\n', ' ').strip()
            lines.append(f"- [`{name}`]({link}): {desc_clean}")
        lines.append("")

    return '\n'.join(lines)

if __name__ == '__main__':
    output = main()
    print(output)