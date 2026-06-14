---
name: agent-fleet-operations
description: "Operate Hermes/Appie-style agent fleets across machines: provision remote hosts, validate transport/auth, refresh knowledge packs, and recover provider or gateway runtime failures."
version: 1.0.0
author: Appie
license: MIT
metadata:
  hermes:
    tags: [devops, hermes-agent, agent-fleet, provisioning, gateway, providers, ssh, tailscale]
    related_skills: [hermes-agent, healthcheck, webhook-subscriptions]
---

# Agent Fleet Operations

Use this skill when operating Hermes/Appie-style agents across one or more machines: bootstrapping a new node, refreshing an Appie kit or knowledge pack, validating remote access, troubleshooting remote deploy failures, or recovering Hermes provider/gateway failures that prevent the agent from answering.

This is an umbrella skill. It absorbs the former `fleet-provisioning` and `hermes-provider-troubleshooting` skills. Load the protected `hermes-agent` skill first for authoritative Hermes CLI/config commands, then use this skill for fleet-level operational sequence and Appie/Seyed-specific lessons.

## Core operating model

Treat each layer as a separate gate:

1. **Identity and ownership**: which machine, account, Tailnet name/IP, and runtime profile are in scope?
2. **Network visibility**: can the node be reached on the overlay or public network?
3. **Transport access**: are SSH/VNC/HTTP control-plane ports open independently?
4. **Authentication**: does the intended user/key/token actually work?
5. **Configuration**: does Hermes point at the intended provider/model/runtime paths?
6. **Credentials and quota**: are provider credentials fresh, scoped to this node, and not exhausted?
7. **Runtime readiness**: is the gateway/service restarted and answering after changes?
8. **Artifact verification**: did the files, knowledge pack, persona, or service entrypoint land where expected?

Do not collapse these gates. A node can answer Tailscale ping while refusing SSH. SSH port 22 can be open while public-key auth fails. Hermes config can be correct while OAuth is stale or quota is exhausted.

## Remote provisioning workflow

Use for bootstrapping or refreshing remote agent hosts, Macs, VPS nodes, or Tailnet-hosted agents.

1. Confirm target identity, owner, and intended user.
2. Check Tailnet or network reachability.
3. Check each required control-plane port separately.
4. Prove shell access with a harmless command before running deploy scripts.
5. Run deploy scripts in dry-run mode if available.
6. Only then copy files, rsync knowledge packs, install services, or write persona/runtime files.
7. Verify installed files and runtime entrypoints on the target.

Good commands:

```bash
tailscale ping -c 3 <host>
nc -z -G 3 <host> 22
nc -z -G 3 <host> 5900
ssh -o BatchMode=yes -o ConnectTimeout=10 <user>@<host> 'whoami && hostname'
ssh -vvv -o BatchMode=yes -o ConnectTimeout=10 <user>@<host> 'whoami'
```

### Remote Mac / Leona lessons

For remote Mac deployments, never trust a deploy script's default login until `ssh ... 'whoami'` proves it. In the Leona Appie-kit case, Tailnet and port 22 were healthy, but the script failed until the SSH user was corrected to `zahedi` via `LEONA_USER=zahedi`.

See:

- `references/cross-machine-provisioning.md`
- `references/ssh-auth-denied-session.md`
- `references/leona-appie-kit-sync.md`

## Hermes provider and gateway troubleshooting workflow

Use when Hermes Agent or its gateway fails because of provider/model/authentication issues: `Provider authentication failed`, OAuth refresh errors, HTTP 401/403/429, bad model names, fallback routing surprises, auxiliary-model failures, or gateway shutdowns after model changes.

### Fast diagnostic sequence

1. **Check config first**
   - Read `~/.hermes/config.yaml`.
   - Confirm `model.provider`, `model.default`, provider-specific `base_url`, fallback providers, and auxiliary model/provider settings.

2. **Check auth state second**
   - Read `~/.hermes/auth.json`.
   - Inspect provider entries, credential pool state, and `last_auth_error`.
   - Never paste full tokens in chat or logs.

3. **Check gateway/provider logs third**
   - Inspect `~/.hermes/logs/gateway.error.log`, `gateway.log`, and `errors.log` for provider name, model name, HTTP status, retry count, `last_auth_error`, and fallback messages.

4. **Classify the failure**
   - Config wrong: update via `hermes config set` or a targeted edit.
   - OAuth stale/reused: run provider login, then restart gateway.
   - Quota/429: choose a fallback or lower-cost model until quota resets.
   - Gateway stale after valid config/auth: restart gateway.
   - Auxiliary-only failure: fix `auxiliary.*`, not the primary model.

5. **Verify after changes**
   - Restart the gateway after config/auth changes.
   - Confirm the active provider/model in a fresh session or logs.

### OpenAI Codex OAuth `refresh_token_reused`

Hermes can be configured correctly for `openai-codex` while still failing because the OAuth refresh token was consumed by another Codex client.

Durable signal in `~/.hermes/auth.json`:

```text
last_auth_error.code = refresh_token_reused
message = Codex refresh token was already consumed by another client
relogin_required = true
```

Recovery on the target machine:

```bash
codex
hermes auth
hermes gateway restart
```

During `hermes auth`, choose `openai-codex` if prompted. This may require human browser/device approval and cannot always be completed silently by the agent.

See `references/openai-codex-refresh-token-reused.md`.

## Reporting standard

When reporting operational blockers:

- State which gate succeeded and which gate failed.
- Say whether config is already correct before asking for config changes.
- Name the blocker precisely: network, port, SSH auth, remote username, provider auth, quota, model name, auxiliary model, or gateway runtime.
- Give exact next commands only when human action is required.
- Do not paste secrets, tokens, or credential values.
- Avoid tool-call play-by-play.

Good:

```text
Config is already pointed at openai-codex / gpt-5.5. The blocker is OAuth: auth.json shows refresh_token_reused. Run codex, then hermes auth, choose openai-codex, then hermes gateway restart.
```

Good:

```text
The node is visible on Tailnet and port 22 is open, but SSH auth is failing for the default user. Prove the correct login with ssh '<user>@<host> whoami' before rerunning deploy.
```

## Pitfalls

- Do not assume `tailscale ping` implies SSH, VNC, or HTTP readiness.
- Do not assume open SSH port implies usable shell auth.
- Do not run deploy/copy/install steps until the login has been proven with `whoami`.
- Do not overwrite local memory stores, secrets, or runtime state unless the deploy explicitly calls for it.
- Do not rewrite Hermes config just because a provider failed; classify auth/quota/runtime first.
- Do not claim a provider is unsupported just because the current token is stale.
- Do not copy provider credentials between machines or agents. Authenticate the target node.
- If terminal execution is interrupted repeatedly, use file/skill/log inspection where possible and report the external OAuth or access blocker instead of retrying the same failing command loop.

## Verification checklist

- [ ] Target host, user, and profile are explicit.
- [ ] Network reachability and control-plane ports were checked separately.
- [ ] SSH/auth was proven with a harmless command before deploy.
- [ ] Deploy or sync ran only after prerequisite gates passed.
- [ ] Installed files/runtime entrypoints were verified on the target.
- [ ] Hermes config was inspected before changing providers/models.
- [ ] Auth/log evidence was inspected before labeling a provider failure.
- [ ] Gateway was restarted after config/auth changes.
- [ ] Final report identifies the failing gate without leaking secrets.
