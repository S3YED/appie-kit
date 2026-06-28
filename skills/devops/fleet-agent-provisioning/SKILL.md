---
name: fleet-agent-provisioning
description: Provision a remote Hermes agent with the Appie Kit (skills, workspace, SOUL.md preservation, knowledge doc transfer, and verification). Use when setting up a new fleet member, reinstalling a corrupted agent, or bulk-updating skills across the fleet.
---

# Fleet Agent Provisioning — Appie Kit Install + Knowledge Transfer

## When to Use

- Seyed says "set up X with the Appie Kit" or "give Y all the skills"
- A new Hermes agent needs the full skill library
- An existing agent needs skills refreshed from the canonical Appie Kit repo
- Post-migration skill restauration

## Prerequisites

- SSH key access to the target host (check fleet scan first)
- Appie Kit repo exists on appie-1 at `/Users/appie/clawd/projects/appie-kit/`
- Agent's Hermes skills directory is at `~/.hermes/skills/`

## Workflow

### 1. Clone Appie Kit on Target

```bash
ssh -o StrictHostKeyChecking=no <target>.tail61f54b.ts.net 'cd ~ && git clone https://github.com/S3YED/appie-kit.git'
```

### 2. Run Install Script

```bash
ssh -o StrictHostKeyChecking=no <target>.tail61f54b.ts.net 'cd ~/appie-kit && ./install.sh ~/.hermes/'
```

The install.sh copies skills to `~/.hermes/skills/`, workspace templates to `~/.hermes/`, and creates `.env.secrets`.

### 3. Verify SOUL.md Is Intact

The install script copies workspace template files (SOUL.md, USER.md, etc.). If the agent already had custom SOUL.md, **verify it was preserved**:

```bash
ssh <target> 'head -5 ~/.hermes/SOUL.md'
```

If overwritten, restore from backup or rewrite with agent's identity.

### 4. Verify Skill Count

```bash
ssh <target> 'find ~/.hermes/skills -name "SKILL.md" | wc -l'
```

Expected: ~994+ (grows as Appie Kit expands). If significantly lower, re-run install.

### 5. Transfer Knowledge Documents

Create docs locally, then SCP to agent:

```bash
scp /tmp/<doc>.md <target>.tail61f54b.ts.net:~/<path>/
```

Create directories on target if needed:
```bash
ssh <target> 'mkdir -p ~/appie-brain/knowledge/frameworks'
```

### 6. Verify Transfer

```bash
ssh <target> 'head -3 ~/<path>/<doc>.md && wc -l ~/<path>/<doc>.md'
```

### 7. Knowledge Infrastructure (Neo4j + Ollama + Pipeline)

For agents that need persistent memory beyond skills and docs, provision a local knowledge graph + vector search stack.

```bash
# Install Docker
ssh <target> 'curl -fsSL https://get.docker.com | sh'

# Start Neo4j with random password
PASS=$(openssl rand -base64 18 | tr -dc a-zA-Z0-9 | head -c 20)
ssh <target> "docker run -d --name neo4j-memory --restart unless-stopped \\
  -p 7474:7474 -p 7687:7687 \\
  -e 'NEO4J_AUTH=*** \\
  -e NEO4J_PLUGINS='[\\\"apoc\\\"]' \\
  -v ~/neo4j-data:/data neo4j:5-community"
# Write $PASS to target's .env.secrets as NEO4J_PASSWORD

# Install Ollama + embedding model
ssh <target> "curl -fsSL https://ollama.com/install.sh | sh && ollama pull bge-m3"

# Create venv and install deps (PEP 668-safe)
ssh <target> "python3 -m venv ~/knowledge-env && \
  ~/knowledge-env/bin/pip install numpy pymupdf neo4j ollama"

# Create pipeline directory and SCP scripts
ssh <target> 'mkdir -p ~/clawd/projects/knowledge-pipeline/.data'

# Templates are in the fleet-agent-provisioning skill at templates/ingest.py and templates/query.py
# Copy and upload them to the target
scp <skill_dir>/templates/ingest.py <target>:~/clawd/projects/knowledge-pipeline/
scp <skill_dir>/templates/query.py <target>:~/clawd/projects/knowledge-pipeline/

# Create wrapper command (avoids secret-masking in heredoc — write via Python)
ssh <target> 'python3 -c "
import os
with open(os.path.expanduser(\\\"~/.hermes/.env.secrets\\\")) as f:
    for line in f:
        if line.startswith(\\\"NEO4J_PASSWORD=***                pw = line.strip().split(\\\"=\\", 1)[1]
                break
script = open(\\\"/dev/stdin\\\").read().replace(\\\"ENV_PASSWORD_VAR\\\", pw)
with open(\\\"/usr/local/bin/memory-search\\\", \\\"w\\\") as f: f.write(script)
os.chmod(\\\"/usr/local/bin/memory-search\\\", 0o755)
" << '\"'\"'SCRIPT'\"'\"'
#!/bin/bash
source ~/knowledge-env/bin/activate 2>/dev/null
export NEO4J_PASSWORD="ENV_PASSWORD_VAR"
CMD="${1:-}"; shift 2>/dev/null || true
case "$CMD" in
  search|query) python3 ~/clawd/projects/knowledge-pipeline/query.py "$@" ;;
  ingest) python3 ~/clawd/projects/knowledge-pipeline/ingest.py "$@" ;;
  stats|--stats) python3 ~/clawd/projects/knowledge-pipeline/query.py --stats ;;
  graph|--graph) python3 ~/clawd/projects/knowledge-pipeline/query.py --graph ;;
  *) python3 ~/clawd/projects/knowledge-pipeline/query.py "$CMD" "$@" ;;
esac
SCRIPT'

# Seed initial knowledge
ssh <target> 'source ~/knowledge-env/bin/activate && \
  python3 ~/clawd/projects/knowledge-pipeline/ingest.py ~/.hermes/SOUL.md --tenant <user>'

# Restart gateway
ssh <target> 'systemctl restart hermes 2>/dev/null || pkill -f hermes_cli.main.gateway'
```

