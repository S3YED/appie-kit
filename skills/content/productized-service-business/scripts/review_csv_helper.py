#!/usr/bin/env python3
"""Review to Revenue CSV helper.

Usage:
  python3 review_csv_helper.py reviews.csv --text-col review --rating-col rating

Prepares review data for Customer Voice Conversion Audits:
- normalizes review text
- counts recurring words
- highlights likely signal categories
- writes a markdown summary for audit workflow
"""
from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from pathlib import Path

STOPWORDS = set("""
de het een en of in op voor van met aan is zijn was waren ik je jij u wij ze zij dit dat deze die
te niet wel heel erg goed slecht prima mooi snel langzaam naar bij als om maar ook meer minder
""".split())

SIGNAL_PATTERNS = {
    "maat_pasvorm": r"\b(maat|valt|pasvorm|klein|groot|ruim|strak|lengte)\b",
    "levering": r"\b(levering|bezorg|verzend|pakket|snel|laat|vertraging)\b",
    "kwaliteit": r"\b(kwaliteit|stof|materiaal|stevig|kapot|defect|duurzaam)\b",
    "service": r"\b(service|klantenservice|contact|antwoord|geholpen|retour)\b",
    "prijs_waarde": r"\b(prijs|duur|goedkoop|waarde|geld|aanbieding)\b",
    "installatie_gebruik": r"\b(installeren|montage|gebruik|handleiding|duidelijk|makkelijk|lastig)\b",
    "twijfel": r"\b(twijfel|verwacht|onduidelijk|jammer|helaas|probleem|nadeel)\b",
}


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def words(text: str):
    for w in re.findall(r"[a-zA-ZÀ-ÿ0-9]{3,}", text.lower()):
        if w not in STOPWORDS:
            yield w


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path")
    ap.add_argument("--text-col", default="review")
    ap.add_argument("--rating-col", default="rating")
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    path = Path(args.csv_path)
    rows = []
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = clean(row.get(args.text_col, ""))
            if text:
                rows.append({"text": text, "rating": clean(row.get(args.rating_col, "")), **row})

    word_counts = Counter()
    signal_counts = Counter()
    examples = {k: [] for k in SIGNAL_PATTERNS}

    for row in rows:
        text = row["text"]
        word_counts.update(words(text))
        for label, pattern in SIGNAL_PATTERNS.items():
            if re.search(pattern, text, flags=re.I):
                signal_counts[label] += 1
                if len(examples[label]) < 5:
                    examples[label].append(text[:260])

    out = []
    out.append(f"# Review CSV Summary — {path.name}\n")
    out.append(f"Aantal reviews: {len(rows)}\n")

    ratings = Counter(row["rating"] for row in rows if row["rating"])
    if ratings:
        out.append("## Ratings\n")
        for rating, count in ratings.most_common():
            out.append(f"- {rating}: {count}")
        out.append("")

    out.append("## Meest voorkomende woorden\n")
    for word, count in word_counts.most_common(40):
        out.append(f"- {word}: {count}")
    out.append("")

    out.append("## Signaalgebieden\n")
    for label, count in signal_counts.most_common():
        out.append(f"### {label} — {count}")
        for ex in examples[label]:
            out.append(f"> {ex}")
        out.append("")

    out.append("## Volgende analysevragen\n")
    out.append("- Welke woorden bewijzen koopredenen?")
    out.append("- Welke twijfels moeten op productpagina/FAQ/checkout opgelost worden?")
    out.append("- Welke claims kunnen als trustblok bij de CTA?")
    out.append("- Welke klachten verlagen conversie of verhogen retouren?")

    output = "\n".join(out)
    out_path = Path(args.out) if args.out else path.with_suffix(".review-summary.md")
    out_path.write_text(output, encoding="utf-8")
    print(out_path)

if __name__ == "__main__":
    main()
