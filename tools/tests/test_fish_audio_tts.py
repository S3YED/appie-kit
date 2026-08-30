#!/usr/bin/env python3
"""Contract tests for the fleet Fish Audio TTS executable and installer."""

from __future__ import annotations

import importlib.machinery
import importlib.util
import pathlib
import shlex
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "tools" / "fish-audio-tts"
CONFIGURATOR = ROOT / "tools" / "configure-fish-audio-tts.py"


def load_module():
    loader = importlib.machinery.SourceFileLoader("fish_audio_tts", str(SCRIPT))
    spec = importlib.util.spec_from_loader("fish_audio_tts", loader)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load fish-audio-tts")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_configurator():
    loader = importlib.machinery.SourceFileLoader("fish_audio_configurator", str(CONFIGURATOR))
    spec = importlib.util.spec_from_loader("fish_audio_configurator", loader)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load configure-fish-audio-tts.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FishAudioTtsContractTest(unittest.TestCase):
    def test_default_payload_uses_fish_s21_free_and_mp3(self):
        module = load_module()
        payload = module.build_payload("[warm] Hello")
        self.assertEqual(payload["model"], "fish-audio/s2.1-pro-free:free")
        self.assertEqual(payload["input"], "[warm] Hello")
        self.assertEqual(payload["response_format"], "mp3")
        self.assertNotIn("voice", payload)

    def test_error_redacts_openrouter_key(self):
        module = load_module()
        secret = "token-super-secret"
        error = module.safe_error(RuntimeError(f"upstream rejected {secret}"), secret)
        self.assertNotIn(secret, error)
        self.assertIn("[REDACTED]", error)

    def test_installer_configures_custom_provider(self):
        installer = (ROOT / "tools" / "configure-fish-audio-tts.py").read_text()
        self.assertIn('"provider": "fish-audio"', installer)
        self.assertIn('"type": "command"', installer)
        self.assertIn('"voice_compatible": True', installer)
        self.assertNotIn("OPENROUTER_API_KEY=", installer)

    def test_command_path_is_shell_quoted(self):
        module = load_configurator()
        command_path = pathlib.Path("/tmp/Hermes Profile/bin/fish-audio-tts")
        configured = module.configure({}, command_path)
        command = configured["tts"]["providers"]["fish-audio"]["command"]
        self.assertEqual(shlex.split(command)[0], str(command_path))
        self.assertIn("{input_path}", command)
        self.assertIn("{output_path}", command)

    def test_workspace_docs_name_fish_as_default_and_kokoro_as_retired(self):
        tools = (ROOT / "workspace" / "TOOLS.md").read_text()
        cloud = (ROOT / "workspace" / "CLOUD.md").read_text()
        combined = tools + cloud
        self.assertIn("fish-audio/s2.1-pro-free:free", combined)
        self.assertIn("default", combined.lower())
        self.assertIn("Kokoro", combined)
        self.assertIn("retired", combined.lower())


if __name__ == "__main__":
    unittest.main()
