#!/usr/bin/env python3
"""
hermes-clean-output.py — apply the clean/minimal client-output standard to a Hermes bot.

Implements PRD-hermes-clean-telegram-output.md: sets the display.platforms.telegram
override (+ legacy telegram: block) so a client only sees the final natural-language
answer (no tool calls, reasoning, shell echoes, or status bubbles), and appends the
"Client Communication" persona block to SOUL.md (idempotent).

Usage:
  hermes-clean-output.py --home /root/.hermes [--profile client|operator] [--check]

Safe: backs up config.yaml before editing; no secrets touched; idempotent.
"""
import argparse, os, sys, shutil, datetime

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml")

SOUL_BLOCK = """
## Client Communication (clean output)
- Reply with the answer only. One clear, natural-language message.
- Keep your full capability. Do everything you can already do: all tools, skills, knowledge and actions stay available and unchanged. Only the way you SHOW your work changes.
- Hide your process, not your results. Do not narrate tools, searches, reasoning, or steps. Do not paste raw logs, shell commands or their output, JSON blobs, internal IDs, or server file paths.
- Still deliver exactly what the client asks for, including code, a file, a link or a snippet when they explicitly request it. Give the deliverable cleanly, without the surrounding machinery.
- Do not show your reasoning or thinking. Decide silently, then answer.
- Write like a calm, competent human assistant. Short sentences. Plain words. Mirror the client's language (NL/EN).
- If a task takes a while, send at most one short line ("One moment, working on it.") and then the result.
- If you need something from the client, ask one direct question.
- No em dashes. No corporate filler. No "as an AI" framing.
- If you cannot do something, say so plainly in one sentence and offer the next best step.
"""

SOUL_MARKER = "## Client Communication (clean output)"

CLIENT_DISPLAY = {
    "show_reasoning": False,
    "streaming": False,
    "background_process_notifications": "off",
    "tool_progress": "off",
    "platforms": {
        "telegram": {
            "tool_progress": "off",
            "show_reasoning": False,
            "interim_assistant_messages": False,
            "tool_preview_length": 0,
            "cleanup_progress": True,
            "streaming": False,
        },
        "whatsapp": {
            "tool_progress": "off",
            "show_reasoning": False,
            "interim_assistant_messages": False,
            "tool_preview_length": 0,
            "cleanup_progress": True,
        },
    },
}
CLIENT_TELEGRAM = {
    "show_reasoning": False,
    "tool_progress": False,
    "interim_assistant_messages": False,
}


def patch_config(path, profile):
    if not os.path.exists(path):
        print(f"SKIP config: {path} not found")
        return False
    with open(path) as f:
        cfg = yaml.safe_load(f) or {}
    if profile == "operator":
        print("profile=operator: leaving verbose/tool-visible behaviour intact")
        return False
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    shutil.copy2(path, f"{path}.bak-cleanoutput-{ts}")
    disp = cfg.get("display") or {}
    disp.update({k: v for k, v in CLIENT_DISPLAY.items() if k != "platforms"})
    plats = disp.get("platforms") or {}
    for p, vals in CLIENT_DISPLAY["platforms"].items():
        plats[p] = {**(plats.get(p) or {}), **vals}
    disp["platforms"] = plats
    cfg["display"] = disp
    cfg["telegram"] = {**(cfg.get("telegram") or {}), **CLIENT_TELEGRAM}
    cfg["output_profile"] = "client"
    with open(path, "w") as f:
        yaml.safe_dump(cfg, f, sort_keys=False, allow_unicode=True)
    print(f"config patched (backup .bak-cleanoutput-{ts})")
    return True


def patch_soul(path):
    if not os.path.exists(path):
        print(f"SKIP SOUL: {path} not found")
        return False
    txt = open(path).read()
    if SOUL_MARKER in txt:
        print("SOUL already has Client Communication block (idempotent skip)")
        return False
    with open(path, "a") as f:
        f.write("\n" + SOUL_BLOCK)
    print("SOUL Client Communication block appended")
    return True


def check(path):
    cfg = yaml.safe_load(open(path)) or {}
    tg = (((cfg.get("display") or {}).get("platforms") or {}).get("telegram") or {})
    ok = tg.get("tool_progress") == "off" and tg.get("show_reasoning") is False and tg.get("interim_assistant_messages") is False
    print("RESOLVED telegram:", {k: tg.get(k) for k in ["tool_progress", "show_reasoning", "interim_assistant_messages"]})
    print("VALIDATION:", "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--home", required=True, help="Hermes home (contains config.yaml + SOUL.md)")
    ap.add_argument("--profile", default="client", choices=["client", "operator"])
    ap.add_argument("--check", action="store_true", help="only validate, do not modify")
    a = ap.parse_args()
    cfg_path = os.path.join(a.home, "config.yaml")
    soul_path = os.path.join(a.home, "SOUL.md")
    if a.check:
        sys.exit(0 if check(cfg_path) else 1)
    patch_config(cfg_path, a.profile)
    patch_soul(soul_path)
    if a.profile == "client" and os.path.exists(cfg_path):
        check(cfg_path)
