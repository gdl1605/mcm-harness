from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = PROJECT_ROOT / "scripts"


class WorkflowToolTests(unittest.TestCase):
    def test_open_markdown_run_and_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "problem.txt"
            source.write_text("Synthetic C problem", encoding="utf-8")
            run_dir = root / "run"

            initialized = subprocess.run(
                [sys.executable, str(SCRIPTS / "init_run.py"), str(run_dir), "--title", "Synthetic C", "--source", str(source)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(initialized.returncode, 0, initialized.stderr)

            checked = subprocess.run(
                [sys.executable, str(SCRIPTS / "check_workspace.py"), str(run_dir), "--stage", "init", "--json"],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
            report = json.loads(checked.stdout)
            self.assertFalse(report["markdown_content_parsed"])
            self.assertFalse(report["semantic_correctness_checked"])
            self.assertTrue((run_dir / "submissions/W3R").is_dir())
            self.assertTrue((run_dir / "routes/responses").is_dir())
            self.assertTrue((run_dir / "data/staging").is_dir())
            self.assertTrue((run_dir / "data/processed/canonical").is_dir())
            self.assertTrue((run_dir / "data/processed/analytical").is_dir())
            self.assertFalse(any((run_dir / "data").rglob("*.md")))
            self.assertFalse((run_dir / "synthesis/problem-baseline.md").exists())

            brief = run_dir / "briefs/W1-literal.md"
            brief.write_text((PROJECT_ROOT / "templates/task-brief.md").read_text(encoding="utf-8"), encoding="utf-8")
            rendered = subprocess.run(
                [sys.executable, str(SCRIPTS / "build_prompt.py"), "--role", "literal-contract", "--task-brief", str(brief)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(rendered.returncode, 0, rendered.stderr)
            self.assertIn("Worker Base Prompt", rendered.stdout)
            self.assertIn("最低必答", rendered.stdout)
            self.assertIn("任务之外的新发现", rendered.stdout)

    def test_data_workspace_stage_templates_and_prompts(self) -> None:
        template_root = PROJECT_ROOT / "templates/data-engineering"
        expected_templates = {
            "task-brief.md",
            "data-contract.md",
            "data-profile.md",
            "data-risk-review.md",
            "preprocessing-plan.md",
            "preprocessing-log.md",
            "pipeline-implementation-memo.md",
            "repro-review.md",
            "interface-review.md",
            "builder-response.md",
            "data-method-note.md",
            "data-handoff.md",
        }
        self.assertTrue(expected_templates.issubset({path.name for path in template_root.glob("*.md")}))
        for name in expected_templates:
            content = (template_root / name).read_text(encoding="utf-8")
            self.assertIn("最低责任", content)

        with tempfile.TemporaryDirectory() as temp:
            run_dir = Path(temp) / "run"
            initialized = subprocess.run(
                [sys.executable, str(SCRIPTS / "init_run.py"), str(run_dir)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(initialized.returncode, 0, initialized.stderr)

            required_data_dirs = (
                "briefs", "contracts", "profiling", "decisions", "pipeline/src",
                "pipeline/tests", "staging", "processed/canonical",
                "processed/analytical", "reviews", "paper-notes",
            )
            for relative in required_data_dirs:
                self.assertTrue((run_dir / "data" / relative).is_dir(), relative)
            self.assertFalse(any((run_dir / "data").rglob("*.md")))

            stage_reports = (
                "synthesis/problem-baseline.md",
                "routes/route-a.md",
                "routes/route-b.md",
                "routes/route-review.md",
                "routes/route-handoff.md",
            )
            for relative in stage_reports:
                path = run_dir / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("mechanical fixture\n", encoding="utf-8")

            missing_handoff = subprocess.run(
                [sys.executable, str(SCRIPTS / "check_workspace.py"), str(run_dir), "--stage", "data", "--json"],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(missing_handoff.returncode, 1)
            missing_report = json.loads(missing_handoff.stdout)
            self.assertIn("missing or empty handoff file: data/data-handoff.md", missing_report["errors"])

            (run_dir / "data/data-handoff.md").write_text("opaque mechanical fixture\n", encoding="utf-8")
            checked = subprocess.run(
                [sys.executable, str(SCRIPTS / "check_workspace.py"), str(run_dir), "--stage", "data", "--json"],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
            report = json.loads(checked.stdout)
            self.assertFalse(report["markdown_content_parsed"])
            self.assertFalse(report["semantic_correctness_checked"])

            brief = run_dir / "data/briefs/D1-profiler.md"
            brief.write_text((template_root / "task-brief.md").read_text(encoding="utf-8"), encoding="utf-8")
            data_leader = subprocess.run(
                [sys.executable, str(SCRIPTS / "build_prompt.py"), "--data-leader"],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(data_leader.returncode, 0, data_leader.stderr)
            self.assertIn("数据工程 Leader", data_leader.stdout)

            data_worker = subprocess.run(
                [sys.executable, str(SCRIPTS / "build_prompt.py"), "--data-role", "data_profiler", "--task-brief", str(brief)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(data_worker.returncode, 0, data_worker.stderr)
            self.assertIn("数据工程 Worker Base Prompt", data_worker.stdout)
            self.assertIn("角色：数据剖析员", data_worker.stdout)
            self.assertIn("任务之外的新发现", data_worker.stdout)

            data_team_path = PROJECT_ROOT / "Workflow/data-team.json"
            if data_team_path.is_file():
                data_team = json.loads(data_team_path.read_text(encoding="utf-8"))
                self.assertEqual(data_team["execution"]["mode"], "leader_with_native_subagents")
                self.assertFalse(data_team["execution"]["external_orchestrator_required"])
                self.assertTrue((PROJECT_ROOT / data_team["execution"]["worker_base_prompt"]).is_file())
                self.assertIn("data_profiler", data_team["roles"])
                self.assertIn("data_builder_responder", data_team["roles"])
                for role in data_team["roles"].values():
                    prompt = role.get("prompt")
                    if prompt:
                        self.assertTrue((PROJECT_ROOT / prompt).is_file(), prompt)

            response_worker = subprocess.run(
                [sys.executable, str(SCRIPTS / "build_prompt.py"), "--data-role", "data_builder_responder", "--task-brief", str(brief)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(response_worker.returncode, 0, response_worker.stderr)
            self.assertIn("角色：数据实现者集中回应", response_worker.stdout)

    def test_figure_preparation_workspace_and_prompts(self) -> None:
        """Figure preparation starts empty and exposes only preparation prompts.

        The harness prepares evidence/data packages and recommendations.  It does
        not pre-create reports that would pretend that a figure has already been
        selected or rendered, and it does not add a visual-style/plotting CLI.
        """
        with tempfile.TemporaryDirectory() as temp:
            run_dir = Path(temp) / "run"
            initialized = subprocess.run(
                [sys.executable, str(SCRIPTS / "init_run.py"), str(run_dir)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(initialized.returncode, 0, initialized.stderr)

            # The initializer owns the workspace skeleton, but not any semantic
            # figure report or candidate.  These paths are created lazily by the
            # curators/integrator after V6 has frozen its inputs.
            for relative in (
                "figure-prep",
                "figure-prep/scope",
                "figure-prep/questions",
                "figure-prep/cross-question",
                "figure-prep/change-requests",
            ):
                self.assertTrue((run_dir / relative).is_dir(), relative)
            for relative in (
                "figure-prep/figure-plan.md",
                "figure-prep/figure-preparation-handoff.md",
            ):
                self.assertFalse((run_dir / relative).exists(), relative)
            self.assertFalse((run_dir / "figure-prep/shared").exists())
            self.assertFalse(any((run_dir / "figure-prep").rglob("*.md")))

            figure_leader = subprocess.run(
                [sys.executable, str(SCRIPTS / "build_prompt.py"), "--figure-leader"],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(figure_leader.returncode, 0, figure_leader.stderr)
            self.assertIn("图表准备", figure_leader.stdout)
            self.assertIn("F0", figure_leader.stdout)
            self.assertIn("F4", figure_leader.stdout)

            brief = run_dir / "figure-prep/briefs/Q1.md"
            brief.parent.mkdir(parents=True, exist_ok=True)
            brief.write_text(
                "# Figure preparation task\n\n请整理问题一的诊断证据和作图数据。\n",
                encoding="utf-8",
            )
            figure_worker = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "build_prompt.py"),
                    "--figure-role",
                    "question_figure_curator",
                    "--task-brief",
                    str(brief),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(figure_worker.returncode, 0, figure_worker.stderr)
            self.assertIn("图表准备 Worker Base Prompt", figure_worker.stdout)
            self.assertIn("# 本轮 Task Brief", figure_worker.stdout)
            self.assertIn("任务之外的新发现", figure_worker.stdout)

            # The legacy front-half CLI remains available after adding the new
            # module; this is intentionally a smoke check rather than a semantic
            # prompt test.
            legacy = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "build_prompt.py"),
                    "--role",
                    "literal-contract",
                    "--task-brief",
                    str(brief),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(legacy.returncode, 0, legacy.stderr)
            self.assertIn("Worker Base Prompt", legacy.stdout)

    def test_figure_preparation_workspace_stage_is_mechanical(self) -> None:
        """The figure-prep checker only checks files/paths, never Markdown meaning."""
        with tempfile.TemporaryDirectory() as temp:
            run_dir = Path(temp) / "run"
            initialized = subprocess.run(
                [sys.executable, str(SCRIPTS / "init_run.py"), str(run_dir)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(initialized.returncode, 0, initialized.stderr)

            # Figure preparation starts only after V6.  Seed the two opaque V6
            # entry artifacts so this test isolates the figure-prep handoff
            # failure rather than testing the upstream validation gate.
            for relative in (
                "validation/validation-handoff.md",
                "validation/claims/claim-evidence-map.md",
                "figure-prep/scope/frozen-inputs.md",
                "paper-prep/structure/chapter-map-v0.md",
            ):
                path = run_dir / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("opaque V6 fixture\n", encoding="utf-8")

            missing = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "check_workspace.py"),
                    str(run_dir),
                    "--stage",
                    "figure-prep",
                    "--json",
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(missing.returncode, 1, missing.stdout + missing.stderr)
            missing_report = json.loads(missing.stdout)
            self.assertFalse(missing_report["markdown_content_parsed"])
            self.assertFalse(missing_report["semantic_correctness_checked"])
            self.assertFalse(missing_report["figure_aesthetic_checked"])
            self.assertTrue(
                any("figure-preparation-handoff.md" in error for error in missing_report["errors"]),
                missing_report["errors"],
            )

            # Any non-empty Markdown is sufficient for this mechanical check;
            # the checker must not interpret headings, claims, or chart content.
            figure_root = run_dir / "figure-prep"
            (figure_root / "figure-plan.md").write_text("opaque fixture\n", encoding="utf-8")
            (figure_root / "figure-preparation-handoff.md").write_text(
                "opaque fixture\n",
                encoding="utf-8",
            )
            candidate = figure_root / "questions/q1/candidates/FIG-Q1-01"
            candidate.mkdir(parents=True, exist_ok=True)
            (candidate / "data.csv").write_text("x,y\n1,2\n", encoding="utf-8")
            (candidate / "export.py").write_text("# reproducible export fixture\n", encoding="utf-8")
            (candidate / "provenance.md").write_text("opaque provenance fixture\n", encoding="utf-8")
            (candidate / "recommendation.md").write_text("opaque recommendation fixture\n", encoding="utf-8")
            checked = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "check_workspace.py"),
                    str(run_dir),
                    "--stage",
                    "figure-prep",
                    "--json",
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
            report = json.loads(checked.stdout)
            self.assertFalse(report["markdown_content_parsed"])
            self.assertFalse(report["semantic_correctness_checked"])
            self.assertFalse(report["figure_aesthetic_checked"])
            self.assertEqual(report["errors"], [])

    def test_figure_preparation_team_configuration_and_scope(self) -> None:
        team_path = PROJECT_ROOT / "Workflow/figure-preparation-team.json"
        self.assertTrue(team_path.is_file())
        team = json.loads(team_path.read_text(encoding="utf-8"))
        self.assertEqual(team["execution"]["mode"], "leader_with_native_subagents")
        self.assertFalse(team["execution"]["external_orchestrator_required"])
        # Concurrency is described as policy, not as a worker-slot field.
        self.assertNotIn("worker_slots", team["execution"])
        self.assertIn("worker_concurrency_policy", team["execution"])
        self.assertTrue(
            any(
                marker in team["execution"]["worker_concurrency_policy"]
                for marker in ("独立输入", "输入独立性")
            )
        )
        self.assertTrue(team["branch_policy"]["no_fixed_numeric_worker_cap"])

        worker_base = team["execution"]["worker_base_prompt"]
        self.assertTrue((PROJECT_ROOT / worker_base).is_file(), worker_base)
        expected_roles = {
            "question_figure_curator",
            "shared_figure_curator",
            "figure_evidence_auditor",
            "question_curator_response",
            "figure_chapter_integrator",
        }
        self.assertTrue(expected_roles.issubset(team["roles"]))
        for role_name, role in team["roles"].items():
            prompt = role.get("prompt")
            self.assertTrue(prompt, role_name)
            self.assertTrue((PROJECT_ROOT / prompt).is_file(), prompt)

        integrator_writes = team["roles"]["figure_chapter_integrator"]["writes"]
        self.assertIn("figure-prep/cross-question/integration/**", integrator_writes)
        self.assertNotIn("figure-prep/cross-question/**", integrator_writes)
        self.assertIn(
            "figure-prep/cross-question/shared/**",
            team["roles"]["shared_figure_curator"]["writes"],
        )

        # Scope is intentionally evidence preparation only.  These assertions
        # prevent a future config/prompt from silently turning this harness into
        # a plotting-style or formal-figure renderer.
        scope_text = "\n".join(
            [
                (PROJECT_ROOT / "Workflow/figure-preparation.md").read_text(encoding="utf-8"),
                (PROJECT_ROOT / worker_base).read_text(encoding="utf-8"),
                *[
                    (PROJECT_ROOT / role["prompt"]).read_text(encoding="utf-8")
                    for role in team["roles"].values()
                ],
            ]
        )
        self.assertRegex(scope_text, r"不.{0,12}(绘制|生成|负责).{0,12}(论文图|正式图)")
        self.assertRegex(scope_text, r"(外部|独立).{0,16}(绘图|审美|视觉)")
        self.assertNotRegex(scope_text, r"必须.{0,20}(美观|审美|视觉评分|配色模板)")
        self.assertNotIn("要求生成正式论文图", scope_text)
        self.assertNotIn("必须生成正式论文图", scope_text)
        self.assertNotIn("要求生成论文级图表", scope_text)

    def test_paper_preparation_workspace_prompts_and_templates(self) -> None:
        template_root = PROJECT_ROOT / "templates/paper-preparation"
        expected_templates = {
            "task-brief.md",
            "frozen-inputs.md",
            "chapter-map.md",
            "narrative-spine.md",
            "page-budget.md",
            "chapter-material.md",
            "evidence-review.md",
            "evidence-response.md",
            "notation-registry.md",
            "claim-to-section-map.md",
            "table-and-figure-plan.md",
            "paper-framework.md",
            "competition-review-blind.md",
            "competition-pattern-sweep.md",
            "framework-response.md",
            "competition-review-closure.md",
            "change-request.md",
            "paper-framework-handoff.md",
        }
        self.assertTrue(expected_templates.issubset({path.name for path in template_root.glob("*.md")}))
        for name in expected_templates:
            self.assertIn("最低责任", (template_root / name).read_text(encoding="utf-8"), name)

        with tempfile.TemporaryDirectory() as temp:
            run_dir = Path(temp) / "run"
            initialized = subprocess.run(
                [sys.executable, str(SCRIPTS / "init_run.py"), str(run_dir)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(initialized.returncode, 0, initialized.stderr)
            for relative in (
                "paper-prep/briefs",
                "paper-prep/scope",
                "paper-prep/structure",
                "paper-prep/questions",
                "paper-prep/shared",
                "paper-prep/integration",
                "paper-prep/change-requests",
            ):
                self.assertTrue((run_dir / relative).is_dir(), relative)
            self.assertFalse(any((run_dir / "paper-prep").rglob("*.md")))

            leader = subprocess.run(
                [sys.executable, str(SCRIPTS / "build_prompt.py"), "--paper-prep-leader"],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(leader.returncode, 0, leader.stderr)
            self.assertIn("CP0", leader.stdout)
            self.assertIn("CP6", leader.stdout)

            brief = run_dir / "paper-prep/briefs/CP2-q1.md"
            brief.write_text("# Paper preparation task\n\n整理问题一材料。\n", encoding="utf-8")
            worker = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "build_prompt.py"),
                    "--paper-prep-role",
                    "question_chapter_curator",
                    "--task-brief",
                    str(brief),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(worker.returncode, 0, worker.stderr)
            self.assertIn("论文准备 Worker Base Prompt", worker.stdout)
            self.assertIn("Question Chapter Curator", worker.stdout)
            self.assertIn("任务之外", worker.stdout)

    def test_paper_preparation_stage_is_mechanical(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            run_dir = Path(temp) / "run"
            initialized = subprocess.run(
                [sys.executable, str(SCRIPTS / "init_run.py"), str(run_dir)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(initialized.returncode, 0, initialized.stderr)

            missing = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "check_workspace.py"),
                    str(run_dir),
                    "--stage",
                    "paper-prep",
                    "--json",
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(missing.returncode, 1)
            missing_report = json.loads(missing.stdout)
            self.assertFalse(missing_report["semantic_correctness_checked"])
            self.assertFalse(missing_report["competition_manuscript_quality_checked"])
            self.assertFalse(missing_report["award_distillation_context_isolation_checked"])
            self.assertTrue(
                any("paper-framework-handoff.md" in error for error in missing_report["errors"]),
                missing_report["errors"],
            )

            required_files = (
                "validation/validation-handoff.md",
                "validation/claims/claim-evidence-map.md",
                "figure-prep/figure-preparation-handoff.md",
                "paper-prep/scope/frozen-inputs.md",
                "paper-prep/structure/chapter-map-v0.md",
                "paper-prep/structure/chapter-map-v1.md",
                "paper-prep/structure/narrative-spine.md",
                "paper-prep/structure/page-budget.md",
                "paper-prep/shared/notation-registry.md",
                "paper-prep/shared/claim-to-section-map.md",
                "paper-prep/shared/table-and-figure-plan.md",
                "paper-prep/integration/paper-framework-v1.md",
                "paper-prep/integration/competition-review-blind.md",
                "paper-prep/integration/competition-review-pattern-sweep.md",
                "paper-prep/integration/framework-response.md",
                "paper-prep/integration/paper-framework-v2.md",
                "paper-prep/integration/competition-review-closure.md",
                "paper-prep/paper-framework-handoff.md",
                "paper-prep/questions/q1/chapter-material-v1.md",
                "paper-prep/questions/q1/evidence-review.md",
                "paper-prep/questions/q1/evidence-response.md",
                "paper-prep/questions/q1/chapter-material-v2.md",
                "paper-prep/questions/q2/chapter-material-v1.md",
                "paper-prep/questions/q2/evidence-review.md",
                "paper-prep/questions/q2/evidence-response.md",
                "paper-prep/questions/q2/chapter-material-v2.md",
            )
            for relative in required_files:
                path = run_dir / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("opaque mechanical fixture\n", encoding="utf-8")

            checked = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "check_workspace.py"),
                    str(run_dir),
                    "--stage",
                    "paper-prep",
                    "--json",
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
            report = json.loads(checked.stdout)
            self.assertEqual(report["errors"], [])
            self.assertFalse(report["markdown_content_parsed"])
            self.assertFalse(report["competition_manuscript_quality_checked"])

    def test_paper_preparation_team_scope_and_review_isolation(self) -> None:
        team = json.loads(
            (PROJECT_ROOT / "Workflow/paper-preparation-team.json").read_text(encoding="utf-8")
        )
        self.assertEqual(team["execution"]["mode"], "leader_with_native_subagents")
        self.assertFalse(team["execution"]["external_orchestrator_required"])
        self.assertNotIn("worker_slots", team["execution"])
        self.assertTrue(team["branch_policy"]["no_fixed_numeric_worker_cap"])
        self.assertTrue(team["branch_policy"]["question_tasks_may_run_in_parallel"])
        self.assertTrue(team["context_isolation"]["award_patterns_are_not_evidence"])
        self.assertIn("award_paper_distillation", team["context_isolation"]["competition_blind_forbidden"])

        expected_roles = {
            "paper_structure_architect",
            "question_chapter_curator",
            "chapter_evidence_auditor",
            "chapter_curator_response",
            "paper_framework_integrator",
            "competition_manuscript_reviewer",
            "paper_framework_response",
        }
        self.assertEqual(expected_roles, set(team["roles"]))
        for role in team["roles"].values():
            self.assertTrue((PROJECT_ROOT / role["prompt"]).is_file(), role["prompt"])

        reviewer = (
            PROJECT_ROOT / "prompts/paper-preparation/competition-manuscript-reviewer.md"
        ).read_text(encoding="utf-8")
        blind_index = reviewer.index("第一遍盲审")
        second_index = reviewer.index("第二遍模式扫描")
        self.assertLess(blind_index, second_index)
        self.assertIn("盲审落盘", reviewer)
        self.assertIn("run", reviewer)
        self.assertIn("debug", reviewer)

        scope_text = "\n".join(
            [
                (PROJECT_ROOT / "Workflow/paper-preparation.md").read_text(encoding="utf-8"),
                *[
                    (PROJECT_ROOT / role["prompt"]).read_text(encoding="utf-8")
                    for role in team["roles"].values()
                ],
            ]
        )
        self.assertRegex(scope_text, r"不.{0,12}(生成|写).{0,12}(完整论文|正式论文)")
        self.assertIn("Evidence Auditor", scope_text)
        self.assertIn("Competition Manuscript Reviewer", scope_text)
        figure_team = json.loads(
            (PROJECT_ROOT / "Workflow/figure-preparation-team.json").read_text(encoding="utf-8")
        )
        self.assertIn(
            "paper-prep/structure/chapter-map-v0.md when CP1 completes",
            figure_team["scope"]["inputs"],
        )

    def test_paper_writing_workspace_prompts_and_templates(self) -> None:
        template_root = PROJECT_ROOT / "templates/paper-writing"
        expected_templates = {
            "task-brief.md",
            "frozen-inputs.md",
            "writing-plan.md",
            "section-contracts.md",
            "prose-boundary.md",
            "figure-table-slots.md",
            "question-section.md",
            "section-fact-response.md",
            "full-paper.md",
            "fact-consistency-review.md",
            "competition-expression-review.md",
            "coherence-review.md",
            "ai-prose-review.md",
            "fact-response.md",
            "language-review-response.md",
            "closure-review.md",
            "change-request.md",
            "formal-paper-handoff.md",
        }
        self.assertTrue(expected_templates.issubset({path.name for path in template_root.glob("*.md")}))
        for name in expected_templates:
            self.assertIn("最低责任", (template_root / name).read_text(encoding="utf-8"), name)

        with tempfile.TemporaryDirectory() as temp:
            run_dir = Path(temp) / "run"
            initialized = subprocess.run(
                [sys.executable, str(SCRIPTS / "init_run.py"), str(run_dir)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(initialized.returncode, 0, initialized.stderr)
            for relative in (
                "paper-writing/briefs",
                "paper-writing/scope",
                "paper-writing/plan",
                "paper-writing/sections",
                "paper-writing/manuscript",
                "paper-writing/reviews/closure",
                "paper-writing/responses",
                "paper-writing/change-requests",
            ):
                self.assertTrue((run_dir / relative).is_dir(), relative)
            self.assertFalse(any((run_dir / "paper-writing").rglob("*.md")))

            leader = subprocess.run(
                [sys.executable, str(SCRIPTS / "build_prompt.py"), "--paper-writing-leader"],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(leader.returncode, 0, leader.stderr)
            self.assertIn("唯一全文作者", leader.stdout)
            self.assertIn("PW7", leader.stdout)

            brief = run_dir / "paper-writing/briefs/PW2-q1.md"
            brief.write_text("# Writing task\n\n写问题一正式章节。\n", encoding="utf-8")
            writer = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "build_prompt.py"),
                    "--paper-writing-role",
                    "question_manuscript_writer",
                    "--task-brief",
                    str(brief),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(writer.returncode, 0, writer.stderr)
            self.assertIn("正式论文写作 Worker Base Prompt", writer.stdout)
            self.assertIn("Question Manuscript Writer", writer.stdout)

    def test_paper_writing_stage_is_mechanical(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            run_dir = Path(temp) / "run"
            initialized = subprocess.run(
                [sys.executable, str(SCRIPTS / "init_run.py"), str(run_dir)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(initialized.returncode, 0, initialized.stderr)

            missing = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "check_workspace.py"),
                    str(run_dir),
                    "--stage",
                    "paper-writing",
                    "--json",
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(missing.returncode, 1)
            missing_report = json.loads(missing.stdout)
            self.assertFalse(missing_report["semantic_correctness_checked"])
            self.assertFalse(missing_report["ai_prose_quality_checked"])
            self.assertFalse(missing_report["reviewer_independence_checked"])
            self.assertTrue(
                any("formal-paper-handoff.md" in error for error in missing_report["errors"]),
                missing_report["errors"],
            )

            required_files = (
                "validation/claims/claim-evidence-map.md",
                "figure-prep/figure-preparation-handoff.md",
                "paper-prep/paper-framework-handoff.md",
                "paper-writing/scope/frozen-inputs.md",
                "paper-writing/plan/writing-plan.md",
                "paper-writing/plan/section-contracts.md",
                "paper-writing/plan/prose-boundary.md",
                "paper-writing/plan/figure-table-slots.md",
                "paper-writing/manuscript/full-paper-v1.md",
                "paper-writing/manuscript/full-paper-v2.md",
                "paper-writing/manuscript/full-paper-v3.md",
                "paper-writing/manuscript/final-paper.md",
                "paper-writing/reviews/fact-consistency-review.md",
                "paper-writing/reviews/competition-expression-review.md",
                "paper-writing/reviews/full-paper-coherence-review.md",
                "paper-writing/reviews/ai-prose-review.md",
                "paper-writing/reviews/closure/fact-closure.md",
                "paper-writing/reviews/closure/competition-expression-closure.md",
                "paper-writing/reviews/closure/coherence-closure.md",
                "paper-writing/reviews/closure/ai-prose-closure.md",
                "paper-writing/responses/fact-response.md",
                "paper-writing/responses/language-review-response.md",
                "paper-writing/formal-paper-handoff.md",
                "paper-writing/sections/q1/section-v1.md",
                "paper-writing/sections/q1/section-fact-response.md",
                "paper-writing/sections/q1/section-v2.md",
                "paper-writing/sections/q2/section-v1.md",
                "paper-writing/sections/q2/section-fact-response.md",
                "paper-writing/sections/q2/section-v2.md",
            )
            for relative in required_files:
                path = run_dir / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("opaque mechanical fixture\n", encoding="utf-8")

            checked = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "check_workspace.py"),
                    str(run_dir),
                    "--stage",
                    "paper-writing",
                    "--json",
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
            report = json.loads(checked.stdout)
            self.assertEqual(report["errors"], [])
            self.assertFalse(report["markdown_content_parsed"])
            self.assertFalse(report["ai_prose_quality_checked"])

    def test_paper_writing_team_ownership_and_review_isolation(self) -> None:
        team = json.loads(
            (PROJECT_ROOT / "Workflow/paper-writing-team.json").read_text(encoding="utf-8")
        )
        self.assertEqual(team["execution"]["leader"], "current_primary_agent_is_unique_full_manuscript_author")
        self.assertFalse(team["execution"]["reviewers_may_edit_manuscript"])
        self.assertEqual(team["scope"]["canonical_manuscript_format"], "markdown")
        self.assertIn("mechanical_style_linter", team["scope"]["out_of_scope"])
        self.assertIn("automatic_rewriting", team["scope"]["out_of_scope"])
        self.assertTrue(team["review_isolation"]["pw5_reviewers_read_same_frozen_v2"])
        self.assertTrue(team["review_isolation"]["peer_reviews_hidden"])
        self.assertTrue(team["branch_policy"]["leader_is_unique_manuscript_owner"])

        expected_roles = {
            "question_manuscript_writer",
            "question_manuscript_response",
            "full_paper_fact_auditor",
            "competition_expression_reviewer",
            "full_paper_coherence_reviewer",
            "ai_prose_auditor",
        }
        self.assertEqual(expected_roles, set(team["roles"]))
        for role in team["roles"].values():
            self.assertTrue((PROJECT_ROOT / role["prompt"]).is_file(), role["prompt"])
        for reviewer_name in (
            "full_paper_fact_auditor",
            "competition_expression_reviewer",
            "full_paper_coherence_reviewer",
            "ai_prose_auditor",
        ):
            self.assertTrue(team["roles"][reviewer_name]["review_only"])

        phase_ids = [phase["id"] for phase in team["phases"]]
        self.assertLess(phase_ids.index("PW4"), phase_ids.index("PW5"))
        self.assertEqual(
            next(phase for phase in team["phases"] if phase["id"] == "PW5")["frozen_input"],
            "manuscript/full-paper-v2.md",
        )

        ai_prompt = (PROJECT_ROOT / "prompts/paper-writing/ai-prose-auditor.md").read_text(
            encoding="utf-8"
        )
        for marker in ("首先", "此外", "比喻", "口水话", "run", "debug", "数学术语"):
            self.assertIn(marker, ai_prompt)
        self.assertIn("不给 AI 分数", ai_prompt)
        self.assertIn("不直接修改正文", ai_prompt)
        self.assertIn("不要把必要技术术语", ai_prompt)

    def test_final_delivery_workspace_prompts_templates_and_team(self) -> None:
        template_root = PROJECT_ROOT / "templates/final-delivery"
        expected_templates = {
            "task-brief.md",
            "frozen-inputs.md",
            "result-data-manifest.md",
            "source-code-manifest.md",
            "execution-order.md",
            "source-code.md",
            "supporting-materials.md",
            "typesetting-memo.md",
            "preflight-report.md",
            "candidate-snapshot.md",
            "layout-and-compliance-review.md",
            "answer-relevance-review.md",
            "prose-and-engineering-style-review.md",
            "delivery-evidence-review.md",
            "end-to-end-consistency-review.md",
            "issue-index.md",
            "human-finalization-guide.md",
            "submission-checklist.md",
            "final-delivery-handoff.md",
        }
        self.assertTrue(expected_templates.issubset({path.name for path in template_root.glob("*.md")}))
        for name in expected_templates:
            self.assertIn("最低责任", (template_root / name).read_text(encoding="utf-8"), name)

        team = json.loads(
            (PROJECT_ROOT / "Workflow/final-delivery-team.json").read_text(encoding="utf-8")
        )
        self.assertEqual(team["scope"]["terminal_status"], "AWAITING_HUMAN_FINALIZATION")
        self.assertTrue(team["execution"]["post_review_agent_revision_forbidden"])
        self.assertTrue(team["branch_policy"]["no_agent_edits_after_fd4_starts"])
        self.assertNotIn("response", " ".join(team["roles"]))
        for role in team["roles"].values():
            self.assertTrue((PROJECT_ROOT / role["prompt"]).is_file(), role["prompt"])
        for reviewer_name in (
            "layout_compliance_auditor",
            "answer_relevance_reviewer",
            "prose_engineering_style_auditor",
            "delivery_evidence_auditor",
            "end_to_end_consistency_auditor",
        ):
            self.assertTrue(team["roles"][reviewer_name]["review_only"])
        self.assertTrue(team["roles"]["end_to_end_consistency_auditor"]["fresh_context_required"])
        self.assertEqual(
            next(phase for phase in team["phases"] if phase["id"] == "FD4")["dispatch"],
            "five_new_isolated_terminal_reviewers",
        )

        with tempfile.TemporaryDirectory() as temp:
            run_dir = Path(temp) / "run"
            initialized = subprocess.run(
                [sys.executable, str(SCRIPTS / "init_run.py"), str(run_dir)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(initialized.returncode, 0, initialized.stderr)
            for relative in (
                "final-delivery/briefs",
                "final-delivery/scope",
                "final-delivery/source",
                "final-delivery/supporting-materials/results",
                "final-delivery/candidate",
                "final-delivery/reviews",
                "final-delivery/human-review",
            ):
                self.assertTrue((run_dir / relative).is_dir(), relative)
            self.assertFalse(any((run_dir / "final-delivery").rglob("*.md")))

            leader = subprocess.run(
                [sys.executable, str(SCRIPTS / "build_prompt.py"), "--final-delivery-leader"],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(leader.returncode, 0, leader.stderr)
            self.assertIn("FD0–FD7", leader.stdout)
            self.assertIn("不再修改", leader.stdout)

            brief = run_dir / "final-delivery/briefs/FD1-support.md"
            brief.write_text("# FD1\n\n整理结果数据和运行脚本源码。\n", encoding="utf-8")
            curator = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "build_prompt.py"),
                    "--final-delivery-role",
                    "supporting_material_curator",
                    "--task-brief",
                    str(brief),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(curator.returncode, 0, curator.stderr)
            self.assertIn("完整粘贴", curator.stdout)
            self.assertIn("最终排版与终审 Worker Base Prompt", curator.stdout)

            prose = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "build_prompt.py"),
                    "--final-delivery-role",
                    "prose_engineering_style_auditor",
                    "--task-brief",
                    str(brief),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(prose.returncode, 0, prose.stderr)
            for marker in ("首先", "比喻", "口水话", "pipeline", "不给 AI 分数", "不得直接修改"):
                self.assertIn(marker, prose.stdout)

            chain = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "build_prompt.py"),
                    "--final-delivery-role",
                    "end_to_end_consistency_auditor",
                    "--task-brief",
                    str(brief),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(chain.returncode, 0, chain.stderr)
            for marker in ("fresh-context", "题意", "路线", "数据", "验证", "最早产生偏差"):
                self.assertIn(marker, chain.stdout)

    def test_final_delivery_stage_is_mechanical_and_terminal(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            run_dir = Path(temp) / "run"
            initialized = subprocess.run(
                [sys.executable, str(SCRIPTS / "init_run.py"), str(run_dir)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(initialized.returncode, 0, initialized.stderr)

            missing = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "check_workspace.py"),
                    str(run_dir),
                    "--stage",
                    "final-delivery",
                    "--json",
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(missing.returncode, 1)
            missing_report = json.loads(missing.stdout)
            self.assertFalse(missing_report["layout_quality_checked"])
            self.assertFalse(missing_report["answer_relevance_checked"])
            self.assertTrue(
                any("final-delivery-handoff.md" in error for error in missing_report["errors"]),
                missing_report["errors"],
            )
            self.assertTrue(
                any("end-to-end-consistency-review.md" in error for error in missing_report["errors"]),
                missing_report["errors"],
            )

            required_files = (
                "synthesis/problem-baseline.md",
                "routes/route-handoff.md",
                "data/data-handoff.md",
                "modeling/model-handoff.md",
                "validation/validation-handoff.md",
                "validation/claims/claim-evidence-map.md",
                "paper-writing/manuscript/final-paper.md",
                "paper-writing/formal-paper-handoff.md",
                "figure-prep/figure-preparation-handoff.md",
                "paper-prep/paper-framework-handoff.md",
                "final-delivery/scope/frozen-inputs.md",
                "final-delivery/scope/candidate-snapshot.md",
                "final-delivery/source/submission-source.md",
                "final-delivery/source/supporting-materials.md",
                "final-delivery/supporting-materials/result-data-manifest.md",
                "final-delivery/supporting-materials/source-code-manifest.md",
                "final-delivery/supporting-materials/execution-order.md",
                "final-delivery/supporting-materials/source-code.md",
                "final-delivery/supporting-materials/supporting-materials.md",
                "final-delivery/supporting-materials/results/final-results.csv",
                "final-delivery/candidate/paper.pdf",
                "final-delivery/candidate/paper.docx",
                "final-delivery/candidate/supporting-materials.pdf",
                "final-delivery/preflight-report.md",
                "final-delivery/typesetting-memo.md",
                "final-delivery/reviews/layout-and-compliance-review.md",
                "final-delivery/reviews/answer-relevance-review.md",
                "final-delivery/reviews/prose-and-engineering-style-review.md",
                "final-delivery/reviews/delivery-evidence-review.md",
                "final-delivery/reviews/end-to-end-consistency-review.md",
                "final-delivery/human-review/issue-index.md",
                "final-delivery/human-review/human-finalization-guide.md",
                "final-delivery/submission-checklist.md",
                "final-delivery/final-delivery-handoff.md",
            )
            for relative in required_files:
                path = run_dir / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("opaque mechanical fixture\n", encoding="utf-8")

            checked = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "check_workspace.py"),
                    str(run_dir),
                    "--stage",
                    "final-delivery",
                    "--json",
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
            report = json.loads(checked.stdout)
            self.assertEqual(report["errors"], [])
            self.assertFalse(report["markdown_content_parsed"])
            self.assertFalse(report["ai_prose_quality_checked"])
            self.assertFalse(report["delivery_evidence_semantics_checked"])
            self.assertFalse(report["end_to_end_consistency_semantics_checked"])

            forbidden = run_dir / "final-delivery/responses/automatic-rewrite.md"
            forbidden.parent.mkdir(parents=True, exist_ok=True)
            forbidden.write_text("forbidden post-review rewrite\n", encoding="utf-8")
            rejected = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "check_workspace.py"),
                    str(run_dir),
                    "--stage",
                    "final-delivery",
                    "--json",
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(rejected.returncode, 1)
            rejected_report = json.loads(rejected.stdout)
            self.assertTrue(
                any("response or closure" in error for error in rejected_report["errors"]),
                rejected_report["errors"],
            )

    def test_refuses_nonempty_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            run_dir = Path(temp) / "run"
            run_dir.mkdir()
            owned = run_dir / "owned.txt"
            owned.write_text("keep", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "init_run.py"), str(run_dir)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 2)
            self.assertEqual(owned.read_text(encoding="utf-8"), "keep")

    def test_native_subagent_team_configuration_and_prompts(self) -> None:
        team = json.loads((PROJECT_ROOT / "Workflow/team.json").read_text(encoding="utf-8"))
        self.assertEqual(team["execution"]["mode"], "leader_with_native_subagents")
        self.assertFalse(team["execution"]["external_orchestrator_required"])
        self.assertEqual(team["execution"]["worker_slots"], 3)
        self.assertIn("original_judgment_reviewer", team["roles"])
        self.assertIn("route_proposer_responder", team["roles"])
        for role in team["roles"].values():
            self.assertTrue((PROJECT_ROOT / role["prompt"]).is_file())

        agents = (PROJECT_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("创建新的 subagent", agents)
        self.assertIn("原 subagent", agents)
        self.assertIn("W3R", agents)
        self.assertIn("W5C", agents)

    def test_leader_router_and_workflow_list_every_role_prompt(self) -> None:
        workflow = (PROJECT_ROOT / "Workflow/README.md").read_text(encoding="utf-8")
        agents = (PROJECT_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        front_team = json.loads((PROJECT_ROOT / "Workflow/team.json").read_text(encoding="utf-8"))
        data_team = json.loads((PROJECT_ROOT / "Workflow/data-team.json").read_text(encoding="utf-8"))
        paper_team = json.loads(
            (PROJECT_ROOT / "Workflow/paper-preparation-team.json").read_text(encoding="utf-8")
        )
        writing_team = json.loads(
            (PROJECT_ROOT / "Workflow/paper-writing-team.json").read_text(encoding="utf-8")
        )

        prompt_paths = {role["prompt"] for role in front_team["roles"].values()}
        prompt_paths.add(data_team["execution"]["worker_base_prompt"])
        prompt_paths.update(role["prompt"] for role in data_team["roles"].values())
        prompt_paths.add(paper_team["execution"]["worker_base_prompt"])
        prompt_paths.update(role["prompt"] for role in paper_team["roles"].values())
        prompt_paths.add(writing_team["execution"]["worker_base_prompt"])
        prompt_paths.update(role["prompt"] for role in writing_team["roles"].values())

        for prompt_path in sorted(prompt_paths):
            self.assertTrue((PROJECT_ROOT / prompt_path).is_file(), prompt_path)
            self.assertIn(prompt_path, workflow, prompt_path)

        routed_paths = {
            "Workflow/README.md",
            "Workflow/team.json",
            "Workflow/data-team.json",
            "Workflow/paper-preparation-team.json",
            "Workflow/paper-writing-team.json",
            "prompts/leader.md",
            "prompts/worker-base.md",
            "prompts/data-engineering/leader.md",
            "prompts/data-engineering/worker-base.md",
            "prompts/paper-preparation/leader.md",
            "prompts/paper-preparation/worker-base.md",
            "prompts/paper-writing/leader.md",
            "prompts/paper-writing/worker-base.md",
            "templates/task-brief.md",
            "templates/data-engineering/task-brief.md",
            "templates/paper-preparation/task-brief.md",
            "templates/paper-writing/task-brief.md",
        }
        for routed_path in sorted(routed_paths):
            self.assertIn(routed_path, agents, routed_path)

        self.assertIn("详细波次、角色输入、prompt 路径和输出路径以 `Workflow/README.md` 为准", agents)
        self.assertIn("本文是 Leader 的逐波调度手册", workflow)


if __name__ == "__main__":
    unittest.main()
