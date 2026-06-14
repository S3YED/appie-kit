# Meta - 11 skills

Skills about skills: authoring, planning, QA, dogfooding, and agent workflow meta-processes.

## Skills

- [`brainstorming`](brainstorming/): MUST use before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation.
- [`clawhub`](clawhub/): Use the ClawHub CLI to search, install, update, and publish agent skills from clawhub.com. Use when you need to fetch new skills on the fly, sync installed skills to latest or a specific version, or publish new/updated skill folders with the npm-installed clawhub CLI.
- [`clawlist`](clawlist/): MUST use for any multi-step project, long-running task, or infinite monitoring workflow. Plan, execute, track, and verify tasks with checkpoint validation. For projects, automation, and ongoing operations.
- [`dispatch-multiple-agents`](clawlist/dispatch-multiple-agents/): Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies. Dispatch subagents to work concurrently.
- [`dogfood`](dogfood/): Exploratory QA of web apps: find bugs, evidence, reports.
- [`doing-tasks`](clawlist/doing-tasks/): Use when executing any task. Work through plans systematically, tracking progress, handling blockers, and coordinating with other skills. The central execution skill.
- [`hermes-agent-skill-authoring`](hermes-agent-skill-authoring/): Author in-repo SKILL.md: frontmatter, validator, structure.
- [`never-relay-uncaptured-output`](never-relay-uncaptured-output/): Guard-rail against fabricating or relaying command output, URLs, tokens, deploy status, or API data that was not literally captured from a real tool call in this session. Born from a recurring fabrication loop (2026-05-30) where a session claimed successful Vercel deploys and Brevo API responses without real tool output. Use whenever you are about to relay a result to the user or report a task as complete.
- [`skill-creator`](skill-creator/): Create, edit, improve, or audit AgentSkills. Use when creating a new skill from scratch or when asked to improve, review, audit, tidy up, or clean up an existing skill or SKILL.md file. Also use when editing or restructuring a skill directory (moving files to references/ or scripts/, removing stale content, validating against the AgentSkills spec). Triggers on phrases like "create a skill", "author a skill", "tidy up a skill", "improve this skill", "review the skill", "clean up the skill", "audit the skill".
- [`verify-task`](verify-task/): MUST use after completing any multi-step task or project. Verifies completion against the original plan, checks quality criteria, and documents outcomes.
- [`write-plan`](write-plan/): MUST use after brainstorming and before executing. Creates detailed implementation plans with checkpoints, verification criteria, and execution options.
