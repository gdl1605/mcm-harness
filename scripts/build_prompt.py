#!/usr/bin/env python3
"""Inject embedded mcm semantics, then combine worker, role, and task-brief prompts."""

from __future__ import annotations

import argparse
import json
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
FORMAL_FIGURE_PROMPT_ROOT = PROMPT_ROOT / "formal-figures"
MCM_INTEGRATION_PATH = PROJECT_ROOT / "Workflow" / "mcm-skill-integration.json"
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
FORMAL_FIGURE_ROLE_ALIASES = {
    "question_visual_producer": "question-visual-producer",
    "shared_visual_producer": "question-visual-producer",
    "figure_portfolio_reviewer": "figure-portfolio-reviewer",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def load_mcm_integration() -> dict[str, object]:
    """Load and mechanically validate the embedded mcm skill routing config."""

    if not MCM_INTEGRATION_PATH.is_file():
        raise ValueError(f"missing mcm skill integration config: {MCM_INTEGRATION_PATH}")
    try:
        config = json.loads(MCM_INTEGRATION_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid mcm skill integration config: {exc}") from exc
    if not isinstance(config, dict):
        raise ValueError("mcm skill integration config must be a JSON object")
    skill = config.get("skill")
    profiles = config.get("profiles")
    bindings = config.get("bindings")
    if not isinstance(skill, dict) or not isinstance(profiles, dict) or not isinstance(bindings, dict):
        raise ValueError("mcm skill integration config requires skill, profiles, and bindings objects")
    entrypoint = skill.get("entrypoint")
    if not isinstance(entrypoint, str) or not (PROJECT_ROOT / entrypoint).is_file():
        raise ValueError(f"embedded mcm skill entrypoint is missing: {entrypoint!r}")
    skill_root = (PROJECT_ROOT / entrypoint).parent
    for profile_name, profile in profiles.items():
        if not isinstance(profile, dict):
            raise ValueError(f"mcm profile must be an object: {profile_name}")
        references = profile.get("references", [])
        if not isinstance(references, list) or not all(isinstance(path, str) for path in references):
            raise ValueError(f"mcm profile references must be a string list: {profile_name}")
        for relative in references:
            if not (skill_root / relative).is_file():
                raise ValueError(
                    f"mcm profile {profile_name} references missing file: {skill_root / relative}"
                )
    for binding_name, binding in bindings.items():
        if not isinstance(binding, dict):
            raise ValueError(f"mcm binding must be an object: {binding_name}")
        referenced_profiles = [binding.get("profile"), binding.get("default")]
        overrides = binding.get("overrides", {})
        if not isinstance(overrides, dict):
            raise ValueError(f"mcm binding overrides must be an object: {binding_name}")
        referenced_profiles.extend(overrides.values())
        for profile_name in referenced_profiles:
            if profile_name is not None and profile_name not in profiles:
                raise ValueError(
                    f"mcm binding {binding_name} references unknown profile: {profile_name!r}"
                )
    return config


def resolve_mcm_profile(
    config: dict[str, object],
    binding_key: str,
    role_stem: str | None,
    override: str,
) -> str | None:
    """Resolve a semantic profile without inferring paper quality mechanically."""

    profiles = config["profiles"]
    assert isinstance(profiles, dict)
    if override == "none":
        return None
    if override != "auto":
        if override not in profiles:
            available = ", ".join(sorted(str(name) for name in profiles))
            raise ValueError(f"unknown mcm profile {override!r}; choose from: {available}")
        return override

    bindings = config["bindings"]
    assert isinstance(bindings, dict)
    binding = bindings.get(binding_key)
    if not isinstance(binding, dict):
        raise ValueError(f"missing mcm binding for prompt mode: {binding_key}")
    if role_stem is None:
        profile = binding.get("profile")
    else:
        overrides = binding.get("overrides", {})
        if not isinstance(overrides, dict):
            raise ValueError(f"mcm binding overrides must be an object: {binding_key}")
        profile = overrides.get(role_stem, binding.get("default"))
    if profile is not None and profile not in profiles:
        raise ValueError(f"mcm binding {binding_key} references unknown profile: {profile!r}")
    return profile if isinstance(profile, str) else None


def render_mcm_context(config: dict[str, object], profile_name: str | None) -> str:
    """Render the exact skill files a role may load; never inline semantic verdicts."""

    if profile_name is None:
        return ""
    profiles = config["profiles"]
    skill = config["skill"]
    assert isinstance(profiles, dict) and isinstance(skill, dict)
    profile = profiles[profile_name]
    if not isinstance(profile, dict):
        raise ValueError(f"mcm profile must be an object: {profile_name}")
    activation = profile.get("activation", "required")
    purpose = profile.get("purpose", "")
    if activation == "forbidden_until_explicit_override":
        return "\n".join(
            [
                "# 内置 mcm Skill 隔离协议",
                "",
                f"本轮配置为 `{profile_name}`：{purpose}",
                "盲审文件落盘前禁止调用 `$mcm`、读取 `.agents/skills/mcm/SKILL.md` 或任何国奖/评委向参考资料。",
                "需要开始第二遍模式扫描时，由 Leader 重新使用 `--mcm-profile judge-review` 构建后续 prompt；不得由本 Agent自行提前切换。",
            ]
        )
    if activation != "required":
        raise ValueError(f"unsupported mcm profile activation: {activation!r}")

    entrypoint = skill.get("entrypoint")
    invocation = skill.get("invocation")
    if not isinstance(entrypoint, str) or not isinstance(invocation, str):
        raise ValueError("mcm skill config requires string entrypoint and invocation")
    skill_root = (PROJECT_ROOT / entrypoint).parent
    references = profile.get("references", [])
    if not isinstance(references, list) or not all(isinstance(path, str) for path in references):
        raise ValueError(f"mcm profile references must be a string list: {profile_name}")
    rendered_refs: list[str] = []
    for relative in references:
        path = skill_root / relative
        if not path.is_file():
            raise ValueError(f"mcm profile {profile_name} references missing file: {path}")
        rendered_refs.append(f"- `{path.relative_to(PROJECT_ROOT)}`")

    lines = [
        "# 内置 mcm Skill 运行协议",
        "",
        f"本轮必须显式使用仓库内置 `{invocation}`；开始推理前完整读取 `{entrypoint}`。",
        f"本轮语义模式：`{profile.get('mode', profile_name)}`。目的：{purpose}",
        "随后只按当前任务需要加载以下已授权参考：",
        "",
        *rendered_refs,
        "",
        "这些资源是语义透镜，不是填空模板或机械评分表。Task brief 和模块 prompt 仍决定读取白名单、文件所有权、停止边界与禁止动作；skill 不得扩大权限。",
        "不得自行读取未列出的 `references/distill/source-notes/`、旧范文或其他 profile 资料；不得用模型名、字段命中或范文相似度替代本题证据判断。",
    ]
    return "\n".join(lines)


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


def formal_figure_roles() -> list[str]:
    """Return available formal-figure role prompt stems."""

    return sorted(
        path.stem
        for path in FORMAL_FIGURE_PROMPT_ROOT.glob("*.md")
        if path.stem not in {"leader", "worker-base"}
    )


def formal_figure_role_path(name: str) -> Path | None:
    """Resolve a formal-figure role by prompt stem or team key."""

    raw = name.strip()
    candidates = [FORMAL_FIGURE_ROLE_ALIASES.get(raw), raw, raw.replace("_", "-")]
    for stem in candidates:
        if not stem:
            continue
        path = FORMAL_FIGURE_PROMPT_ROOT / f"{stem}.md"
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
    mode.add_argument(
        "--formal-figure-leader",
        "--figure-rendering-leader",
        dest="formal_figure_leader",
        action="store_true",
    )
    mode.add_argument(
        "--formal-figure-role",
        "--figure-rendering-role",
        dest="formal_figure_role",
        metavar="ROLE",
        help=(
            "Formal-figure role (accepts a prompt stem or team key; "
            f"available stems: {', '.join(formal_figure_roles())})"
        ),
    )
    parser.add_argument("--task-brief", type=Path, help="Markdown brief required for a worker role")
    parser.add_argument("--output", type=Path, help="Optional rendered prompt path")
    parser.add_argument(
        "--mcm-profile",
        default="auto",
        metavar="PROFILE",
        help="Embedded mcm semantic profile override; use auto (default), none, or a configured profile",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    binding_key: str
    role_stem: str | None = None
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
        or args.formal_figure_leader
    ):
        if args.task_brief:
            print(
                "error: --task-brief is only valid with a worker role, not a leader mode",
                file=sys.stderr,
            )
            return 2
        if args.data_leader:
            leader_prompt = DATA_PROMPT_ROOT / "leader.md"
            binding_key = "data_leader"
        elif args.model_leader:
            leader_prompt = MODEL_PROMPT_ROOT / "leader.md"
            binding_key = "model_leader"
        elif args.validation_leader:
            leader_prompt = VALIDATION_PROMPT_ROOT / "leader.md"
            binding_key = "validation_leader"
        elif args.figure_leader:
            leader_prompt = FIGURE_PROMPT_ROOT / "leader.md"
            binding_key = "figure_leader"
        elif args.paper_prep_leader:
            leader_prompt = PAPER_PROMPT_ROOT / "leader.md"
            binding_key = "paper_prep_leader"
        elif args.paper_writing_leader:
            leader_prompt = PAPER_WRITING_PROMPT_ROOT / "leader.md"
            binding_key = "paper_writing_leader"
        elif args.final_delivery_leader:
            leader_prompt = FINAL_DELIVERY_PROMPT_ROOT / "leader.md"
            binding_key = "final_delivery_leader"
        elif args.literature_leader:
            leader_prompt = LITERATURE_PROMPT_ROOT / "leader.md"
            binding_key = "literature_leader"
        elif args.formal_figure_leader:
            leader_prompt = FORMAL_FIGURE_PROMPT_ROOT / "leader.md"
            binding_key = "formal_figure_leader"
        else:
            leader_prompt = PROMPT_ROOT / "leader.md"
            binding_key = "leader"
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
            binding_key = "data_role"
        elif args.model_role:
            role_prompt = model_role_path(args.model_role)
            if role_prompt is None:
                available = ", ".join(model_roles())
                print(f"error: unknown model role {args.model_role!r}; choose from: {available}", file=sys.stderr)
                return 2
            worker_prompt = MODEL_PROMPT_ROOT / "worker-base.md"
            binding_key = "model_role"
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
            binding_key = "validation_role"
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
            binding_key = "figure_role"
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
            binding_key = "paper_prep_role"
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
            binding_key = "paper_writing_role"
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
            binding_key = "final_delivery_role"
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
            binding_key = "literature_role"
        elif args.formal_figure_role:
            role_prompt = formal_figure_role_path(args.formal_figure_role)
            if role_prompt is None:
                available = ", ".join(formal_figure_roles()) or "(no formal-figure role prompts found)"
                print(
                    f"error: unknown formal-figure role {args.formal_figure_role!r}; "
                    f"choose a prompt stem or team key from: {available}",
                    file=sys.stderr,
                )
                return 2
            worker_prompt = FORMAL_FIGURE_PROMPT_ROOT / "worker-base.md"
            binding_key = "formal_figure_role"
        else:
            role_prompt = ROLE_ROOT / f"{args.role}.md"
            worker_prompt = PROMPT_ROOT / "worker-base.md"
            binding_key = "role"
        role_stem = role_prompt.stem
        rendered = "\n\n".join(
            [
                read_text(worker_prompt),
                read_text(role_prompt),
                "# 本轮 Task Brief\n\n" + brief,
            ]
        )

    try:
        mcm_config = load_mcm_integration()
        mcm_profile = resolve_mcm_profile(
            mcm_config,
            binding_key=binding_key,
            role_stem=role_stem,
            override=args.mcm_profile,
        )
        mcm_context = render_mcm_context(mcm_config, mcm_profile)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if mcm_context:
        rendered = "\n\n".join([mcm_context, rendered])

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
