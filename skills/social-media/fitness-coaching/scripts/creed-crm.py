#!/usr/bin/env python3
"""Creed Giveaway CRM — tracks every lead through the funnel
Usage:
  python3 creed-crm.py import          # Import new leads from main database
  python3 creed-crm.py status          # Show current status and next actions
  python3 creed-crm.py update <email> <status> [notes]  # Update a lead
"""
import json
import os
from datetime import datetime, timezone

DB_PATH = "/root/creed-crm.json"

STATUSES = [
    "entered", "welcomed", "replied", "triage_booked",
    "triage_done", "winner", "sales_booked", "converted", "lost",
]

def load():
    if os.path.exists(DB_PATH):
        with open(DB_PATH) as f:
            return json.load(f)
    return []

def save(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=2)

def import_from_leads():
    with open("/root/leads-database.json") as f:
        leads = json.load(f)
    crm = load()
    existing_emails = {l["email"] for l in crm if l.get("email")}
    count = 0
    for lead in leads:
        email = lead.get("email", "")
        if email in existing_emails or not email or email == "—":
            continue
        crm.append({
            "name": lead.get("name", "—"),
            "email": email,
            "phone": lead.get("phone", ""),
            "commitment": lead.get("commitment_score"),
            "situation": lead.get("situation_answer", ""),
            "vision": lead.get("vision_answer", ""),
            "source": "giveaway",
            "status": "entered",
            "triage_call_notes": "",
            "sales_call_notes": "",
            "next_action": "Send welcome message",
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "entry_date": lead.get("submitted_at", ""),
        })
        existing_emails.add(email)
        count += 1
    save(crm)
    return count

def summary():
    data = load()
    counts = {s: 0 for s in STATUSES}
    for l in data:
        st = l.get("status", "entered")
        counts[st] = counts.get(st, 0) + 1
    print(f"Total leads: {len(data)}")
    for s in STATUSES:
        label = s.replace("_", " ").title()
        icon = {"entered": "🔴", "welcomed": "🟡", "replied": "🟢",
                "triage_booked": "🔵", "triage_done": "🟣", "converted": "💰",
                "lost": "⚪", "winner": "🏆", "sales_booked": "📞"}.get(s, "•")
        print(f"  {icon} {label}: {counts.get(s, 0)}")
    print("\nNEXT ACTIONS:")
    for l in data:
        if l.get("status") == "entered":
            print(f"  🔴 Send welcome: {l['name']} - {l['email']}")
        elif l.get("status") == "welcomed":
            print(f"  🟡 Waiting for reply: {l['name']} - {l['email']}")
        elif l.get("status") == "replied":
            print(f"  🟢 Book triage: {l['name']} - {l['email']}")
        elif l.get("status") == "triage_booked":
            print(f"  🔵 Triage call pending: {l['name']} - {l['email']}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "import":
        c = import_from_leads()
        print(f"Imported {c} new leads into CRM")
    elif len(sys.argv) > 2 and sys.argv[1] == "update":
        email = sys.argv[2]
        data = load()
        for l in data:
            if l.get("email") == email:
                l["status"] = sys.argv[3] if len(sys.argv) > 3 else l["status"]
                if len(sys.argv) > 4:
                    l["triage_call_notes"] = sys.argv[4]
                l["last_updated"] = datetime.now(timezone.utc).isoformat()
                save(data)
                print(f"Updated {l['name']} → {l['status']}")
                break
        else:
            print(f"Lead {email} not found")
    else:
        summary()