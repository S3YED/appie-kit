# Cognify + Claude

Two ways to use Cognify with Claude.

## 1. Claude as the extractor (the brain that builds the graph)

Cognify uses Claude natively when `ANTHROPIC_API_KEY` is set (auto-detected):

```bash
pip install 'cognify-kg[local]'
export ANTHROPIC_API_KEY=sk-ant-...
# optional: export COGNIFY_ANTHROPIC_MODEL=claude-3-5-haiku-latest
cognify ingest notes.md --tenant demo
cognify recall "what connects to onboarding?" --tenant demo
```

Force it explicitly with `COGNIFY_LLM_PROVIDER=anthropic`.

## 2. Cognify as MCP tools (Claude Code / Claude Desktop use it)

Expose `cognify_ingest`, `cognify_recall`, `cognify_stats` as MCP tools so Claude
can build and query memory itself.

```bash
pip install 'cognify-kg[local,claude]'
```

**Claude Code:**
```bash
claude mcp add cognify -- cognify-mcp
```

**Claude Desktop** (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "cognify": {
      "command": "cognify-mcp",
      "env": {
        "ANTHROPIC_API_KEY": "sk-ant-...",
        "COGNIFY_BACKEND": "local",
        "COGNIFY_DATA_DIR": "/absolute/path/to/.cognify"
      }
    }
  }
}
```

Then ask Claude to "remember this document" (it calls `cognify_ingest`) or
"what do we know about X?" (it calls `cognify_recall` and answers from the
returned chunks + entity/relation subgraph).
