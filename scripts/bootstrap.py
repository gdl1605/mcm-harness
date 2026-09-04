#!/usr/bin/env python3
"""Prepare a local workspace; never start agents, install tools, or reset a run."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from init_run import mcm_skill_snapshot, sha256_file, utc_now


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SUFFIXES = {
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".csv", ".tsv",
    ".txt", ".md", ".json", ".png", ".jpg", ".jpeg", ".zip", ".7z",
}
SOURCE_QUESTION = "请提供题目文件和全部数据附件的本地路径，或上传文件/提供可访问下载链接；如果没有独立数据附件，请说明。"


def read_object(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object: {path}")
    return value


def run_tool(name: str, *args: str) -> str:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / name), *args],
        text=True, capture_output=True, check=False,
    )
    if result.returncode:
        raise ValueError(f"{name} failed: {result.stderr.strip() or result.stdout.strip()}")
    return result.stdout


def external_requirements() -> dict:
    """Local file/hash checks only, not claims about platform availability."""
    skills = {}
    for name in ("nature-figure", "ssci-plots"):
        lock = read_object(ROOT / "Workflow" / f"{name}-skill.lock.json")
        entry = ROOT / ".agents" / "skills" / name / "SKILL.md"
        skills[name] = (
            "missing" if not entry.is_file() else
            "hash_matches_lock" if sha256_file(entry) == lock["skill_md_sha256"] else
            "hash_mismatch"
        )
    return {
        "local_figure_skills": skills,
        "agent_must_verify": [
            "native subagents and file/command permissions",
            "source reading and literature retrieval tools before their stages",
            "visualize-data and gpt-5.6-sol/high availability before formal figures",
        ],
        "full_workflow_ready": False,
    }


def discover_sources(directory: Path) -> tuple[list[Path], list[str]]:
    if directory.is_symlink():
        raise ValueError("raw-sources must not be a symlink; provide explicit --source paths")
    directory.mkdir(exist_ok=True)
    sources, skipped = [], []
    for path in sorted(directory.iterdir()):
        if path.name.startswith((".", "~$")):
            continue
        if path.is_symlink():
            raise ValueError(f"automatic source discovery refuses symlinks: {path.name}")
        if path.is_file() and path.suffix.lower() in SOURCE_SUFFIXES:
            sources.append(path.resolve())
        else:
            skipped.append(path.name)
    return sources, skipped


def bootstrap(args: argparse.Namespace) -> dict:
    if sys.version_info < (3, 10):
        raise ValueError("Python 3.10+ is required")
    # Fail before initializing anything when the bundled instructions are incomplete.
    mcm_skill_snapshot(utc_now())
    requirements = external_requirements()
    raw = ROOT / "raw-sources"
    run_path = args.run_dir or ROOT / "run"
    if run_path.is_symlink():
        raise ValueError("run directory must not be a symlink")
    run_dir = run_path.resolve()
    if run_dir == ROOT or run_dir in ROOT.parents:
        raise ValueError("run directory must not contain the repository")
    if run_dir.exists() and not run_dir.is_dir():
        raise ValueError(f"run path is not a directory: {run_dir}")
    if args.source:
        sources = sorted({path.resolve() for path in args.source})
        skipped = []
    else:
        sources, skipped = discover_sources(raw)
    for source in sources:
        if not source.is_file():
            raise ValueError(f"source is not an existing file: {source}")
        if run_dir == source or run_dir in source.parents:
            raise ValueError("source files must be outside the run directory")

    report = {
        "metadata_only": True,
        "run_dir": str(run_dir),
        "source_directory": str(raw),
        "skipped_source_entries": skipped,
        "requirements": requirements,
        "semantic_correctness_checked": False,
        "source_completeness_checked": False,
        "registered_source_paths": [],
        "script_preparation_only": True,
        "setup_only_requested": args.setup_only,
    }
    if run_dir.exists() and any(run_dir.iterdir()):
        # Existing runs (including progressed ones) are strictly read-only.
        state = read_object(run_dir / "state/run-state.json")
        manifest = read_object(run_dir / "inputs/source-manifest.json")
        if not state.get("run_id") or not state.get("phase"):
            raise ValueError("existing run has invalid identity or phase; refusing to reset it")
        materials = manifest.get("materials")
        if not isinstance(materials, list) or not materials:
            raise ValueError("existing run has no registered sources; choose a new --run-dir")
        registered = set()
        for item in materials:
            if not isinstance(item, dict) or not isinstance(item.get("path"), str):
                raise ValueError("invalid source record in existing run")
            source = Path(item["path"])
            if not source.is_absolute():
                raise ValueError("existing source path must be absolute")
            if not source.is_file() or sha256_file(source) != item.get("sha256"):
                raise ValueError(f"registered source is missing or changed: {source}")
            registered.add(source.resolve())
        if (args.source or sources) and set(sources) != registered:
            raise ValueError("source set changed; keep the old run and choose a new --run-dir")
        if args.title is not None and args.title != state.get("title"):
            raise ValueError("existing run title differs; initialization will not rename it")
        read_object(run_dir / "state/mcm-skill-snapshot.json")
        report.update(status="EXISTING_RUN", run_id=state["run_id"], phase=state["phase"])
    elif not sources:
        report.update(status="AWAITING_SOURCES", registered_sources=0,
                      next_action="ASK_FOR_PROBLEM_AND_DATA_LOCATIONS", user_question=SOURCE_QUESTION)
        return report
    elif args.prepare_only:
        report.update(status="AWAITING_SOURCE_REVIEW", registered_sources=0,
                      candidate_source_paths=[str(path) for path in sources],
                      next_action="REVIEW_PROBLEM_AND_DATA_COVERAGE")
        return report
    else:
        command = [str(run_dir), "--title", args.title or "C problem"]
        for source in sources:
            command.extend(["--source", str(source)])
        run_tool("init_run.py", *command)
        state = read_object(run_dir / "state/run-state.json")
        report.update(status="INITIALIZED", run_id=state["run_id"], phase=state["phase"])

    checked = json.loads(run_tool("check_workspace.py", str(run_dir), "--stage", "init", "--json"))
    if checked.get("embedded_mcm_skill_drift_detected"):
        raise ValueError("embedded mcm changed since initialization; keep the run and review the drift")
    report["warnings"] = checked.get("warnings", [])
    materials = read_object(run_dir / "inputs/source-manifest.json")["materials"]
    report["registered_sources"] = len(materials)
    report["registered_source_paths"] = [item["path"] for item in materials]
    # This is an Agent handoff, not Python orchestration or a semantic approval.
    report["agent_continuation_requires"] = ["complete_readable_sources", "current_stage_capabilities"]
    if args.setup_only:
        report["next_action"] = "STOP_AFTER_SETUP"
    elif state["phase"] in ("H1", "AWAITING_HUMAN_MODEL_DECISION"):
        report["next_action"] = "WAIT_FOR_HUMAN_MODEL_DECISION"
    elif state["phase"] == "AWAITING_HUMAN_FINALIZATION":
        report["next_action"] = "WAIT_FOR_HUMAN_FINALIZATION"
    elif report["status"] == "INITIALIZED":
        report["next_action"] = "START_MATERIAL_READING_AND_ROUTE_TOURNAMENT"
    else:
        report["next_action"] = "REVIEW_EXISTING_PHASE_AND_RESUME_PRE_H1_ONLY"
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, help="Default: repository run/; never overwritten")
    parser.add_argument("--source", type=Path, action="append", default=[], help="Repeat to use explicit files instead of raw-sources/")
    parser.add_argument("--title", help="Title for a new run")
    parser.add_argument("--prepare-only", action="store_true", help="List candidate sources without creating a new run; existing runs remain read-only")
    parser.add_argument("--setup-only", action="store_true", help="User explicitly requested setup without subsequent Agent reading/route exploration")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        report = bootstrap(args)
        code = 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        report = {"status": "BLOCKED", "error": str(exc), "script_preparation_only": True}
        code = 2
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif code:
        print(f"Bootstrap blocked: {report['error']}", file=sys.stderr)
    else:
        print(f"Bootstrap: {report['status']}")
        print(f"运行目录: {report['run_dir']}")
        print(f"已登记材料: {report['registered_sources']}")
        if report["status"] == "AWAITING_SOURCES":
            print(report["user_question"])
            print(f"也可放入 {report['source_directory']}；Agent 收到材料后继续初始化，无需重复发 init。")
        elif report["status"] == "AWAITING_SOURCE_REVIEW":
            print("候选材料（尚未冻结，请核对完整题面与全部数据附件）：")
            for path in report["candidate_source_paths"]:
                print(f"  {path}")
            print("核对齐备后，去掉 --prepare-only，并用 --source 显式登记这批文件。")
        else:
            print(f"当前阶段: {report['phase']}；已有记录不会重置，脚本未调度 Agent。")
            print("已登记路径：")
            for path in report["registered_source_paths"]:
                print(f"  {path}")
            print("文件登记不等于材料齐备；Agent 仍须核对题面和数据附件。")
            guidance = {
                "STOP_AFTER_SETUP": "按用户要求只做准备，暂不开始材料阅读或路线竞标。",
                "WAIT_FOR_HUMAN_MODEL_DECISION": "当前在 H1，继续等待真实模型选择，不自动放行。",
                "WAIT_FOR_HUMAN_FINALIZATION": "保持最终人工接管，不自动修改或投稿。",
                "START_MATERIAL_READING_AND_ROUTE_TOURNAMENT": "材料与当前能力确认后，Agent 自动开始材料阅读与模型路线竞标，到 H1 等待用户选模型，无需另发启动 prompt。",
                "REVIEW_EXISTING_PHASE_AND_RESUME_PRE_H1_ONLY": "Agent 先核对现有阶段和活动任务，仅续接未完成的前半程；不重跑、不越过人工 gate 或自动恢复后半程。",
            }
            print(guidance[report["next_action"]])
        if report["skipped_source_entries"]:
            print("未自动登记（请人工确认）: " + ", ".join(report["skipped_source_entries"]))
        for name, status in report["requirements"]["local_figure_skills"].items():
            print(f"后续绘图依赖 {name}: {status}")
        print("Agent 仍需核对平台能力；Bootstrap 不安装依赖、不确认人工 gate。")
        for warning in report.get("warnings", []):
            print(f"WARN: {warning}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
