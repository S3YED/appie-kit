---
name: claw
description: OpenClaw workflow skills for desktop control, flow orchestration, hub operations, inbox triage, and task-list management. Use when coordinating agentic work through Claw-branded tools and workflows.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [claw, orchestration, desktop-automation, workflows, task-lists]
    related_skills: [coding-agent, dispatch-multiple-agents, doing-tasks]
---

# Claw Workflow Umbrella

## Overview
Use this umbrella for Claw-branded agent workflows. The shared theme is coordinating work, not solving a domain-specific problem.

## Sections
- **Desktop control:** remote UI control and interactive app driving.
- **Flow orchestration:** multi-step or detached workflows that run across sessions.
- **Hub operations:** skill/package discovery, install/update/publish style tasks.
- **Inbox triage:** sorting, summarizing, and routing incoming work.
- **Task lists:** maintaining ordered work queues and execution state.

## Workflow
1. Identify whether the task is about operating Claw infrastructure or moving work through it.
2. Break the task into a small execution plan with clear checkpoints.
3. Keep session-specific details in references or scripts, not in the umbrella body.

## References
- `references/workflows.md` for the coordination families absorbed into this umbrella.

## Pitfalls
- Don’t create separate micro-skills for each one-off Claw session artifact.
- Don’t confuse a workflow wrapper with the underlying task domain.
- Don’t let desktop control and queue management drift into separate skill families when they serve the same coordination class.
