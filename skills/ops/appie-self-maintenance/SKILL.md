---
name: appie-self-maintenance
title: Appie-2 Self-Maintenance Skill
description: Daily healthcheck and maintenance for Appie-2. Keeps the system running smooth.
---

## Purpose
Daily healthcheck and maintenance for Appie-2. Keeps the system running smooth.

## What It Checks
- Gateway status (port 18789, process health)
- Disk space (workspace, logs)
- Git repo status (pending commits, branch state)
- OpenClaw version vs latest
- Memory file freshness (is HEARTBEAT.md current?)
- Skills health (can key scripts run?)

## What It Does
- Updates HEARTBEAT.md with fresh timestamp and status
- Reports issues to Telegram via cron delivery
- Archives old memory entries (>7 days)

## Operational Environment
- **Hosting Provider:** Hetzner
- **RAM:** 32GB

## Internal Constraints
- **Persistent Memory Limit:** 2,200 characters. When this limit is reached, older or less critical entries may need to be consolidated or removed before new information can be added.

## Usage
Run via cron or on-demand for self-maintenance.
