---
name: rtk-token-killer
description: rtk (Rust Token Killer) — CLI proxy that filters/compresses command output before it reaches the LLM, cutting tokens 60-90% on ls/cat/grep/git/tests/etc. Fleet token-discipline tool. Prefix heavy read/inspect commands with `rtk`.
---

# rtk — Rust Token Killer (fleet token discipline)

A single Rust binary that filters and summarises command output before it hits the LLM context. ~80% fewer tokens on common dev commands, <10ms overhead, 100+ commands. Apache-2.0. Directly serves our token-reduction doctrine.

## Install
```bash
brew install rtk                                  # macOS
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh   # Linux/macOS -> ~/.local/bin
rtk --version
```

## Use it (prefix the command)
```bash
rtk ls            rtk tree           rtk read <file>        # token-optimized read/list
rtk git status    rtk git diff       rtk git log            # compact git
rtk grep <pat>    rtk find -name x   rtk diff a b           # condensed search/diff
rtk test          rtk err <cmd>                             # tests: only failures; cmd: only errors/warnings
rtk gh ...        rtk docker ...     rtk psql ...           # compact gh/docker/db
rtk json <file>   rtk env            rtk deps               # compact json/env/deps
```
`rtk smart` gives a 2-line technical summary of output.

## Automatic mode (recommended for agents)
```bash
rtk init -g       # installs a global hook so common commands route through rtk automatically
```
Without the hook, just prefix manually with `rtk`.

## When to use
- DEFAULT for any read-only inspect command whose raw output is large (file reads, listings, grep, git status/diff/log, test runs, logs, docker ps, json).
- Pairs with [[token discipline]]: reference-over-inline, deltas-over-dumps — rtk enforces it at the shell layer.
- Not for commands whose full output you genuinely need verbatim (then run the raw command).

## Verified
Tested on appie-brain 2026-06-14 (rtk 0.42.4): `rtk git status`, `rtk ls` return compact output correctly. Pushed fleet-wide.
