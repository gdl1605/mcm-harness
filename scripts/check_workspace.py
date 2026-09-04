#!/usr/bin/env python3
"""Check run directories and metadata only; never judge Markdown semantics."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
from zipfile import BadZipFile, ZipFile


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MCM_INTEGRATION_PATH = PROJECT_ROOT / "Workflow" / "mcm-skill-integration.json"

STAGES = {"init": 0, "baseline": 1, "model-briefing": 2, "route": 2, "data": 3, "figure-prep": 4, "paper-prep": 5, "paper-writing": 6, "formal-figures": 7, "final-delivery": 8, "literature": 9}
ASYNC_STAGES = {"figure-prep", "paper-prep", "paper-writing", "formal-figures", "final-delivery", "literature"}

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
    "final-delivery/supporting-materials/processed-data",
    "final-delivery/supporting-materials/results",
    "final-delivery/supporting-materials/source-code",
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

FORMAL_FIGURE_DIRS = (
    "formal-figures/briefs",
    "formal-figures/scope",
    "formal-figures/style",
    "formal-figures/questions",
    "formal-figures/shared",
    "formal-figures/previews",
    "formal-figures/change-requests",
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


def check_mcm_skill_snapshot(
    snapshot: object,
    errors: list[str],
    warnings: list[str],
) -> bool:
    """Check embedded-skill paths and hashes only; never judge semantic behavior."""

    if not isinstance(snapshot, dict):
        errors.append("missing or invalid state/mcm-skill-snapshot.json")
        return False
    expected = {
        "metadata_only": True,
        "skill_name": "mcm",
        "skill_invocation": "$mcm",
        "skill_entrypoint": ".agents/skills/mcm/SKILL.md",
        "integration_config": "Workflow/mcm-skill-integration.json",
        "semantic_quality_checked": False,
    }
    for field, value in expected.items():
        if snapshot.get(field) != value:
            errors.append(f"mcm skill snapshot must set {field}={value!r}")

    drift_detected = False
    expected_config_hash = snapshot.get("integration_config_sha256")
    if not MCM_INTEGRATION_PATH.is_file():
        errors.append("missing embedded mcm integration config")
    elif isinstance(expected_config_hash, str):
        actual = hashlib.sha256(MCM_INTEGRATION_PATH.read_bytes()).hexdigest()
        if actual != expected_config_hash:
            warnings.append("embedded mcm integration config changed after run initialization")
            drift_detected = True
    else:
        errors.append("mcm skill snapshot is missing integration_config_sha256")

    file_hashes = snapshot.get("file_sha256")
    if not isinstance(file_hashes, dict) or not file_hashes:
        errors.append("mcm skill snapshot must contain non-empty file_sha256 metadata")
        return drift_detected
    for relative, expected_hash in file_hashes.items():
        if not isinstance(relative, str) or not isinstance(expected_hash, str):
            errors.append("mcm skill snapshot file_sha256 entries must be string pairs")
            continue
        path = PROJECT_ROOT / relative
        if not path.is_file():
            errors.append(f"embedded mcm skill file is missing: {relative}")
            continue
        actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual_hash != expected_hash:
            warnings.append(f"embedded mcm skill file changed after run initialization: {relative}")
            drift_detected = True
    return drift_detected


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
        "routes/model-candidate-briefing.md",
        "routes/human-model-decision.md",
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
        "formal-figures/figure-rendering-handoff.md",
        "formal-figures/figure-manifest.md",
        "paper-prep/paper-framework-handoff.md",
        "final-delivery/scope/frozen-inputs.md",
        "final-delivery/scope/candidate-snapshot.md",
        "final-delivery/source/submission-source.md",
        "final-delivery/source/supporting-materials.md",
        "final-delivery/supporting-materials/README.md",
        "final-delivery/supporting-materials/processed-data-manifest.md",
        "final-delivery/supporting-materials/result-data-manifest.md",
        "final-delivery/supporting-materials/source-code-manifest.md",
        "final-delivery/supporting-materials/execution-order.md",
        "final-delivery/supporting-materials/source-code.md",
        "final-delivery/supporting-materials/supporting-materials.md",
        "final-delivery/candidate/paper.pdf",
        "final-delivery/candidate/supporting-materials.zip",
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

    preflight = run_dir / "final-delivery/preflight-report.md"
    if nonempty_file(preflight):
        preflight_text = preflight.read_text(encoding="utf-8")
        for marker in ("actual_embedded_width_mm", "aspect_ratio", "in-paper-preview", "FR3"):
            if marker not in preflight_text:
                errors.append(
                    f"final-delivery preflight report is missing figure-layout marker: {marker!r}"
                )

    required_material_roots = {
        "processed data": run_dir / "final-delivery/supporting-materials/processed-data",
        "result data": run_dir / "final-delivery/supporting-materials/results",
        "original source code": run_dir / "final-delivery/supporting-materials/source-code",
    }
    for label, material_root in required_material_roots.items():
        material_files = (
            [path for path in material_root.rglob("*") if nonempty_file(path)]
            if material_root.is_dir()
            else []
        )
        if not material_files:
            errors.append(
                f"final-delivery supporting materials must contain at least one non-empty {label} file"
            )

    archive_path = run_dir / "final-delivery/candidate/supporting-materials.zip"
    if nonempty_file(archive_path):
        try:
            with ZipFile(archive_path) as archive:
                corrupt_member = archive.testzip()
                if corrupt_member is not None:
                    errors.append(
                        f"final-delivery supporting-materials.zip has a corrupt member: {corrupt_member}"
                    )
                members = [
                    info
                    for info in archive.infolist()
                    if not info.is_dir() and info.file_size > 0
                ]
                member_names = {info.filename for info in members}
                for info in members:
                    member_path = PurePosixPath(info.filename)
                    if member_path.is_absolute() or ".." in member_path.parts:
                        errors.append(
                            f"final-delivery supporting-materials.zip has unsafe member path: {info.filename}"
                        )
                for required_member in (
                    "README.md",
                    "processed-data-manifest.md",
                    "result-data-manifest.md",
                    "source-code-manifest.md",
                    "execution-order.md",
                ):
                    if required_member not in member_names:
                        errors.append(
                            f"final-delivery supporting-materials.zip is missing root file: {required_member}"
                        )
                for prefix in ("processed-data/", "results/", "source-code/"):
                    if not any(name.startswith(prefix) for name in member_names):
                        errors.append(
                            f"final-delivery supporting-materials.zip has no non-empty file under {prefix}"
                        )
        except (BadZipFile, OSError) as exc:
            errors.append(f"invalid final-delivery supporting-materials.zip: {exc}")

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


def check_formal_figure_bundle(bundle: Path, errors: list[str]) -> None:
    """Check one question/shared formal-figure bundle mechanically."""

    if not nonempty_file(bundle / "visual-plan.md"):
        errors.append(f"missing or empty formal-figure visual plan: {bundle}/visual-plan.md")
    figure_roots = sorted(
        path for path in bundle.iterdir() if path.is_dir() and path.name.startswith("FIG-")
    ) if bundle.is_dir() else []
    if not figure_roots:
        errors.append(f"formal-figure unit must contain at least one FIG-* directory: {bundle}")
        return
    for figure_root in figure_roots:
        for relative in (
            "data-ref.md",
            "chart-contract.md",
            "render.py",
            "render-config.md",
            "render-memo.md",
            "iteration-log.md",
            "response.md",
            "v1/figure.png",
            "v1/figure.pdf",
            "v1/figure.svg",
            "v2/figure.png",
            "v2/figure.pdf",
            "v2/figure.svg",
            "final/figure.png",
            "final/figure.pdf",
            "final/figure.svg",
        ):
            if not nonempty_file(figure_root / relative):
                errors.append(f"missing or empty formal-figure file: {figure_root / relative}")


def check_project_skill_lock(
    *,
    lock_file: str,
    skill_name: str,
    invocation: str,
    project_skill_path: str,
    errors: list[str],
) -> None:
    """Validate one project skill lock and its local copy when present."""

    lock_path = PROJECT_ROOT / lock_file
    lock: object | None = None
    if not nonempty_file(lock_path):
        errors.append(f"missing {skill_name} skill lock: {lock_file}")
    else:
        try:
            lock = json.loads(lock_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid {skill_name} skill lock JSON: {exc}")
    if isinstance(lock, dict):
        expected_lock = {
            "metadata_only": True,
            "skill": skill_name,
            "required_invocation": invocation,
            "required_backend": "python",
        }
        for field, value in expected_lock.items():
            if lock.get(field) != value:
                errors.append(f"{skill_name} skill lock must set {field}={value!r}")
        skill_path = PROJECT_ROOT / project_skill_path
        expected_hash = lock.get("skill_md_sha256")
        if skill_path.is_file() and isinstance(expected_hash, str):
            actual_hash = hashlib.sha256(skill_path.read_bytes()).hexdigest()
            if actual_hash != expected_hash:
                errors.append(
                    f"project-local {skill_name} SKILL.md does not match the lock hash"
                )


def check_formal_figures(run_dir: Path, errors: list[str], warnings: list[str]) -> None:
    """Check FR0–FR4 files and explicit model/skill/profile metadata only."""

    check_project_skill_lock(
        lock_file="Workflow/nature-figure-skill.lock.json",
        skill_name="nature-figure",
        invocation="$nature-figure",
        project_skill_path=".agents/skills/nature-figure/SKILL.md",
        errors=errors,
    )
    check_project_skill_lock(
        lock_file="Workflow/ssci-plots-skill.lock.json",
        skill_name="ssci-plots",
        invocation="$ssci-plots",
        project_skill_path=".agents/skills/ssci-plots/SKILL.md",
        errors=errors,
    )

    profile_path = PROJECT_ROOT / "Workflow/formal-figure-style-profile.cassatt2.json"
    profile: object | None = None
    if not nonempty_file(profile_path):
        errors.append(
            "missing formal-figure visual profile: "
            "Workflow/formal-figure-style-profile.cassatt2.json"
        )
    else:
        try:
            profile = json.loads(profile_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid formal-figure visual profile JSON: {exc}")
    if isinstance(profile, dict):
        expected_profile = {
            "metadata_only": True,
            "profile_id": "cassatt2_quiet_journal_v1",
            "selected_direction": "C",
            "design_skill": "$visualize-data",
            "style_skill": "$ssci-plots",
            "render_and_qa_skill": "$nature-figure",
            "backend": "python",
        }
        for field, value in expected_profile.items():
            if profile.get(field) != value:
                errors.append(
                    f"formal-figure visual profile must set {field}={value!r}"
                )
        palette = profile.get("palette")
        if not isinstance(palette, dict) or palette.get("name") != "metbrewer_cassatt2":
            errors.append(
                "formal-figure visual profile must set palette.name='metbrewer_cassatt2'"
            )

    for relative in FORMAL_FIGURE_DIRS:
        if not (run_dir / relative).is_dir():
            errors.append(f"missing formal-figure directory: {relative}")

    required_files = (
        "validation/validation-handoff.md",
        "validation/claims/claim-evidence-map.md",
        "figure-prep/figure-plan.md",
        "figure-prep/figure-preparation-handoff.md",
        "paper-prep/structure/chapter-map-v0.md",
        "paper-prep/structure/chapter-map-v1.md",
        "paper-writing/plan/figure-table-slots.md",
        "paper-writing/manuscript/full-paper-v2.md",
        "formal-figures/scope/frozen-inputs.md",
        "formal-figures/style/visual-system.md",
        "formal-figures/style/paper.mplstyle",
        "formal-figures/style/theme.py",
        "formal-figures/figure-review.md",
        "formal-figures/figure-review-closure.md",
        "formal-figures/figure-coverage-map.md",
        "formal-figures/figure-manifest.md",
        "formal-figures/placement-and-caption-handoff.md",
        "formal-figures/figure-rendering-handoff.md",
        "formal-figures/previews/contact-sheet.pdf",
        "formal-figures/previews/in-paper-preview.pdf",
    )
    for relative in required_files:
        if not nonempty_file(run_dir / relative):
            errors.append(f"missing or empty formal-figure file: {relative}")

    dispatch_path = run_dir / "formal-figures/scope/dispatch-log.json"
    dispatch: object | None = None
    producer_units: set[str] = set()
    if not nonempty_file(dispatch_path):
        errors.append("missing or empty formal-figure dispatch log: formal-figures/scope/dispatch-log.json")
    else:
        try:
            dispatch = json.loads(dispatch_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid formal-figure dispatch log JSON: {exc}")
    if isinstance(dispatch, dict):
        if dispatch.get("metadata_only") is not True:
            errors.append("formal-figure dispatch log must declare metadata_only=true")
        tasks = dispatch.get("tasks")
        if not isinstance(tasks, list) or not tasks:
            errors.append("formal-figure dispatch log must contain non-empty tasks")
        else:
            roles_seen: set[str] = set()
            for index, task in enumerate(tasks, 1):
                if not isinstance(task, dict):
                    errors.append(f"formal-figure dispatch task {index} must be an object")
                    continue
                role = task.get("role")
                if isinstance(role, str):
                    roles_seen.add(role)
                if role not in {"question_visual_producer", "figure_portfolio_reviewer"}:
                    errors.append(f"formal-figure dispatch task {index} has unknown role: {role!r}")
                if role == "question_visual_producer" and isinstance(task.get("unit"), str):
                    producer_units.add(task["unit"])
                expected = {
                    "requested_model": "gpt-5.6-sol",
                    "requested_reasoning_effort": "high",
                    "fork_turns": "none",
                    "backend": "python",
                    "visual_profile": "cassatt2_quiet_journal_v1",
                    "palette": "metbrewer_cassatt2",
                }
                for field, value in expected.items():
                    if task.get(field) != value:
                        errors.append(
                            f"formal-figure dispatch task {index} must set {field}={value!r}"
                        )
                expected_skills = ["visualize-data", "ssci-plots", "nature-figure"]
                expected_invocations = ["$visualize-data", "$ssci-plots", "$nature-figure"]
                if task.get("required_skills") != expected_skills:
                    errors.append(
                        f"formal-figure dispatch task {index} must set "
                        f"required_skills={expected_skills!r}"
                    )
                if task.get("skill_invocations") != expected_invocations:
                    errors.append(
                        f"formal-figure dispatch task {index} must set "
                        f"skill_invocations={expected_invocations!r}"
                    )
                if not task.get("agent_handle"):
                    errors.append(f"formal-figure dispatch task {index} is missing agent_handle")
                brief_ref = task.get("task_brief")
                if not isinstance(brief_ref, str) or not nonempty_file(run_dir / brief_ref):
                    errors.append(
                        f"formal-figure dispatch task {index} has missing or empty task_brief"
                    )
                else:
                    brief_text = (run_dir / brief_ref).read_text(encoding="utf-8")
                    for marker in (
                        "gpt-5.6-sol",
                        "high",
                        "fork_turns=none",
                        "$visualize-data",
                        "$ssci-plots",
                        "$nature-figure",
                        "backend=python",
                        "cassatt2_quiet_journal_v1",
                        "metbrewer_cassatt2",
                        "ssci-plots-skill.lock.json",
                        "nature-figure-skill.lock.json",
                    ):
                        if marker not in brief_text:
                            errors.append(
                                f"formal-figure task brief for dispatch task {index} is missing {marker!r}"
                            )
            for required_role in ("question_visual_producer", "figure_portfolio_reviewer"):
                if required_role not in roles_seen:
                    errors.append(
                        f"formal-figure dispatch log is missing required role: {required_role}"
                    )

    question_root = run_dir / "formal-figures/questions"
    question_bundles = sorted(path for path in question_root.iterdir() if path.is_dir()) if question_root.is_dir() else []
    if not question_bundles:
        errors.append("formal-figures must contain at least one question ownership directory")
    for bundle in question_bundles:
        check_formal_figure_bundle(bundle, errors)
        if bundle.name not in producer_units:
            errors.append(
                f"formal-figure dispatch log has no sol-high producer task for question unit: {bundle.name}"
            )
    shared_root = run_dir / "formal-figures/shared"
    if shared_root.is_dir():
        for bundle in sorted(path for path in shared_root.iterdir() if path.is_dir()):
            check_formal_figure_bundle(bundle, errors)

    previews = run_dir / "formal-figures/previews"
    if previews.is_dir() and not any(nonempty_file(path) for path in previews.rglob("*")):
        warnings.append("formal-figure previews directory is empty; checker cannot confirm real-context QA")


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
        "routes/responses", "routes/change-requests",
    ]
    for relative in required_dirs:
        if not (run_dir / relative).is_dir():
            errors.append(f"missing directory: {relative}")

    metadata: dict[str, object] = {}
    for relative in (
        "inputs/source-manifest.json",
        "state/run-state.json",
        "state/mcm-skill-snapshot.json",
    ):
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
    mcm_snapshot = metadata.get("state/mcm-skill-snapshot.json")
    if isinstance(manifest, dict) and manifest.get("metadata_only") is not True:
        warnings.append("source-manifest.json should declare metadata_only=true")
    if isinstance(state, dict) and state.get("metadata_only") is not True:
        warnings.append("run-state.json should declare metadata_only=true")
    if isinstance(manifest, dict) and isinstance(state, dict):
        if manifest.get("source_snapshot_id") != state.get("source_snapshot_id"):
            errors.append("source snapshot differs between manifest and run state")
        if not manifest.get("materials"):
            warnings.append("no source files are registered")

    mcm_skill_drift_detected = check_mcm_skill_snapshot(mcm_snapshot, errors, warnings)

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
        route_files = (
            "routes/route-a.md",
            "routes/route-b.md",
            "routes/route-review.md",
            "literature/route-alignment/route-a/scout-memo.md",
            "literature/route-alignment/route-b/scout-memo.md",
            "literature/route-alignment/human-consultation/consultation-brief.md",
            "literature/route-alignment/human-consultation/response-record.md",
            "literature/route-alignment/evidence-review.md",
            "literature/route-alignment/route-evidence-handoff.md",
            "routes/responses/route-a-response.md",
            "routes/responses/route-b-response.md",
            "routes/model-candidate-briefing.md",
        )
        # The presentation preflight happens BEFORE asking the human.  Never
        # require a decision or final route handoff just to prepare that ask.
        if args.stage != "model-briefing":
            route_files += (
                "routes/human-model-decision.md",
                "routes/route-handoff.md",
            )
        for relative in route_files:
            path = run_dir / relative
            if not path.is_file() or path.stat().st_size == 0:
                errors.append(f"missing or empty report file: {relative}")
        presentation = "routes/model-selection-presentation.md"
        if not nonempty_file(run_dir / presentation):
            if args.stage == "model-briefing":
                errors.append(f"missing or empty report file: {presentation}")
            else:
                # Preserve historical run compatibility.  New L2C/H1 work
                # must explicitly use the stricter model-briefing preflight.
                warnings.append(
                    f"missing or empty model-selection presentation: {presentation}; "
                    "historical delivery is unverified; use --stage model-briefing for new L2C/H1 work"
                )
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
    if args.stage == "formal-figures":
        check_formal_figures(run_dir, errors, warnings)
    if args.stage == "final-delivery":
        check_final_delivery(run_dir, errors, warnings)
    if args.stage == "literature":
        check_literature(run_dir, errors, warnings)

    payload = {
        "stage": args.stage,
        "run_dir": str(run_dir),
        "markdown_content_parsed": False,
        "semantic_correctness_checked": False,
        "embedded_mcm_skill_files_checked": True,
        "embedded_mcm_skill_drift_detected": mcm_skill_drift_detected,
        "mcm_semantic_behavior_checked": False,
        "figure_aesthetic_checked": False,
        "formal_figure_data_accuracy_checked": False,
        "formal_figure_visual_quality_checked": False,
        "formal_figure_actual_model_identity_verified": False,
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
        "human_model_decision_authenticity_checked": False,
        "model_selection_presentation_content_checked": False,
        "model_selection_presentation_delivery_checked": False,
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
