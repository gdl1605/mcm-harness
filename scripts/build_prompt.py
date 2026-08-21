#!/usr/bin/env python3
"""Combine the worker base prompt, a role prompt, and an open Markdown task brief."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROMPT_ROOT = PROJECT_ROOT / "prompts"
ROLE_ROOT = PROMPT_ROOT / "roles"
DATA_PROMPT_ROOT = PROMPT_ROOT / "data-engineering"
MODEL_PROMPT_ROOT = PROMPT_ROOT / "modeling"
VALIDATION_PROMPT_ROOT = PROMPT_ROOT / "validation"
FIGURE_PROMPT_ROOT = PROMPT_ROOT / "figure-preparation"
PAPER_PROMPT_ROOT = PROMPT_ROOT / "paper-preparation"
PAPER_WRITING_PROMPT_ROOT = PROMPT_ROOT / "paper-writing"
FINAL_DELIVERY_PROMPT_ROOT = PROMPT_ROOT / "final-delivery"
LITERATURE_PROMPT_ROOT = PROMPT_ROOT / "literature"
DATA_ROLE_ALIASES = {
    "data_contract_architect": "data-contract-architect",
    "data_profiler": "data-profiler",
    "data_risk_reviewer": "data-risk-reviewer",
    "data_pipeline_implementer": "data-pipeline-builder",
    "reproducibility_quality_validator": "data-repro-validator",
    "interquestion_interface_reviewer": "data-interface-reviewer",
    "data_builder_response": "data-builder-response",
    "data_builder_responder": "data-builder-response",
}
MODEL_ROLE_ALIASES = {
    "mathematical_specification_architect": "mathematical-specification-architect",
    "computational_path_planner": "computational-path-planner",
    "structural_challenger": "structural-challenger",
    "model_builder": "model-builder",
    "build_result_diagnostician": "build-result-diagnostician",
    "model_builder_responder": "model-builder-response",
    "model_builder_response": "model-builder-response",
    "interface_handoff_owner": "interface-handoff",
    "interface_handoff": "interface-handoff",
}
VALIDATION_ROLE_ALIASES = {
    "mathematical_implementation_auditor": "mathematical-implementation-auditor",
    "experimental_evidence_auditor": "experimental-evidence-auditor",
    "reproducibility_interface_auditor": "reproducibility-interface-auditor",
    "integrated_answer_auditor": "integrated-answer-auditor",
    "original_owner_responder": "original-owner-response",
    "original_owner_response": "original-owner-response",
}
FIGURE_ROLE_ALIASES = {
    # Native team configuration uses snake_case keys, while prompt files use
    # the readable kebab-case stem.  Keep both spellings accepted and leave
    # room for additional prompt stems without changing this CLI.
    "question_figure_curator": "question-figure-curator",
    "question_curator": "question-figure-curator",
    # Cross-question/shared results use the same curator contract as a
    # question owner; the team key is an ownership scope, not a separate
    # prompt type.
    "shared_figure_curator": "question-figure-curator",
    "shared_result_curator": "question-figure-curator",
    "figure_evidence_auditor": "figure-evidence-auditor",
    "figure_chapter_integrator": "figure-chapter-integrator",
    "question_curator_response": "question-curator-response",
    "figure_curator_response": "question-curator-response",
}
PAPER_ROLE_ALIASES = {
    "paper_structure_architect": "paper-structure-architect",
    "question_chapter_curator": "question-chapter-curator",
    "chapter_evidence_auditor": "chapter-evidence-auditor",
    "chapter_curator_response": "chapter-curator-response",
    "paper_framework_integrator": "paper-framework-integrator",
    "competition_manuscript_reviewer": "competition-manuscript-reviewer",
    "paper_framework_response": "paper-framework-response",
}
PAPER_WRITING_ROLE_ALIASES = {
    "question_manuscript_writer": "question-manuscript-writer",
    "question_manuscript_response": "question-manuscript-response",
    "full_paper_fact_auditor": "full-paper-fact-auditor",
    "competition_expression_reviewer": "competition-expression-reviewer",
    "full_paper_coherence_reviewer": "full-paper-coherence-reviewer",
    "ai_prose_auditor": "ai-prose-auditor",
}
FINAL_DELIVERY_ROLE_ALIASES = {
    "supporting_material_curator": "supporting-material-curator",
    "submission_typesetter": "submission-typesetter",
    "layout_compliance_auditor": "layout-compliance-auditor",
    "answer_relevance_reviewer": "answer-relevance-reviewer",
    "prose_engineering_style_auditor": "prose-engineering-style-auditor",
    "delivery_evidence_auditor": "delivery-evidence-auditor",
    "end_to_end_consistency_auditor": "end-to-end-consistency-auditor",
}
LITERATURE_ROLE_ALIASES = {
    "route_literature_scout": "route-literature-scout",
    "human_consultation_recorder": "human-consultation-recorder",
    "literature_evidence_auditor": "literature-evidence-auditor",
    "citation_gap_analyst": "citation-gap-analyst",
    "citation_literature_scout": "citation-literature-scout",
    "citation_auditor": "citation-auditor",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def roles() -> list[str]:
    return sorted(path.stem for path in ROLE_ROOT.glob("*.md"))


def data_roles() -> list[str]:
    return sorted(
        path.stem
        for path in DATA_PROMPT_ROOT.glob("*.md")
        if path.stem not in {"leader", "worker-base"}
    )


def data_role_path(name: str) -> Path | None:
    stem = DATA_ROLE_ALIASES.get(name, name.replace("_", "-"))
    path = DATA_PROMPT_ROOT / f"{stem}.md"
    return path if path.is_file() else None


def model_roles() -> list[str]:
    return sorted(
        path.stem
        for path in MODEL_PROMPT_ROOT.glob("*.md")
        if path.stem not in {"leader", "worker-base"}
    )


def model_role_path(name: str) -> Path | None:
    stem = MODEL_ROLE_ALIASES.get(name, name.replace("_", "-"))
    path = MODEL_PROMPT_ROOT / f"{stem}.md"
    return path if path.is_file() else None


def validation_roles() -> list[str]:
    return sorted(
        path.stem
        for path in VALIDATION_PROMPT_ROOT.glob("*.md")
        if path.stem not in {"leader", "worker-base"}
    )


def validation_role_path(name: str) -> Path | None:
    stem = VALIDATION_ROLE_ALIASES.get(name, name.replace("_", "-"))
    path = VALIDATION_PROMPT_ROOT / f"{stem}.md"
    return path if path.is_file() else None


def figure_roles() -> list[str]:
    """Return available figure role prompt stems, excluding base prompts."""

    return sorted(
        path.stem
        for path in FIGURE_PROMPT_ROOT.glob("*.md")
        if path.stem not in {"leader", "worker-base"}
    )


def figure_role_path(name: str) -> Path | None:
    """Resolve a figure role by prompt stem or native team role key."""

    raw = name.strip()
    candidates = [
        FIGURE_ROLE_ALIASES.get(raw),
        raw,
        raw.replace("_", "-"),
    ]
    for stem in candidates:
        if not stem:
            continue
        path = FIGURE_PROMPT_ROOT / f"{stem}.md"
        if path.is_file():
            return path
    return None


def paper_roles() -> list[str]:
    """Return available paper-preparation role prompt stems."""

    return sorted(
        path.stem
        for path in PAPER_PROMPT_ROOT.glob("*.md")
        if path.stem not in {"leader", "worker-base"}
    )


def paper_role_path(name: str) -> Path | None:
    """Resolve a paper-preparation role by prompt stem or team key."""

    raw = name.strip()
    candidates = [PAPER_ROLE_ALIASES.get(raw), raw, raw.replace("_", "-")]
    for stem in candidates:
        if not stem:
            continue
        path = PAPER_PROMPT_ROOT / f"{stem}.md"
        if path.is_file():
            return path
    return None


def paper_writing_roles() -> list[str]:
    """Return available formal paper-writing role prompt stems."""

    return sorted(
        path.stem
        for path in PAPER_WRITING_PROMPT_ROOT.glob("*.md")
        if path.stem not in {"leader", "worker-base"}
    )


def paper_writing_role_path(name: str) -> Path | None:
    """Resolve a paper-writing role by prompt stem or team key."""

    raw = name.strip()
    candidates = [PAPER_WRITING_ROLE_ALIASES.get(raw), raw, raw.replace("_", "-")]
    for stem in candidates:
        if not stem:
            continue
        path = PAPER_WRITING_PROMPT_ROOT / f"{stem}.md"
        if path.is_file():
            return path
    return None


def final_delivery_roles() -> list[str]:
    """Return available final-delivery role prompt stems."""

    return sorted(
        path.stem
        for path in FINAL_DELIVERY_PROMPT_ROOT.glob("*.md")
        if path.stem not in {"leader", "worker-base"}
    )


def final_delivery_role_path(name: str) -> Path | None:
    """Resolve a final-delivery role by prompt stem or team key."""

    raw = name.strip()
    candidates = [FINAL_DELIVERY_ROLE_ALIASES.get(raw), raw, raw.replace("_", "-")]
    for stem in candidates:
        if not stem:
            continue
        path = FINAL_DELIVERY_PROMPT_ROOT / f"{stem}.md"
        if path.is_file():
            return path
    return None


def literature_roles() -> list[str]:
    """Return available literature role prompt stems."""

    return sorted(
        path.stem
        for path in LITERATURE_PROMPT_ROOT.glob("*.md")
        if path.stem not in {"leader", "worker-base"}
    )


def literature_role_path(name: str) -> Path | None:
    """Resolve a literature role by prompt stem or team key."""

    raw = name.strip()
    candidates = [LITERATURE_ROLE_ALIASES.get(raw), raw, raw.replace("_", "-")]
    for stem in candidates:
        if not stem:
            continue
        path = LITERATURE_PROMPT_ROOT / f"{stem}.md"
        if path.is_file():
            return path
    return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--leader", action="store_true")
    mode.add_argument("--role", choices=roles())
    mode.add_argument("--data-leader", action="store_true")
    mode.add_argument("--data-role", metavar="ROLE", help=f"Data role ({', '.join(data_roles())})")
    mode.add_argument("--model-leader", action="store_true")
    mode.add_argument("--model-role", metavar="ROLE", help=f"Model role ({', '.join(model_roles())})")
    mode.add_argument("--validation-leader", action="store_true")
    mode.add_argument(
        "--validation-role",
        metavar="ROLE",
        help=f"Validation role ({', '.join(validation_roles())})",
    )
    mode.add_argument(
        "--figure-leader",
        "--figure-prep-leader",
        "--figure-preparation-leader",
        dest="figure_leader",
        action="store_true",
    )
    mode.add_argument(
        "--figure-role",
        "--figure-prep-role",
        "--figure-preparation-role",
        dest="figure_role",
        metavar="ROLE",
        help=(
            "Figure-preparation role (accepts a prompt stem or team key; "
            f"available stems: {', '.join(figure_roles())})"
        ),
    )
    mode.add_argument(
        "--paper-prep-leader",
        "--paper-preparation-leader",
        "--paper-leader",
        dest="paper_prep_leader",
        action="store_true",
    )
    mode.add_argument(
        "--paper-prep-role",
        "--paper-preparation-role",
        "--paper-role",
        dest="paper_prep_role",
        metavar="ROLE",
        help=(
            "Paper-preparation role (accepts a prompt stem or team key; "
            f"available stems: {', '.join(paper_roles())})"
        ),
    )
    mode.add_argument(
        "--paper-writing-leader",
        "--formal-paper-leader",
        dest="paper_writing_leader",
        action="store_true",
    )
    mode.add_argument(
        "--paper-writing-role",
        "--formal-paper-role",
        dest="paper_writing_role",
        metavar="ROLE",
        help=(
            "Paper-writing role (accepts a prompt stem or team key; "
            f"available stems: {', '.join(paper_writing_roles())})"
        ),
    )
    mode.add_argument(
        "--final-delivery-leader",
        "--delivery-leader",
        dest="final_delivery_leader",
        action="store_true",
    )
    mode.add_argument(
        "--final-delivery-role",
        "--delivery-role",
        dest="final_delivery_role",
        metavar="ROLE",
        help=(
            "Final-delivery role (accepts a prompt stem or team key; "
            f"available stems: {', '.join(final_delivery_roles())})"
        ),
    )
    mode.add_argument("--literature-leader", action="store_true")
    mode.add_argument(
        "--literature-role",
        dest="literature_role",
        metavar="ROLE",
        help=(
            "Literature role (accepts a prompt stem or team key; "
            f"available stems: {', '.join(literature_roles())})"
        ),
    )
    parser.add_argument("--task-brief", type=Path, help="Markdown brief required for a worker role")
    parser.add_argument("--output", type=Path, help="Optional rendered prompt path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if (
        args.leader
        or args.data_leader
        or args.model_leader
        or args.validation_leader
        or args.figure_leader
        or args.paper_prep_leader
        or args.paper_writing_leader
        or args.final_delivery_leader
        or args.literature_leader
    ):
        if args.task_brief:
            print(
                "error: --task-brief is only valid with a worker role, not a leader mode",
                file=sys.stderr,
            )
            return 2
        if args.data_leader:
            leader_prompt = DATA_PROMPT_ROOT / "leader.md"
        elif args.model_leader:
            leader_prompt = MODEL_PROMPT_ROOT / "leader.md"
        elif args.validation_leader:
            leader_prompt = VALIDATION_PROMPT_ROOT / "leader.md"
        elif args.figure_leader:
            leader_prompt = FIGURE_PROMPT_ROOT / "leader.md"
        elif args.paper_prep_leader:
            leader_prompt = PAPER_PROMPT_ROOT / "leader.md"
        elif args.paper_writing_leader:
            leader_prompt = PAPER_WRITING_PROMPT_ROOT / "leader.md"
        elif args.final_delivery_leader:
            leader_prompt = FINAL_DELIVERY_PROMPT_ROOT / "leader.md"
        elif args.literature_leader:
            leader_prompt = LITERATURE_PROMPT_ROOT / "leader.md"
        else:
            leader_prompt = PROMPT_ROOT / "leader.md"
        if not leader_prompt.is_file():
            print(f"error: leader prompt is missing: {leader_prompt}", file=sys.stderr)
            return 2
        rendered = read_text(leader_prompt)
    else:
        if not args.task_brief or not args.task_brief.is_file():
            print("error: --task-brief must point to an existing Markdown file", file=sys.stderr)
            return 2
        brief = read_text(args.task_brief)
        if not brief:
            print("error: task brief is empty", file=sys.stderr)
            return 2
        if args.data_role:
            role_prompt = data_role_path(args.data_role)
            if role_prompt is None:
                available = ", ".join(data_roles())
                print(f"error: unknown data role {args.data_role!r}; choose from: {available}", file=sys.stderr)
                return 2
            worker_prompt = DATA_PROMPT_ROOT / "worker-base.md"
        elif args.model_role:
            role_prompt = model_role_path(args.model_role)
            if role_prompt is None:
                available = ", ".join(model_roles())
                print(f"error: unknown model role {args.model_role!r}; choose from: {available}", file=sys.stderr)
                return 2
            worker_prompt = MODEL_PROMPT_ROOT / "worker-base.md"
        elif args.validation_role:
            role_prompt = validation_role_path(args.validation_role)
            if role_prompt is None:
                available = ", ".join(validation_roles())
                print(
                    f"error: unknown validation role {args.validation_role!r}; choose from: {available}",
                    file=sys.stderr,
                )
                return 2
            worker_prompt = VALIDATION_PROMPT_ROOT / "worker-base.md"
        elif args.figure_role:
            role_prompt = figure_role_path(args.figure_role)
            if role_prompt is None:
                available = ", ".join(figure_roles()) or "(no figure role prompts found)"
                print(
                    f"error: unknown figure role {args.figure_role!r}; choose a prompt stem or team key from: {available}",
                    file=sys.stderr,
                )
                return 2
            worker_prompt = FIGURE_PROMPT_ROOT / "worker-base.md"
        elif args.paper_prep_role:
            role_prompt = paper_role_path(args.paper_prep_role)
            if role_prompt is None:
                available = ", ".join(paper_roles()) or "(no paper-preparation role prompts found)"
                print(
                    f"error: unknown paper-preparation role {args.paper_prep_role!r}; "
                    f"choose a prompt stem or team key from: {available}",
                    file=sys.stderr,
                )
                return 2
            worker_prompt = PAPER_PROMPT_ROOT / "worker-base.md"
        elif args.paper_writing_role:
            role_prompt = paper_writing_role_path(args.paper_writing_role)
            if role_prompt is None:
                available = ", ".join(paper_writing_roles()) or "(no paper-writing role prompts found)"
                print(
                    f"error: unknown paper-writing role {args.paper_writing_role!r}; "
                    f"choose a prompt stem or team key from: {available}",
                    file=sys.stderr,
                )
                return 2
            worker_prompt = PAPER_WRITING_PROMPT_ROOT / "worker-base.md"
        elif args.final_delivery_role:
            role_prompt = final_delivery_role_path(args.final_delivery_role)
            if role_prompt is None:
                available = ", ".join(final_delivery_roles()) or "(no final-delivery role prompts found)"
                print(
                    f"error: unknown final-delivery role {args.final_delivery_role!r}; "
                    f"choose a prompt stem or team key from: {available}",
                    file=sys.stderr,
                )
                return 2
            worker_prompt = FINAL_DELIVERY_PROMPT_ROOT / "worker-base.md"
        elif args.literature_role:
            role_prompt = literature_role_path(args.literature_role)
            if role_prompt is None:
                available = ", ".join(literature_roles()) or "(no literature role prompts found)"
                print(
                    f"error: unknown literature role {args.literature_role!r}; "
                    f"choose a prompt stem or team key from: {available}",
                    file=sys.stderr,
                )
                return 2
            worker_prompt = LITERATURE_PROMPT_ROOT / "worker-base.md"
        else:
            role_prompt = ROLE_ROOT / f"{args.role}.md"
            worker_prompt = PROMPT_ROOT / "worker-base.md"
        rendered = "\n\n".join(
            [
                read_text(worker_prompt),
                read_text(role_prompt),
                "# 本轮 Task Brief\n\n" + brief,
            ]
        )

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
