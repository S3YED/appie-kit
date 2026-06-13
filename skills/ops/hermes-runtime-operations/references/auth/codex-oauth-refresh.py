#!/usr/bin/env python3
"""
Codex OAuth device-code flow: poll → exchange → save to auth.json.

Usage:
  1. First, request a device code:
     curl -s https://auth.openai.com/api/accounts/deviceauth/usercode \
       -X POST -H "Content-Type: application/json" \
       -d '{"client_id":"app_EMoamEEZ73f0CkXaXp7hrann"}' | python3 -m json.tool

  2. Give the user_code to the user (they visit https://auth.openai.com/codex/device)

  3. Edit DEVICE_AUTH_ID and USER_CODE below, then run:
     python3 -u codex-oauth-refresh.py

Outputs "OK:<entry_id>" on success, "TIMEOUT" if user didn't authorize within 14 min,
or "ERROR:..." on other failures.
"""

import httpx, json, sys, time, os, uuid
from datetime import datetime, timezone

# ── EDIT THESE ──────────────────────────────────────────────
DEVICE_AUTH_ID = "deviceauth_PLACEHOLDER"
USER_CODE = "XXXX-XXXXX"
# ────────────────────────────────────────────────────────────

ISSUER = "https://auth.openai.com"
CLIENT_ID = "app_EMoamEEZ73f0CkXaXp7hrann"
TOKEN_URL = "https://auth.openai.com/oauth/token"
AUTH_PATH = os.path.expanduser("~/.hermes/auth.json")

# ── Poll ────────────────────────────────────────────────────
code_resp = None
with httpx.Client(timeout=httpx.Timeout(15.0)) as client:
    for _ in range(168):  # 14 min at 5s intervals
        time.sleep(5)
        poll = client.post(
            f"{ISSUER}/api/accounts/deviceauth/token",
            json={"device_auth_id": DEVICE_AUTH_ID, "user_code": USER_CODE},
            headers={"Content-Type": "application/json"},
        )
        if poll.status_code == 200:
            code_resp = poll.json()
            break
        elif poll.status_code not in {403, 404}:
            print(f"ERROR: Poll returned {poll.status_code}: {poll.text}", flush=True)
            sys.exit(1)

if code_resp is None:
    print("TIMEOUT", flush=True)
    sys.exit(1)

# ── Exchange ────────────────────────────────────────────────
auth_code = code_resp["authorization_code"]
code_verifier = code_resp["code_verifier"]

token_resp = client.post(TOKEN_URL, data={
    "grant_type": "authorization_code",
    "code": auth_code,
    "redirect_uri": f"{ISSUER}/deviceauth/callback",
    "client_id": CLIENT_ID,
    "code_verifier": code_verifier,
}, headers={"Content-Type": "application/x-www-form-urlencoded"})

if token_resp.status_code != 200:
    print(f"ERROR: Token exchange returned {token_resp.status_code}: {token_resp.text}", flush=True)
    sys.exit(1)

tokens = token_resp.json()
access_token = tokens["access_token"]
refresh_token = tokens.get("refresh_token", "")

# ── Save to auth.json (both layers) ─────────────────────────
with open(AUTH_PATH) as f:
    auth_data = json.load(f)

# Layer 1: provider state
auth_data.setdefault("providers", {})["openai-codex"] = {
    "tokens": {"access_token": access_token, "refresh_token": refresh_token},
    "last_refresh": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    "auth_mode": "chatgpt",
}

# Layer 2: credential pool - remove old device_code entries, add fresh one
entry_id = uuid.uuid4().hex[:6]
auth_data.setdefault("credential_pool", {}).setdefault("openai-codex", [])

# Purge entries seeded from old/stale device codes
auth_data["credential_pool"]["openai-codex"] = [
    e for e in auth_data["credential_pool"]["openai-codex"]
    if e.get("source") not in ("device_code", "manual:device_code")
]

auth_data["credential_pool"]["openai-codex"].append({
    "id": entry_id,
    "label": f"codex-oauth-{entry_id}",
    "auth_type": "oauth",
    "priority": 0,
    "source": "manual:device_code",
    "access_token": access_token,
    "refresh_token": refresh_token,
    "last_status": "ok",
    "last_status_at": None,
    "last_error_code": None,
    "last_error_reason": None,
    "last_error_message": None,
    "last_error_reset_at": None,
    "base_url": "https://chatgpt.com/backend-api/codex",
    "last_refresh": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    "request_count": 0,
})

auth_data["updated_at"] = datetime.now(timezone.utc).isoformat()
auth_data["active_provider"] = "openai-codex"

with open(AUTH_PATH, "w") as f:
    json.dump(auth_data, f, indent=2)

print(f"OK:{entry_id}", flush=True)