---
name: ashp
description: "Use Appie Secure Handshake Protocol patterns for authenticated inter-agent communication and secure Appie-family coordination."
version: 1.0.0
category: ops
---

# Appie Secure Handshake Protocol (ASHP)

*Inter-agent communication protocol for the Appie family*

## Overview

ASHP is a lightweight secure communication protocol that allows Appie instances to:
1. Authenticate each other via API key exchange
2. Send encrypted messages between instances
3. Establish secure tunnels for collaboration

## Protocol Version
- **Version:** 1.0
- **Status:** Production Ready

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Appie Family Network                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────┐    ASHP Handshake    ┌─────────┐              │
│  │ Appie-1 │ ◄──────────────────► │ Appie-2 │              │
│  │   (Mac) │    API Key Exchange   │   (DO)  │              │
│  └─────────┘                       └─────────┘              │
│       │                                 │                    │
│       └───────────── ASHP ──────────────┘                    │
│                     Tunnel                                   │
└─────────────────────────────────────────────────────────────┘
```

## API Key Configuration

Each Appie instance has a unique API key configured in `~/.openclaw/openclaw.json`:

```json
{
  "ashp": {
    "api_key": "<agent-api-key>",
    "allowed_keys": [
      "<peer-api-key-1>",
      "<peer-api-key-2>"
    ],
    "timeout_ms": 30000
  }
}
```

## Handshake Flow

```
Step 1: Appie-1 initiates
  → POST /api/ashp/handshake
  → { "to": "appie-2", "from": "appie-1", "key_id": "<key-id>" }

Step 2: Appie-2 validates and responds
  → Returns: { "status": "accepted", "session_id": "sess_abc123" }

Step 3: Appie-1 confirms
  → POST /api/ashp/confirm
  → { "session_id": "sess_abc123", "signature": "sha256(...)" }

Step 4: Secure tunnel established
  → All subsequent messages include session_id
```

## API Endpoints

### POST /api/ashp/handshake
Initiate secure handshake with another Appie.

**Request:**
```json
{
  "to": "appie-2",
  "from": "appie-1",
  "key_id": "<key-id>"
}
```

**Response:**
```json
{
  "status": "accepted" | "denied",
  "session_id": "sess_xyz789",
  "expires_at": "2026-02-15T08:00:00Z"
}
```

### POST /api/ashp/confirm
Confirm handshake and establish session.

**Request:**
```json
{
  "session_id": "sess_xyz789",
  "signature": "sha256(session_id + <api-key>)"
}
```

### POST /api/ashp/message
Send encrypted message through established session.

**Request:**
```json
{
  "session_id": "sess_xyz789",
  "to": "appie-2",
  "message": "base64_encrypted_message",
  "timestamp": "2026-02-15T01:00:00Z"
}
```

### POST /api/ashp/close
Close active session.

**Request:**
```json
{
  "session_id": "sess_xyz789"
}
```

## Usage Example

```bash
# Initiate handshake
curl -X POST "http://localhost:8080/api/ashp/handshake" \
  -H "Content-Type: application/json" \
  -d '{"to":"appie-2","from":"appie-1","key_id":"appie-1-abc123"}'

# Send secure message
curl -X POST "http://localhost:8080/api/ashp/message" \
  -H "Content-Type: application/json" \
  -d '{"session_id":"sess_xyz789","to":"appie-2","message":"SGVsbG8gQXBwaWUh"}'
```

## Security Features

1. **API Key Validation** - Each message validated against allowed keys
2. **Session Management** - Sessions expire after 30 minutes
3. **Message Signing** - All messages signed with session key
4. **Audit Logging** - All handshakes logged for security

## Configuration

Add to `~/.openclaw/openclaw.json`:

```json
{
  "ashp": {
    "api_key": "your-appie-key-here",
    "allowed_keys": ["list", "of", "allowed", "keys"],
    "timeout_ms": 30000,
    "log_file": "/Users/seyed/.openclaw/logs/ashp.log"
  }
}
```

## Skill Integration

This protocol is available as a OpenClaw skill:

```bash
# Enable ASHP skill
openclaw skill enable ashp

# View handshake status
openclaw ashp status

# List active sessions
openclaw ashp sessions
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Handshake rejected | Verify API key is in allowed_keys of recipient |
| Session expired | Re-initiate handshake |
| Message failed | Check session is still active |

## File Locations

- **Skill:** `/Users/seyed/clawd/skills/ashp/`
- **Config:** `~/.openclaw/openclaw.json` → `ashp` section
- **Logs:** `~/.openclaw/logs/ashp.log`