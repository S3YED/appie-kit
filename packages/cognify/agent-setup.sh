#!/usr/bin/env bash
# Set up Cognify on a fleet agent: a LOCAL graph of its own workspace + access to
# the SHARED fleet brain. Idempotent. Run on any box (Hermes or Claude Code).
#
#   ./agent-setup.sh <agent-name> [workspace-dir]
#
# Env it honours:
#   COGNIFY_SHARED=1            also wire shared-brain access (needs NEO4J_* below)
#   NEO4J_URI/NEO4J_USER/NEO4J_PASSWORD   shared graph on appie-2 (Tailscale)
#   COGNIFY_LLM_KEY or OPENROUTER_API_KEY / ANTHROPIC_API_KEY   extractor
#   SKILLS_DIR                 where to drop the skill (default ~/.hermes/skills)
set -euo pipefail
AGENT="${1:?usage: agent-setup.sh <agent-name> [workspace-dir]}"
WORKSPACE="${2:-$HOME/.hermes/memory}"
HERE="$(cd "$(dirname "$0")" && pwd)"
CFG="$HOME/.cognify"
mkdir -p "$CFG"

# 1. install the package (local backend; add neo4j extra when sharing)
EXTRAS="local"
[ "${COGNIFY_SHARED:-0}" = "1" ] && EXTRAS="local,neo4j"
PYBIN="${PYTHON:-python3}"
"$PYBIN" -m pip install -q -e "${HERE}[${EXTRAS}]" 2>/dev/null || "$PYBIN" -m pip install -q "${HERE}" 2>/dev/null || true

# 2. write the agent's config (tenant isolates this agent's local data)
cat > "$CFG/agent.env" <<ENV
export COGNIFY_DATA_DIR="$CFG/data"
export COGNIFY_TENANT_LOCAL="agent:${AGENT}"
export COGNIFY_BACKEND=local
ENV
[ "${COGNIFY_SHARED:-0}" = "1" ] && cat >> "$CFG/agent.env" <<ENV
export COGNIFY_SHARED=1
export NEO4J_URI="${NEO4J_URI:-}"
export NEO4J_USER="${NEO4J_USER:-neo4j}"
export NEO4J_PASSWORD="${NEO4J_PASSWORD:-}"
ENV
echo "wrote $CFG/agent.env (tenant=agent:${AGENT}, shared=${COGNIFY_SHARED:-0})"

# 3. ingest this agent's workspace into its LOCAL graph
if [ -d "$WORKSPACE" ]; then
  # shellcheck disable=SC1090
  source "$CFG/agent.env"
  echo "ingesting workspace $WORKSPACE -> local graph (tenant=agent:${AGENT})"
  "$PYBIN" -m cognify.cli --backend local --tenant "agent:${AGENT}" --namespace workspace \
    ingest-dir "$WORKSPACE" --glob '**/*.md' --cache 2>&1 | tail -3 || true
fi

# 4. drop the Hermes skill so the agent uses it
SKILLS_DIR="${SKILLS_DIR:-$HOME/.hermes/skills}"
if [ -d "$SKILLS_DIR" ] && [ -f "$HERE/integrations/hermes/SKILL.md" ]; then
  mkdir -p "$SKILLS_DIR/cognify"
  cp "$HERE/integrations/hermes/SKILL.md" "$SKILLS_DIR/cognify/SKILL.md"
  echo "installed cognify skill -> $SKILLS_DIR/cognify/"
fi

echo "DONE. local recall:  source $CFG/agent.env && cognify recall '<q>' --backend local --tenant agent:${AGENT}"
[ "${COGNIFY_SHARED:-0}" = "1" ] && echo "      shared recall:  cognify recall '<q>' --backend neo4j --tenant fleet"
