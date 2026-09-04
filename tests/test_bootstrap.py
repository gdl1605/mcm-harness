from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class BootstrapTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.repo = self.base / "clone with 空格"
        self.repo.mkdir()
        for name in ("scripts", "Workflow", ".agents/skills/mcm"):
            shutil.copytree(ROOT / name, self.repo / name)

    def call(self, *args: str, code: int = 0) -> dict:
        result = subprocess.run(
            [sys.executable, str(self.repo / "scripts/bootstrap.py"), "--json", *args],
            cwd=self.base, text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def source(self, name: str = "C题.txt") -> Path:
        raw = self.repo / "raw-sources"
        raw.mkdir(exist_ok=True)
        path = raw / name
        path.write_text("Synthetic test source", encoding="utf-8")
        return path

    def snapshot(self) -> dict:
        run = self.repo / "run"
        return {
            str(p.relative_to(run)): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in run.rglob("*") if p.is_file()
        }

    def test_empty_clone_prepares_sources_without_freezing_empty_run(self) -> None:
        for _ in range(2):
            report = self.call()
            self.assertEqual(report["status"], "AWAITING_SOURCES")
            self.assertFalse((self.repo / "run").exists())
            self.assertTrue((self.repo / "raw-sources").is_dir())
            self.assertFalse(report["requirements"]["full_workflow_ready"])
            self.assertEqual(report["requirements"]["local_figure_skills"]["nature-figure"], "missing")

    def test_source_discovery_then_repeat_does_not_touch_run(self) -> None:
        self.source()
        self.source("附件.xlsx")
        self.source(".env")
        self.source("~$lock.docx")
        self.source("notes.exe")
        (self.repo / "raw-sources/subfolder").mkdir()
        report = self.call()
        self.assertEqual(report["status"], "INITIALIZED")
        self.assertEqual(report["phase"], "SOURCE_FREEZE")
        self.assertEqual(report["registered_sources"], 2)
        self.assertEqual(report["skipped_source_entries"], ["notes.exe", "subfolder"])
        before = self.snapshot()
        again = self.call()
        self.assertEqual(again["status"], "EXISTING_RUN")
        self.assertEqual(again["run_id"], report["run_id"])
        self.assertEqual(before, self.snapshot())
        self.assertFalse((self.repo / "run/routes/human-model-decision.md").exists())

    def test_progressed_run_keeps_phase_and_reports(self) -> None:
        self.source()
        self.call()
        path = self.repo / "run/state/run-state.json"
        state = json.loads(path.read_text())
        state["phase"] = "AWAITING_HUMAN_FINALIZATION"
        path.write_text(json.dumps(state))
        (self.repo / "run/synthesis/memo.md").write_text("Do not replace")
        before = self.snapshot()
        report = self.call()
        self.assertEqual(report["phase"], "AWAITING_HUMAN_FINALIZATION")
        self.assertEqual(before, self.snapshot())

    def test_explicit_source_and_custom_run(self) -> None:
        source = self.base / "source with 空格.txt"
        source.write_text("Synthetic explicit source")
        target = self.base / "custom run"
        report = self.call("--source", source.name, "--source", source.name,
                           "--run-dir", str(target), "--title", "Explicit title")
        self.assertEqual(report["registered_sources"], 1)
        self.assertEqual(Path(report["run_dir"]), target.resolve())
        self.assertFalse((self.repo / "run").exists())
        self.assertEqual(self.call("--run-dir", str(target))["status"], "EXISTING_RUN")

    def test_missing_explicit_source_does_not_initialize(self) -> None:
        self.assertEqual(self.call("--source", "missing.pdf", code=2)["status"], "BLOCKED")
        self.assertFalse((self.repo / "run").exists())

    def test_source_content_change_is_not_refrozen(self) -> None:
        source = self.source()
        self.call()
        before = self.snapshot()
        source.write_text("Changed source")
        report = self.call(code=2)
        self.assertIn("missing or changed", report["error"])
        self.assertEqual(before, self.snapshot())

    def test_missing_registered_source_is_blocked(self) -> None:
        source = self.source()
        self.call()
        source.unlink()
        self.assertIn("missing or changed", self.call(code=2)["error"])

    def test_added_source_requires_new_run(self) -> None:
        self.source()
        self.call()
        before = self.snapshot()
        self.source("additional.csv")
        self.assertIn("source set changed", self.call(code=2)["error"])
        self.assertEqual(before, self.snapshot())

    def test_explicit_replacement_and_title_changes_are_blocked(self) -> None:
        self.source()
        self.call()
        self.assertIn("title differs", self.call("--title", "Other", code=2)["error"])
        replacement = self.base / "other.txt"
        replacement.write_text("Other synthetic source")
        self.assertIn("source set changed", self.call("--source", str(replacement), code=2)["error"])

    def test_nonempty_unrecognized_directory_is_preserved(self) -> None:
        run = self.repo / "run"
        run.mkdir()
        (run / "keep.txt").write_text("Keep")
        before = self.snapshot()
        self.call(code=2)
        self.assertEqual(before, self.snapshot())

    def test_skill_drift_is_not_reset(self) -> None:
        self.source()
        self.call()
        before = self.snapshot()
        skill = self.repo / ".agents/skills/mcm/SKILL.md"
        skill.write_text(skill.read_text() + "\nChanged instructions\n")
        self.assertIn("changed since initialization", self.call(code=2)["error"])
        self.assertEqual(before, self.snapshot())

    def test_broken_clone_fails_before_directory_creation(self) -> None:
        (self.repo / ".agents/skills/mcm/SKILL.md").unlink()
        self.call(code=2)
        self.assertFalse((self.repo / "raw-sources").exists())
        self.assertFalse((self.repo / "run").exists())

    def test_corrupt_run_metadata_fails_without_repair(self) -> None:
        self.source()
        self.call()
        path = self.repo / "run/state/run-state.json"
        path.write_text("[]")
        before = self.snapshot()
        self.assertIn("JSON object", self.call(code=2)["error"])
        self.assertEqual(before, self.snapshot())

    def test_legacy_empty_source_run_is_not_silently_repopulated(self) -> None:
        result = subprocess.run(
            [sys.executable, str(self.repo / "scripts/init_run.py"), str(self.repo / "run")],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        before = self.snapshot()
        self.source()
        self.assertIn("no registered sources", self.call(code=2)["error"])
        self.assertEqual(before, self.snapshot())

    def test_text_output_explains_waiting_and_invalid_paths(self) -> None:
        command = [sys.executable, str(self.repo / "scripts/bootstrap.py")]
        result = subprocess.run(command, text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 0)
        self.assertIn("AWAITING_SOURCES", result.stdout)
        self.assertIn("不安装依赖", result.stdout)
        (self.repo / "run").write_text("Not a directory")
        result = subprocess.run(command, text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 2)
        self.assertIn("Bootstrap blocked", result.stderr)

    def test_integration_config_drift_is_not_reset(self) -> None:
        self.source()
        self.call()
        config_path = self.repo / "Workflow/mcm-skill-integration.json"
        config_path.write_text(config_path.read_text() + "\n")
        before = self.snapshot()
        self.assertIn("changed since initialization", self.call(code=2)["error"])
        self.assertEqual(before, self.snapshot())

    def test_auto_discovery_does_not_follow_symlinks(self) -> None:
        raw = self.repo / "raw-sources"
        raw.symlink_to(self.base, target_is_directory=True)
        self.assertIn("symlink", self.call(code=2)["error"])
        raw.unlink()
        source = self.source()
        (raw / "linked.txt").symlink_to(source)
        self.assertIn("symlink", self.call(code=2)["error"])
        self.assertFalse((self.repo / "run").exists())

    def test_unsafe_run_destinations_are_rejected(self) -> None:
        self.assertIn("contain the repository", self.call("--run-dir", str(self.repo), code=2)["error"])
        target = self.base / "external"
        target.mkdir()
        (self.repo / "run").symlink_to(target, target_is_directory=True)
        self.assertIn("symlink", self.call(code=2)["error"])
        self.assertEqual(list(target.iterdir()), [])

    def test_external_skill_hash_is_reported_not_installed(self) -> None:
        entry = self.repo / ".agents/skills/ssci-plots/SKILL.md"
        entry.parent.mkdir(parents=True)
        entry.write_text("test fixture")
        self.assertEqual(self.call()["requirements"]["local_figure_skills"]["ssci-plots"], "hash_mismatch")
        lock_path = self.repo / "Workflow/ssci-plots-skill.lock.json"
        lock = json.loads(lock_path.read_text())
        lock["skill_md_sha256"] = hashlib.sha256(entry.read_bytes()).hexdigest()
        lock_path.write_text(json.dumps(lock))
        self.assertEqual(self.call()["requirements"]["local_figure_skills"]["ssci-plots"], "hash_matches_lock")

    def test_agent_entrypoint_is_early_and_distinguishes_development(self) -> None:
        agents = (ROOT / "AGENTS.md").read_text()
        self.assertIn("scripts/bootstrap.py --json", agents[:4000])
        self.assertIn("开发或修改", agents[:4000])
        self.assertTrue((ROOT / "BOOTSTRAP.md").is_file())


if __name__ == "__main__":
    unittest.main()
