# Fleet MCP install notes

Use this reference when installing Weblyfe's webdesign MCP stack across Appie/Hermes homes.

## Durable lessons

- Hermes MCP subprocesses may run with a reduced PATH. Prefer absolute `npx`/`npm` paths in `mcp_servers.<name>.command` and include a `PATH` entry in `mcp_servers.<name>.env` so Node can find its runtime.
- Do not store API keys directly in `config.yaml`. Store secrets in `.env` and reference them in config as `${ENV_VAR}`. Hermes expands `${VAR}` values from the runtime environment.
- For shadcn MCP, a GitHub token is optional but recommended. Use `GITHUB_PERSONAL_ACCESS_TOKEN` or `GITHUB_TOKEN` as an env reference for higher GitHub API limits.
- 21st.dev Magic and Magic UI are separate tools:
  - `@21st-dev/magic` generates components and needs a 21st.dev API key, passed as `API_KEY`.
  - `@magicuidesign/mcp` exposes the Magic UI public registry and usually needs no API key.
- Chrome DevTools MCP should be tested per Hermes home with `hermes mcp test chrome_devtools`. On headless fleet machines, use `--headless` and disable telemetry/update checks through args/env.
- After changing MCP config, restart Hermes or run `/reload-mcp`; current sessions may not see newly discovered tools.

## Verification pattern

For every Hermes home/profile:

```bash
HERMES_HOME=/path/to/home hermes mcp list
HERMES_HOME=/path/to/home hermes mcp test shadcn_ui
HERMES_HOME=/path/to/home hermes mcp test magic_ui
HERMES_HOME=/path/to/home hermes mcp test chrome_devtools
```

Expected tool counts at time of capture:
- `shadcn_ui`: 10 tools
- `magic_ui`: 3 tools
- `chrome_devtools`: 29 tools

Do not treat these counts as permanent API contracts. They are a smoke-test baseline only.
