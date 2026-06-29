#!/usr/bin/env bash
# One-command setup. Creates a venv, installs Cognify with the chosen backend
# extras, and prints next steps. Usage: ./setup.sh [local|neo4j|all]
set -euo pipefail
cd "$(dirname "$0")"
EXTRA="${1:-local}"

# macOS Homebrew: expat shim so pypdf/chromadb load (harmless elsewhere).
if [[ "$(uname)" == "Darwin" && -d /opt/homebrew/opt/expat/lib ]]; then
  export DYLD_LIBRARY_PATH="/opt/homebrew/opt/expat/lib:/opt/homebrew/lib"
fi

PY="${PYTHON:-python3}"
[ -d .venv ] || "$PY" -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
pip install --quiet --upgrade pip
pip install --quiet -e ".[${EXTRA}]"

[ -f .env ] || { cp .env.example .env; echo "created .env (fill in your LLM key)"; }

echo
echo "Cognify installed (backend extras: ${EXTRA})."
echo "  1. edit .env  -> set OPENROUTER_API_KEY (or your OpenAI-compatible key)"
echo "  2. source .venv/bin/activate && set -a && . ./.env && set +a"
echo "  3. cognify ingest examples/sample_docs/clark.md --tenant demo"
echo "     cognify recall 'what does Clark use for memory?' --tenant demo"
echo "  or: python examples/quickstart.py"
