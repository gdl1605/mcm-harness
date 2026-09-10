"""Regression checks for Windows path serialization and legacy output encodings."""

import json
import os
from pathlib import Path, PureWindowsPath
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import init_run


class PortabilityTests(unittest.TestCase):
    def test_snapshot_serializes_windows_relative_path_as_posix(self):
        config = Mock(wraps=init_run.MCM_INTEGRATION_PATH)
        config.relative_to.return_value = PureWindowsPath("Workflow/mcm-skill-integration.json")
        with patch.object(init_run, "MCM_INTEGRATION_PATH", config):
            snapshot = init_run.mcm_skill_snapshot("test")
        self.assertEqual(snapshot["integration_config"], "Workflow/mcm-skill-integration.json")

    def test_cli_pipes_are_utf8_even_with_legacy_environment(self):
        env = dict(os.environ, PYTHONIOENCODING="cp936", PYTHONUTF8="0")
        with tempfile.TemporaryDirectory(prefix="中文 空格-") as tmp:
            root = Path(tmp)
            source = root / "题目😀.txt"
            source.write_text("中文题目", encoding="utf-8")
            run = root / "运行😀"
            commands = [
                ("bootstrap.py", "--prepare-only", "--source", str(source), "--json"),
                ("init_run.py", str(run), "--source", str(source)),
                ("check_workspace.py", str(run), "--stage", "init", "--json"),
                ("bootstrap.py", "--run-dir", str(run), "--setup-only", "--json"),
                ("build_prompt.py", "--leader"),
            ]
            for command in commands:
                with self.subTest(tool=command[0], args=command[1:]):
                    result = subprocess.run(
                        [sys.executable, str(ROOT / "scripts" / command[0]), *command[1:]],
                        env=env, capture_output=True, check=False,
                    )
                    stdout = result.stdout.decode("utf-8")
                    stderr = result.stderr.decode("utf-8")
                    self.assertEqual(result.returncode, 0, stdout + stderr)
                    if "--json" in command:
                        self.assertIsInstance(json.loads(stdout), dict)
                    elif command[0] == "init_run.py":
                        self.assertIn("运行😀", stdout)
                    else:
                        self.assertIn((ROOT / "prompts/leader.md").read_text(encoding="utf-8").strip(), stdout)
