"""Presentation contract wiring and mechanical checks, not an LLM-quality eval."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = PROJECT_ROOT / "scripts"
PRESENTATION = "routes/model-selection-presentation.md"
UPSTREAM_REPORTS = (
    "synthesis/problem-baseline.md",
    "routes/route-a.md",
    "routes/route-b.md",
    "routes/route-review.md",
    "routes/responses/route-a-response.md",
    "routes/responses/route-b-response.md",
    "routes/model-candidate-briefing.md",
    "literature/route-alignment/route-a/scout-memo.md",
    "literature/route-alignment/route-b/scout-memo.md",
    "literature/route-alignment/human-consultation/consultation-brief.md",
    "literature/route-alignment/human-consultation/response-record.md",
    "literature/route-alignment/evidence-review.md",
    "literature/route-alignment/route-evidence-handoff.md",
    "literature/route-alignment/sources/REF-SYNTHETIC/source-note.md",
)


class ModelSelectionPresentationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.run_dir = Path(self.temp.name) / "run"
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "init_run.py"), str(self.run_dir)],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for relative in UPSTREAM_REPORTS:
            self.write_fixture(relative)

    def write_fixture(self, relative: str, text: str = "Opaque mechanical fixture.\n") -> None:
        path = self.run_dir / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def check_stage(self, stage: str) -> tuple[int, dict]:
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "check_workspace.py"),
             str(self.run_dir), "--stage", stage, "--json"],
            capture_output=True, text=True, check=False,
        )
        self.assertIn(result.returncode, (0, 1), result.stdout + result.stderr)
        return result.returncode, json.loads(result.stdout)

    def test_complete_briefing_does_not_replace_missing_or_empty_presentation(self) -> None:
        for state in ("missing", "empty"):
            with self.subTest(state=state):
                if state == "empty":
                    self.write_fixture(PRESENTATION, "")
                code, report = self.check_stage("model-briefing")
                self.assertEqual(code, 1)
                self.assertEqual(report["errors"], [f"missing or empty report file: {PRESENTATION}"])

    def test_preflight_passes_before_human_reply_without_mutating_run(self) -> None:
        self.write_fixture(PRESENTATION)
        before = {path: path.read_bytes() for path in self.run_dir.rglob("*") if path.is_file()}
        code, report = self.check_stage("model-briefing")
        self.assertEqual(code, 0, report)
        self.assertFalse((self.run_dir / "routes/human-model-decision.md").exists())
        self.assertFalse((self.run_dir / "routes/route-handoff.md").exists())
        after = {path: path.read_bytes() for path in self.run_dir.rglob("*") if path.is_file()}
        self.assertEqual(before, after)
        for key in (
            "semantic_correctness_checked", "citation_support_checked",
            "human_model_decision_authenticity_checked",
            "model_selection_presentation_content_checked",
            "model_selection_presentation_delivery_checked",
        ):
            self.assertFalse(report[key], key)

    def test_preflight_still_requires_upstream_evidence(self) -> None:
        self.write_fixture(PRESENTATION)
        for relative in (
            "routes/responses/route-b-response.md",
            "literature/route-alignment/route-evidence-handoff.md",
            "literature/route-alignment/sources/REF-SYNTHETIC/source-note.md",
        ):
            with self.subTest(relative=relative):
                self.write_fixture(relative, "")
                code, report = self.check_stage("model-briefing")
                self.assertEqual(code, 1)
                self.assertTrue(report["errors"])
                self.write_fixture(relative)

    def test_presentation_does_not_release_human_decision_gate(self) -> None:
        self.write_fixture(PRESENTATION)
        code, report = self.check_stage("route")
        self.assertEqual(code, 1)
        self.assertIn("missing or empty report file: routes/human-model-decision.md", report["errors"])
        self.assertIn("missing or empty report file: routes/route-handoff.md", report["errors"])
        self.write_fixture("routes/human-model-decision.md")
        self.write_fixture("routes/route-handoff.md")
        code, report = self.check_stage("route")
        self.assertEqual(code, 0, report)
        self.assertFalse(report["model_selection_presentation_delivery_checked"])

    def test_legacy_route_and_data_only_warn_about_missing_presentation(self) -> None:
        self.write_fixture("routes/human-model-decision.md")
        self.write_fixture("routes/route-handoff.md")
        self.write_fixture("data/data-handoff.md")
        for stage in ("route", "data"):
            with self.subTest(stage=stage):
                code, report = self.check_stage(stage)
                self.assertEqual(code, 0, report)
                self.assertTrue(any("historical delivery is unverified" in w for w in report["warnings"]))
                self.assertFalse((self.run_dir / PRESENTATION).exists())

    def test_contract_is_wired_into_leader_templates_and_h1(self) -> None:
        team = json.loads((PROJECT_ROOT / "Workflow/team.json").read_text(encoding="utf-8"))
        l2c = next(w for w in team["waves"] if w["id"] == "L2C")
        h1 = next(w for w in team["waves"] if w["id"] == "H1")
        self.assertEqual(l2c["presentation"], PRESENTATION)
        self.assertEqual(h1["presentation"], PRESENTATION)
        self.assertEqual(l2c["preflight_stage"], "model-briefing")
        self.assertEqual(h1["presentation_snapshot_dir"], "routes/presentations/")
        template = (PROJECT_ROOT / l2c["presentation_template"]).read_text(encoding="utf-8")
        for obligation in ("最低责任", "全部实际候选", "合并", "最强竞品", "DOI/URL", "元数据/摘要/全文", "待补", "取舍", "隐藏思维链"):
            self.assertIn(obligation, template)
        decision = (PROJECT_ROOT / "templates/human-model-decision.md").read_text(encoding="utf-8")
        self.assertIn("-presentation.md", decision)
        self.assertIn("-briefing.md", decision)
        self.assertIn("旧快照不可覆盖", decision)
        protocol = (PROJECT_ROOT / "Workflow/protocols/route-tournament.md").read_text(encoding="utf-8")
        self.assertIn("不能用“推荐组合＋详情见文件”", protocol)
        self.assertIn("重新 H1 同样遵守第 5 节", protocol)
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "build_prompt.py"), "--leader"],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for obligation in (PRESENTATION, "--stage model-briefing", "最强竞品", "论文标题", "重新 H1"):
            self.assertIn(obligation, result.stdout)


if __name__ == "__main__":
    unittest.main()
