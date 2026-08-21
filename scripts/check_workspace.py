#!/usr/bin/env python3
"""Check run directories and metadata only; never judge Markdown semantics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


STAGES = {"init": 0, "baseline": 1, "route": 2, "data": 3, "figure-prep": 4, "paper-prep": 5, "paper-writing": 6, "final-delivery": 7, "literature": 8}
ASYNC_STAGES = {"figure-prep", "paper-prep", "paper-writing", "final-delivery", "literature"}

DATA_DIRS = (
    "data/briefs",
    "data/contracts",
    "data/profiling",
    "data/decisions",
    "data/pipeline/src",
    "data/pipeline/tests",
    "data/staging",
    "data/processed/canonical",
    "data/processed/analytical",
    "data/reviews",
    "data/paper-notes",
)

FIGURE_PREP_DIRS = (
    "figure-prep/scope",
    "figure-prep/questions",
    "figure-prep/cross-question",
    "figure-prep/change-requests",
)

PAPER_PREP_DIRS = (
    "paper-prep/briefs",
    "paper-prep/scope",
    "paper-prep/structure",
    "paper-prep/questions",
    "paper-prep/shared",
    "paper-prep/integration",
    "paper-prep/change-requests",
)

PAPER_WRITING_DIRS = (
    "paper-writing/briefs",
    "paper-writing/scope",
    "paper-writing/plan",
    "paper-writing/sections",
    "paper-writing/manuscript",
    "paper-writing/reviews/closure",
    "paper-writing/responses",
    "paper-writing/change-requests",
)

FINAL_DELIVERY_DIRS = (
    "final-delivery/briefs",
    "final-delivery/scope",
    "final-delivery/source",
    "final-delivery/supporting-materials/results",
    "final-delivery/candidate",
    "final-delivery/reviews",
    "final-delivery/human-review",
)

LITERATURE_DIRS = (
    "literature/scope",
    "literature/route-alignment/search-briefs",
    "literature/route-alignment/route-a",
    "literature/route-alignment/route-b",
    "literature/route-alignment/sources",
    "literature/route-alignment/human-consultation",
    "literature/citation-preparation/search-briefs",
    "literature/citation-preparation/scouts",
    "literature/citation-preparation/sources",
)


def nonempty_file(path: Path) -> bool:
    """Return whether a path is a regular file with at least one byte."""

    return path.is_file() and path.stat().st_size > 0


def has_diagnostic_records(path: Path) -> bool:
    """Detect whether an optional diagnostics directory actually contains data.

    Empty ownership directories are intentionally ignored.  This lets callers
    create a standard directory skeleton without being forced to create a
    semantic diagnostic report.
    """

    if not path.is_dir():
        return False
    return any(child.is_file() and child.stat().st_size > 0 for child in path.rglob("*"))


def check_figure_candidate(candidate: Path, errors: list[str], warnings: list[str]) -> None:
    """Check only the mechanical contents of one open candidate directory."""

    csv_path = candidate / "data.csv"
    parquet_paths = sorted(candidate.glob("*.parquet"))
    data_paths = [path for path in (csv_path, *parquet_paths) if path.exists()]
    usable_data = [path for path in data_paths if nonempty_file(path)]
    if not usable_data:
        errors.append(
            f"figure candidate must contain a non-empty data.csv or *.parquet: "
            f"{candidate.relative_to(candidate.parents[3])}"
        )
    if len(usable_data) > 1:
        warnings.append(
            f"figure candidate contains both data.csv and data.parquet; checker does not choose a canonical copy: "
            f"{candidate.relative_to(candidate.parents[3])}"
        )
    if not nonempty_file(candidate / "provenance.md"):
        errors.append(f"missing or empty figure candidate file: {candidate}/provenance.md")
    if not nonempty_file(candidate / "export.py"):
        errors.append(f"missing or empty figure candidate file: {candidate}/export.py")
    if not nonempty_file(candidate / "recommendation.md"):
        errors.append(f"missing or empty figure candidate file: {candidate}/recommendation.md")


def iter_figure_candidate_dirs(run_dir: Path) -> list[Path]:
    """Find candidate ownership roots for questions and shared results."""

    roots = [run_dir / "figure-prep/questions", run_dir / "figure-prep/cross-question"]
    candidates: list[Path] = []
    for root in roots:
        if not root.is_dir():
            continue
        for candidates_root in root.rglob("candidates"):
            if not candidates_root.is_dir():
                continue
            candidates.extend(path for path in candidates_root.iterdir() if path.is_dir())
    return sorted(candidates)


def iter_figure_diagnostics_dirs(run_dir: Path) -> list[Path]:
    """Find optional diagnostic roots without requiring a question layout."""

    roots = [run_dir / "figure-prep/questions", run_dir / "figure-prep/cross-question"]
    diagnostics: list[Path] = []
    for root in roots:
        if root.is_dir():
            diagnostics.extend(path for path in root.rglob("diagnostics") if path.is_dir())
    return sorted(diagnostics)


def check_figure_preparation(run_dir: Path, errors: list[str], warnings: list[str]) -> None:
    """Check V6 inputs and figure-prep handoff mechanics, never its semantics."""

    for relative in FIGURE_PREP_DIRS:
        if not (run_dir / relative).is_dir():
            errors.append(f"missing figure-prep directory: {relative}")

    # V6 evidence and the CP1 chapter map are required entry artifacts for F3.
    # Their contents are deliberately opaque to this checker.
    for relative in (
        "validation/validation-handoff.md",
        "validation/claims/claim-evidence-map.md",
        "paper-prep/structure/chapter-map-v0.md",
    ):
        path = run_dir / relative
        if not nonempty_file(path):
            errors.append(f"missing or empty figure-prep entry file: {relative}")

    frozen_inputs = run_dir / "figure-prep/scope/frozen-inputs.md"
    if not nonempty_file(frozen_inputs):
        errors.append("missing or empty figure-prep scope file: figure-prep/scope/frozen-inputs.md")

    for relative in (
        "figure-prep/figure-plan.md",
        "figure-prep/figure-preparation-handoff.md",
    ):
        path = run_dir / relative
        if not nonempty_file(path):
            errors.append(f"missing or empty figure-prep handoff file: {relative}")

    for candidate in iter_figure_candidate_dirs(run_dir):
        check_figure_candidate(candidate, errors, warnings)

    for diagnostics in iter_figure_diagnostics_dirs(run_dir):
        if has_diagnostic_records(diagnostics):
            index = diagnostics / "diagnostic-index.md"
            if not nonempty_file(index):
                errors.append(
                    f"diagnostics contain records but diagnostic-index.md is missing or empty: "
                    f"{diagnostics}"
                )


def check_paper_preparation(run_dir: Path, errors: list[str], warnings: list[str]) -> None:
    """Check CP0–CP6 files and paths without judging manuscript quality."""

    for relative in PAPER_PREP_DIRS:
        if not (run_dir / relative).is_dir():
            errors.append(f"missing paper-prep directory: {relative}")

    for relative in (
        "validation/validation-handoff.md",
        "validation/claims/claim-evidence-map.md",
        "figure-prep/figure-preparation-handoff.md",
        "literature/citation-preparation/references-handoff.md",
        "literature/citation-preparation/claim-to-citation-map.md",
        "literature/references.bib",
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
    ):
        if not nonempty_file(run_dir / relative):
            errors.append(f"missing or empty paper-prep file: {relative}")

    questions_root = run_dir / "paper-prep/questions"
    question_roots = sorted(path for path in questions_root.iterdir() if path.is_dir()) if questions_root.is_dir() else []
    if not question_roots:
        errors.append("paper-prep must contain at least one question ownership directory")
    for question_root in question_roots:
        for name in ("chapter-material-v1.md", "evidence-review.md", "evidence-response.md"):
            if not nonempty_file(question_root / name):
                errors.append(f"missing or empty paper-prep question file: {question_root / name}")
        if not nonempty_file(question_root / "chapter-material-v2.md"):
            errors.append(
                f"paper-prep question requires a non-empty chapter-material-v2.md: {question_root}"
            )

    blind = run_dir / "paper-prep/integration/competition-review-blind.md"
    pattern = run_dir / "paper-prep/integration/competition-review-pattern-sweep.md"
    if nonempty_file(blind) and nonempty_file(pattern) and pattern.stat().st_mtime < blind.stat().st_mtime:
        warnings.append(
            "competition-review-pattern-sweep.md predates the blind review; checker cannot confirm context isolation"
        )


def check_paper_writing(run_dir: Path, errors: list[str], warnings: list[str]) -> None:
    """Check PW0–PW7 paths and versions without judging prose or facts."""

    for relative in PAPER_WRITING_DIRS:
        if not (run_dir / relative).is_dir():
            errors.append(f"missing paper-writing directory: {relative}")

    required_files = (
        "validation/claims/claim-evidence-map.md",
        "figure-prep/figure-preparation-handoff.md",
        "paper-prep/paper-framework-handoff.md",
        "literature/citation-preparation/references-handoff.md",
        "literature/citation-preparation/claim-to-citation-map.md",
        "literature/references.bib",
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
    )
    for relative in required_files:
        if not nonempty_file(run_dir / relative):
            errors.append(f"missing or empty paper-writing file: {relative}")

    sections_root = run_dir / "paper-writing/sections"
    section_roots = sorted(path for path in sections_root.iterdir() if path.is_dir()) if sections_root.is_dir() else []
    if not section_roots:
        errors.append("paper-writing must contain at least one question section directory")
    for section_root in section_roots:
        for name in ("section-v1.md", "section-fact-response.md", "section-v2.md"):
            if not nonempty_file(section_root / name):
                errors.append(f"missing or empty paper-writing section file: {section_root / name}")

    manuscript = run_dir / "paper-writing/manuscript"
    versions = [manuscript / name for name in ("full-paper-v1.md", "full-paper-v2.md", "full-paper-v3.md", "final-paper.md")]
    existing_versions = [path for path in versions if nonempty_file(path)]
    for earlier, later in zip(existing_versions, existing_versions[1:]):
        if later.stat().st_mtime < earlier.stat().st_mtime:
            warnings.append(
                f"paper-writing version timestamp is out of order: {later.name} predates {earlier.name}"
            )


def check_final_delivery(run_dir: Path, errors: list[str], warnings: list[str]) -> None:
    """Check FD0–FD7 artifact mechanics without judging layout or prose."""

    for relative in FINAL_DELIVERY_DIRS:
        if not (run_dir / relative).is_dir():
            errors.append(f"missing final-delivery directory: {relative}")

    required_files = (
        "synthesis/problem-baseline.md",
        "routes/route-handoff.md",
        "data/data-handoff.md",
        "modeling/model-handoff.md",
        "validation/validation-handoff.md",
        "validation/claims/claim-evidence-map.md",
        "literature/route-alignment/route-evidence-handoff.md",
        "literature/citation-preparation/references-handoff.md",
        "literature/citation-preparation/claim-to-citation-map.md",
        "literature/references.bib",
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
        "final-delivery/candidate/paper.pdf",
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
        if not nonempty_file(run_dir / relative):
            errors.append(f"missing or empty final-delivery file: {relative}")

    results_root = run_dir / "final-delivery/supporting-materials/results"
    result_files = (
        [path for path in results_root.rglob("*") if nonempty_file(path)]
        if results_root.is_dir()
        else []
    )
    if not result_files:
        errors.append("final-delivery supporting materials must contain at least one non-empty result data file")

    candidate_root = run_dir / "final-delivery/candidate"
    editable_candidates = [
        path
        for pattern in ("*.docx", "*.tex")
        for path in candidate_root.glob(pattern)
        if nonempty_file(path)
    ] if candidate_root.is_dir() else []
    if not editable_candidates:
        warnings.append(
            "no non-empty DOCX or TeX candidate found; checker cannot determine whether the official submission requires one"
        )

    snapshot = run_dir / "final-delivery/scope/candidate-snapshot.md"
    review_paths = [
        run_dir / relative
        for relative in required_files
        if relative.startswith("final-delivery/reviews/")
    ]
    if nonempty_file(snapshot):
        for review in review_paths:
            if nonempty_file(review) and review.stat().st_mtime < snapshot.stat().st_mtime:
                warnings.append(
                    f"terminal review predates candidate snapshot: {review.relative_to(run_dir)}"
                )

    forbidden_post_review_roots = (
        run_dir / "final-delivery/responses",
        run_dir / "final-delivery/reviews/closure",
    )
    for forbidden_root in forbidden_post_review_roots:
        if forbidden_root.is_dir() and any(
            path.is_file() and path.stat().st_size > 0 for path in forbidden_root.rglob("*")
        ):
            errors.append(
                f"final-delivery terminal review must not create response or closure artifacts: "
                f"{forbidden_root.relative_to(run_dir)}"
            )


def check_literature(run_dir: Path, errors: list[str], warnings: list[str]) -> None:
    """Check literature artifacts and paths without judging source truth."""

    for relative in LITERATURE_DIRS:
        if not (run_dir / relative).is_dir():
            errors.append(f"missing literature directory: {relative}")

    required_files = (
        "literature/route-alignment/search-briefs/route-a.md",
        "literature/route-alignment/search-briefs/route-b.md",
        "literature/route-alignment/route-a/scout-memo.md",
        "literature/route-alignment/route-b/scout-memo.md",
        "literature/route-alignment/human-consultation/consultation-brief.md",
        "literature/route-alignment/human-consultation/response-record.md",
        "literature/route-alignment/evidence-review.md",
        "literature/route-alignment/route-evidence-handoff.md",
        "literature/citation-preparation/citation-gap-map.md",
        "literature/citation-preparation/references-candidate.bib",
        "literature/citation-preparation/claim-to-citation-map.md",
        "literature/citation-preparation/citation-audit.md",
        "literature/citation-preparation/references-handoff.md",
        "literature/references.bib",
    )
    for relative in required_files:
        if not nonempty_file(run_dir / relative):
            errors.append(f"missing or empty literature file: {relative}")

    route_sources = list((run_dir / "literature/route-alignment/sources").glob("*/source-note.md"))
    citation_sources = list((run_dir / "literature/citation-preparation/sources").glob("*/source-note.md"))
    citation_scouts = list((run_dir / "literature/citation-preparation/scouts").glob("*/scout-memo.md"))
    if not any(nonempty_file(path) for path in route_sources):
        errors.append("literature route alignment requires at least one non-empty source-note.md")
    if not any(nonempty_file(path) for path in citation_sources):
        errors.append("literature citation preparation requires at least one non-empty source-note.md")
    if not any(nonempty_file(path) for path in citation_scouts):
        errors.append("literature citation preparation requires at least one topic scout-memo.md")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--stage", choices=STAGES, default="init")
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    run_dir = args.run_dir.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    required_dirs = [
        "inputs", "state", "briefs", "submissions/W1", "submissions/W2",
        "submissions/W3R", "reviews/W3", "reviews/W4", "synthesis",
        "routes/responses",
    ]
    for relative in required_dirs:
        if not (run_dir / relative).is_dir():
            errors.append(f"missing directory: {relative}")

    metadata: dict[str, object] = {}
    for relative in ("inputs/source-manifest.json", "state/run-state.json"):
        path = run_dir / relative
        if not path.is_file():
            errors.append(f"missing metadata file: {relative}")
            continue
        try:
            metadata[relative] = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid runtime metadata JSON in {relative}: {exc}")

    manifest = metadata.get("inputs/source-manifest.json")
    state = metadata.get("state/run-state.json")
    if isinstance(manifest, dict) and manifest.get("metadata_only") is not True:
        warnings.append("source-manifest.json should declare metadata_only=true")
    if isinstance(state, dict) and state.get("metadata_only") is not True:
        warnings.append("run-state.json should declare metadata_only=true")
    if isinstance(manifest, dict) and isinstance(state, dict):
        if manifest.get("source_snapshot_id") != state.get("source_snapshot_id"):
            errors.append("source snapshot differs between manifest and run state")
        if not manifest.get("materials"):
            warnings.append("no source files are registered")

    # ``figure-prep`` is a post-V6 asynchronous branch, not a cumulative
    # legacy stage.  Its entry contract is checked above; it must not pretend
    # to re-run baseline/route/data checks (and those checks do not implement
    # modeling or validation semantics).
    if args.stage not in ASYNC_STAGES and STAGES[args.stage] >= STAGES["baseline"]:
        baseline = run_dir / "synthesis/problem-baseline.md"
        if not baseline.is_file() or baseline.stat().st_size == 0:
            errors.append("missing or empty report file: synthesis/problem-baseline.md")
        submissions = list((run_dir / "submissions").glob("W*/*.md")) if (run_dir / "submissions").is_dir() else []
        if not submissions:
            warnings.append("no raw worker Markdown submissions found; checker does not infer whether this is intentional")

    if args.stage not in ASYNC_STAGES and STAGES[args.stage] >= STAGES["route"]:
        for relative in (
            "routes/route-a.md",
            "routes/route-b.md",
            "routes/route-review.md",
            "literature/route-alignment/route-a/scout-memo.md",
            "literature/route-alignment/route-b/scout-memo.md",
            "literature/route-alignment/human-consultation/consultation-brief.md",
            "literature/route-alignment/human-consultation/response-record.md",
            "literature/route-alignment/evidence-review.md",
            "literature/route-alignment/route-evidence-handoff.md",
            "routes/route-handoff.md",
        ):
            path = run_dir / relative
            if not path.is_file() or path.stat().st_size == 0:
                errors.append(f"missing or empty report file: {relative}")
        route_source_notes = list(
            (run_dir / "literature/route-alignment/sources").glob("*/source-note.md")
        )
        if not any(nonempty_file(path) for path in route_source_notes):
            errors.append("route handoff requires at least one non-empty literature source-note.md")

    if args.stage not in ASYNC_STAGES and STAGES[args.stage] >= STAGES["data"]:
        for relative in DATA_DIRS:
            if not (run_dir / relative).is_dir():
                errors.append(f"missing data directory: {relative}")
        handoff = run_dir / "data/data-handoff.md"
        if not handoff.is_file() or handoff.stat().st_size == 0:
            errors.append("missing or empty handoff file: data/data-handoff.md")

    if args.stage == "figure-prep":
        check_figure_preparation(run_dir, errors, warnings)
    if args.stage == "paper-prep":
        check_paper_preparation(run_dir, errors, warnings)
    if args.stage == "paper-writing":
        check_paper_writing(run_dir, errors, warnings)
    if args.stage == "final-delivery":
        check_final_delivery(run_dir, errors, warnings)
    if args.stage == "literature":
        check_literature(run_dir, errors, warnings)

    payload = {
        "stage": args.stage,
        "run_dir": str(run_dir),
        "markdown_content_parsed": False,
        "semantic_correctness_checked": False,
        "figure_aesthetic_checked": False,
        "competition_manuscript_quality_checked": False,
        "award_distillation_context_isolation_checked": False,
        "ai_prose_quality_checked": False,
        "reviewer_independence_checked": False,
        "layout_quality_checked": False,
        "answer_relevance_checked": False,
        "delivery_evidence_semantics_checked": False,
        "end_to_end_consistency_semantics_checked": False,
        "post_review_human_edits_checked": False,
        "literature_semantics_checked": False,
        "human_opinion_authenticity_checked": False,
        "citation_support_checked": False,
        "errors": errors,
        "warnings": warnings,
    }
    if args.as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for error in errors:
            print(f"ERROR: {error}")
        for warning in warnings:
            print(f"WARN: {warning}")
        print(f"summary: {len(errors)} error(s), {len(warnings)} warning(s)")
        print("note: Markdown content and semantic correctness were not checked")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