### 8. Verify Knowledge Infrastructure

```bash
ssh <target> 'docker ps --filter name=neo4j --format "{{.Names}} {{.Status}}"'
# → neo4j-memory Up

ssh <target> 'ollama list'
# → bge-m3:latest

ssh <target> 'memory-search stats'
# → Knowledge Graph Stats: Documents: N, Chunks: M
```

## Pitfalls

- **SOUL.md overwrite**: The install.sh copies workspace template files but checks for existing files. It should preserve custom SOUL.md. Always verify.
- **SSH host key**: First-time SSH to a new host prompts for host key verification. Use `-o StrictHostKeyChecking=no` only for trusted tailnet hosts.
- **Disk space**: Appie Kit is ~29MB for skills. Check `df -h` on target before cloning.
- **Git clone fails**: If the target has no git credentials, HTTPS clone works for public repos. If repo is private, ensure `gh` is authenticated or use a token.
- **Interrupted install**: If install.sh times out mid-way, running it again is safe (idempotent for skills, prompt to overwrite workspace files).
- **Different Hermes version**: Skills are framework-agnostic (OpenClaw + Hermes compatible). No version conflicts expected.
- **Docker not available**: If Docker isn't installed, the `get.docker.com` script works on Ubuntu/Debian Hetzner VPS. Verify `docker --version` afterwards.
- **Neo4j auth password**: The `NEO4J_AUTH` env var must be `neo4j/<password>`. Setting it after first start requires clearing `~/neo4j-data/` and recreating the container. Always set on first run.
- **Wrapper script secrets**: The `memory-search` wrapper needs NEO4J_PASSWORD exported. Writing it via heredoc on SSH risks shell expansion. Two reliable approaches: (1) write via Python with inline read from .env.secrets, (2) have the wrapper source .env.secrets directly and parse the right line.
- **Gateway restart kills SSH**: If Hermes gateway is the SSH session's parent process, `systemctl restart hermes` may drop the connection. After a few seconds, reconnect and verify.
- **Content filter masks `***  When writing wrapper scripts via heredoc on SSH that read secrets (e.g. `$(grep NEO4J_PASSWORD .env)`), the shell output filter substitutes the `***  with literal asterisks, breaking the script. Solution: write the wrapper via Python ON the target machine, reading the password from `.env.secrets` and substituting inline into a template string. See section 7 for the Python-on-target pattern.
- **PEP 668**: Ubuntu 24+ blocks `pip install --system`. Always use a venv. `python3 -m venv ~/knowledge-env` then activate before install.

## Verification Checklist

- [ ] Appie Kit cloned on target
- [ ] install.sh completed without errors
- [ ] SOUL.md preserved with agent identity
- [ ] Skill count matches expected (~994)
- [ ] Knowledge documents transferred and readable
- [ ] `.env.secrets` created (user fills in keys)
- [ ] Docker + Neo4j running (`docker ps`)
- [ ] Ollama + bge-m3 installed (`ollama list`)
- [ ] Knowledge pipeline scripts deployed (`memory-search stats`)
- [ ] Initial knowledge seeded (SOUL.md, MEMORY.md, etc.)
- [ ] Gateway restarted and responding
- [ ] MEMORY.md updated on target with upgrade info
- [ ] Upgrade notification sent to user (if Telegram token + chat ID available)

### 9. Post-Provisioning Notification

After provisioning, the agent needs to know what changed, and the user needs to be notified.

**9a. Write agent's MEMORY.md** — so the agent reads it at its next session start:

```bash
ssh <target> 'cat >> ~/.hermes/MEMORY.md << '"'"'EOF'"'"'

## YYYY-MM-DD: Provisioned by Appie-3

### What was installed
- Neo4j 5.26.27 (localhost:7687)
- Ollama bge-m3 (localhost:11434)
- Knowledge pipeline at ~/clawd/projects/knowledge-pipeline/
- memory-search wrapper command
- Appie Kit v4.5 (994 skills)

### To do
1. Send upgrade message to user
2. Set up nightly cron
3. Fill in USER.md
4. Explore new skills
EOF'
```

**9b. Send Telegram notification to user** (if agent has a Telegram token and user chat ID is known):

```bash
ssh <target> "python3 -c '
import json, urllib.request
with open(\"/root/.hermes/.env.secrets\") as f:
    for line in f:
        if \"TELEGRAM_BOT_TOKEN=*** in line:
            token = line.split(\"=\", 1)[1].strip()
            break
msg = \"Your AI agent got upgraded! 994 skills, Neo4j knowledge graph, local embeddings, DOE loop.\"
url = \"https://api.telegram.org/bot{}/sendMessage\".format(token)
data = json.dumps({\"chat_id\": <USER_CHAT_ID>, \"text\": msg}).encode()
req = urllib.request.Request(url, data=data, headers={\"Content-Type\": \"application/json\"})
urllib.request.urlopen(req, timeout=10)
print(\"Sent\")
'"
```

### 10. Verification Checklist (final)