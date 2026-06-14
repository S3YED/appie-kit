# Ops - 23 skills

Infrastructure, DevOps, git, fleet operations, security hardening, deployment, and maintenance.

## Skills

- [`1password`](1password/): Set up and use 1Password CLI (op). Use when installing the CLI, enabling desktop app integration, signing in (single or multi-account), or reading/injecting/running secrets via op.
- [`agent-fleet-operations`](agent-fleet-operations/): Operate Hermes-style agent fleets across machines: provision remote hosts, validate transport/auth, refresh knowledge packs, and recover provider or gateway runtime failures.
- [`appie-self-maintenance`](appie-self-maintenance/): Daily healthcheck and low-risk maintenance for a Hermes/OpenClaw agent host.
- [`ashp`](ashp/): Use Appie Secure Handshake Protocol patterns for authenticated inter-agent communication and secure Appie-family coordination.
- [`camsnap`](camsnap/): Capture frames or clips from RTSP/ONVIF cameras.
- [`client-bot-security`](client-bot-security/): Full-spectrum security audit for client Telegram bots across a multi-gateway fleet (Hermes + OpenClaw). Covers bot inventory & topology mapping, token provisioning security, SSH key hygiene, authorized_keys audit, secrets map documentation, and bot lifecycle management (free→assigned→active→retired).
- [`debugging-hermes-tui-commands`](debugging-hermes-tui-commands/): Debug Hermes TUI slash commands: Python, gateway, Ink UI.
- [`digital-ocean`](digital-ocean/): Manage Digital Ocean droplets, domains, and infrastructure via DO API.
- [`fleet-infra-fixes`](fleet-infra-fixes/): Resolve recurring Appie fleet infrastructure issues including Node/Homebrew breakage, pnpm install blockers, deploy keys, secrets, browser auth, Tailscale serve, and local model routing.
- [`fleet-skill-sync`](fleet-skill-sync/): Use when pulling, comparing, de-duping, curating or syncing skills across the agent fleet (primary nodes, worker nodes, media hosts, and approved client-bot profiles), or when asked to consolidate fleet skills into the clawd master library
- [`git-sync`](git-sync/): Automatically syncs local workspace changes to the remote GitHub repository. Use after significant changes or periodically.
- [`gitclaw`](gitclaw/): Back up the OpenClaw agent workspace to a GitHub repo and keep it synced via a cron-driven commit/push script.
- [`healthcheck`](healthcheck/): Host security hardening and risk-tolerance configuration for OpenClaw deployments. Use when a user asks for security audits, firewall/SSH/update hardening, risk posture, exposure review, OpenClaw cron scheduling for periodic checks, or version status checks on a machine running OpenClaw (laptop, workstation, Pi, VPS).
- [`hermes-runtime-operations`](hermes-runtime-operations/): Operate and troubleshoot Hermes runtime health in production-like environments. Use for routine environment maintenance (gateway/cron/disk/workspace checks) and auth incident response (OAuth/API-key failures, refresh-token issues, headless device-code recovery).
- [`model-usage`](model-usage/): Use CodexBar CLI local cost usage to summarize per-model usage for Codex or Claude, including the current (most recent) model or a full model breakdown. Trigger when asked for model-level usage/cost data from codexbar, or when you need a scriptable per-model summary from codexbar cost JSON.
- [`node-connect`](node-connect/): Diagnose OpenClaw node connection and pairing failures for Android, iOS, and macOS companion apps. Use when QR/setup code/manual connect fails, local Wi-Fi works but VPS/tailnet does not, or errors mention pairing required, unauthorized, bootstrap token invalid or expired, gateway.bind, gateway.remote.url, Tailscale, or plugins.entries.device-pair.config.publicUrl.
- [`node-inspect-debugger`](node-inspect-debugger/): Debug Node.js via --inspect + Chrome DevTools Protocol CLI.
- [`openclaw-to-hermes`](openclaw-to-hermes/): Port OpenClaw Appie to Hermes Agent and spawn new instances. Clone appie-brain, configure identity files (SOUL.md, USER.md, IDENTITY.md, AGENTS.md), set up git sync, copy secrets, and start Hermes gateway.
- [`python-debugpy`](python-debugpy/): Debug Python: pdb REPL + debugpy remote (DAP).
- [`session-logs`](session-logs/): Search and analyze your own session logs (older/parent conversations) using jq.
- [`ssh-access-recovery`](ssh-access-recovery/): Restore SSH access when the host is reachable but authentication fails. Diagnose the real failure mode, use the smallest safe break-glass path, convert back to key-based auth, and verify from the source machine.
- [`tmux`](tmux/): Remote-control tmux sessions for interactive CLIs by sending keystrokes and scraping pane output.
- [`vercel-deploy`](vercel-deploy/): Deploy projects to Vercel via CLI with token auth. Use when deploying Next.js, static sites, or any project to Vercel from the terminal.
