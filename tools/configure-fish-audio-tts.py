#!/usr/bin/env python3
"""Configure Fish Audio as the default Hermes custom-command TTS provider."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import shlex
import shutil
import tempfile

import yaml


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser()
    value.add_argument("--hermes-home", type=Path, default=Path(os.environ.get("HERMES_HOME", "~/.hermes")).expanduser())
    value.add_argument("--command-path", type=Path, default=None)
    value.add_argument("--dry-run", action="store_true")
    return value


def configure(config: dict, command_path: Path) -> dict:
    tts = config.setdefault("tts", {})
    tts.update({"provider": "fish-audio"})
    providers = tts.setdefault("providers", {})
    providers["fish-audio"] = {
        "type": "command",
        "command": f"{shlex.quote(str(command_path))} --input {{input_path}} --output {{output_path}}",
        "output_format": "mp3",
        "timeout": 150,
        "max_text_length": 12000,
        "voice_compatible": True,
    }
    return config


def atomic_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            yaml.safe_dump(data, handle, sort_keys=False, allow_unicode=True)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def main() -> int:
    args = parser().parse_args()
    home = args.hermes_home.expanduser().resolve()
    config_path = home / "config.yaml"
    command_path = (args.command_path or home / "bin" / "fish-audio-tts").expanduser().resolve()
    config = yaml.safe_load(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
    config = configure(config or {}, command_path)
    if args.dry_run:
        print(yaml.safe_dump(config, sort_keys=False, allow_unicode=True), end="")
        return 0
    if config_path.exists():
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        shutil.copy2(config_path, config_path.with_name(f"config.yaml.bak-fish-audio-{stamp}"))
    atomic_yaml(config_path, config)
    os.chmod(config_path, 0o600)
    print(f"configured Fish Audio TTS in {config_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
