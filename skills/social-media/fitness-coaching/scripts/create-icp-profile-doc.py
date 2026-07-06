#!/usr/bin/env python3
"""
Create a structured Google Doc with country ICP profiles for a fitness coaching client.

Usage:
  python3 create-icp-profile-doc.py

Requires: gws tokens at /root/.config/gws/tokens.json (OAuth2 with Docs/Drive scopes)

Process:
  1. Read stored tokens
  2. Create a new Google Doc
  3. Populate with country profiles using batchUpdate insertText
  4. Print the doc URL

Each profile section: country flag/name, target, the person, primary pain,
sub-pains, verbatim pain language, testimonial template, CTA formulas, headline angles.

Token refresh pattern: if 401, generate auth URL via:
  timeout 10 gws-wrapper auth login --full | grep -oP 'https://accounts\.google\.com[^ ]*'
User approves, pastes redirect URL. Exchange code for tokens.

Pitfall: insertText indices must be monotonically increasing (insert from end to start).
Pitfall: The GWS --output flag requires relative paths, not absolute.
"""

import json
import urllib.request
import urllib.parse

DOC_TITLE = "THE CREED — ICP Ad Profiles"

def make_doc(token):
    """Create the Google Doc and return its ID."""
    body = {"title": DOC_TITLE}
    req = urllib.request.Request(
        "https://docs.googleapis.com/v1/documents",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
    return result["documentId"]

def insert_requests(doc_id, token, requests):
    """Send batchUpdate to the document."""
    url = f"https://docs.googleapis.com/v1/documents/{doc_id}:batchUpdate"
    body = json.dumps({"requests": requests})
    req = urllib.request.Request(url, data=body.encode(), headers={
        "Authorization": f"Bearer {token}", "Content-Type": "application/json"
    })
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

def build_icp_content():
    """Build the list of insertText requests (in reverse order for correct indexing)."""
    inserts = []

    def insert(text):
        inserts.append({"insertText": {"location": {"index": 1}, "text": text}})

    # --- Template: structure sections per country ---

    # You can extend this with additional countries by following the same pattern.
    # Each country needs: name, target, person description, primary pain,
    # sub-pains, verbatim pain language, testimonial template + example,
    # CTA formulas, headline angles.

    return inserts

if __name__ == "__main__":
    with open("/root/.config/gws/tokens.json") as f:
        t = json.load(f)
    token = t["access_token"]

    doc_id = make_doc(token)
    print(f"Created doc: https://docs.google.com/document/d/{doc_id}/edit")

    # Populate
    requests = build_icp_content()
    if requests:
        insert_requests(doc_id, token, requests)
        print(f"Inserted {len(requests)} content blocks")
