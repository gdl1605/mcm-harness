#!/usr/bin/env python3
"""Create a run workspace with open Markdown handoffs and minimal runtime metadata."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def source_record(path: Path, index: int) -> dict[str, object]:
    stat = path.stat()
    return {
        "source_ref": f"SRC-{index:03d}",
        "name": path.name,
        "path": str(path.resolve()),
        "size_bytes": stat.st_size,
        "modified_at": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(timespec="seconds"),
        "sha256": sha256_file(path),
        "readability": "unchecked",
        "notes": ""
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path, help="New or empty run directory")
    parser.add_argument("--title", default="Untitled C problem")
    parser.add_argument("--source", action="append", default=[], type=Path, help="Raw source file; repeat as needed")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    run_dir = args.run_dir.resolve()
    if run_dir.exists() and any(run_dir.iterdir()):
        print(f"error: refusing to write into non-empty directory: {run_dir}", file=sys.stderr)
        return 2

    sources: list[Path] = []
    for raw in args.source:
        source = raw.resolve()
        if not source.is_file():
            print(f"error: --source must be an existing file: {source}", file=sys.stderr)
            return 2
        sources.append(source)

    directories = [
        "inputs", "state", "briefs", "submissions/W1", "submissions/W2",
        "submissions/W3R", "reviews/W3", "reviews/W4", "synthesis",
        "routes/responses",
        "literature/scope", "literature/route-alignment/search-briefs",
        "literature/route-alignment/route-a", "literature/route-alignment/route-b",
        "literature/route-alignment/sources",
        "literature/route-alignment/human-consultation",
        "literature/citation-preparation/search-briefs",
        "literature/citation-preparation/scouts",
        "literature/citation-preparation/sources",
        "data/briefs", "data/contracts", "data/profiling", "data/decisions",
        "data/pipeline/src", "data/pipeline/tests", "data/staging",
        "data/processed/canonical", "data/processed/analytical",
        "data/reviews", "data/paper-notes",
        "modeling/briefs/M1", "modeling/briefs/M3", "modeling/briefs/M4",
        "modeling/briefs/M5", "modeling/specs", "modeling/plans",
        "modeling/challenges", "modeling/src", "modeling/configs",
        "modeling/runs", "modeling/diagnostics", "modeling/adjustments",
        "modeling/results/candidate-tables", "modeling/results/interfaces",
        "modeling/paper-notes", "modeling/change-requests",
        "validation/briefs/V1", "validation/briefs/V3",
        "validation/briefs/V4", "validation/briefs/V6",
        "validation/scope", "validation/reviews", "validation/dockets",
        "validation/probes", "validation/responses", "validation/decisions",
        "validation/interfaces", "validation/claims",
        "validation/change-requests",
        # Post-V6 figure-preparation branch.  These are deliberately empty
        # ownership roots; question packages, candidate directories and
        # semantic Markdown are created by the native subagents only when the
        # branch is actually started.
        "figure-prep/scope", "figure-prep/questions",
        "figure-prep/cross-question", "figure-prep/change-requests",
        # Post-V6 paper-preparation branch.  These are empty ownership roots;
        # semantic materials are created only when CP0 explicitly starts.
        "paper-prep/briefs", "paper-prep/scope", "paper-prep/structure",
        "paper-prep/questions", "paper-prep/shared",
        "paper-prep/integration", "paper-prep/change-requests",
        # Formal Markdown writing branch.  Leader owns manuscript/responses;
        # question writers and reviewers receive separate roots at runtime.
        "paper-writing/briefs", "paper-writing/scope", "paper-writing/plan",
        "paper-writing/sections", "paper-writing/manuscript",
        "paper-writing/reviews/closure", "paper-writing/responses",
        "paper-writing/change-requests",
        # Final delivery creates only ownership roots.  Candidate files,
        # semantic reports and human handoff are created when FD0 explicitly
        # starts; no successful package is implied by initialization.
        "final-delivery/briefs", "final-delivery/scope",
        "final-delivery/source", "final-delivery/supporting-materials/results",
        "final-delivery/candidate", "final-delivery/reviews",
        "final-delivery/human-review",
    ]
    for relative in directories:
        (run_dir / relative).mkdir(parents=True, exist_ok=True)

    token = uuid.uuid4().hex[:12].upper()
    run_id = f"RUN-{token}"
    snapshot_id = f"SNAPSHOT-{token}"
    now = utc_now()

    manifest = {
        "metadata_only": True,
        "schema_version": "0.4.0",
        "source_snapshot_id": snapshot_id,
        "created_at": now,
        "materials": [source_record(path, index) for index, path in enumerate(sources, 1)],
        "known_gaps": [] if sources else ["No source files were registered during initialization."],
        "semantic_interpretation_location": "Markdown reports, not this JSON file"
    }
    write_json(run_dir / "inputs/source-manifest.json", manifest)

    state = {
        "metadata_only": True,
        "schema_version": "0.4.0",
        "run_id": run_id,
        "title": args.title,
        "phase": "SOURCE_FREEZE",
        "source_snapshot_id": snapshot_id,
        "active_tasks": [],
        "report_paths": [],
        "created_at": now,
        "updated_at": now,
        "scope_boundary": (
            "The main modeling/validation chain stops at validation/validation-handoff.md. "
            "When post-V6 preparation branches are explicitly started, figure preparation stops "
            "after figure-prep/figure-preparation-handoff.md and paper preparation stops after "
            "paper-prep/paper-framework-handoff.md. Formal Markdown writing stops after "
            "paper-writing/formal-paper-handoff.md. When FD0 is explicitly started with formal figures, "
            "verified literature/references handoff, official rules, final result data and executed scripts, final delivery stops "
            "after final-delivery/final-delivery-handoff.md with status AWAITING_HUMAN_FINALIZATION. "
            "Formal figure rendering, post-review human tuning and actual submission "
            "remain outside this harness. Semantic content belongs in Markdown reports."
        )
    }
    write_json(run_dir / "state/run-state.json", state)

    print(f"initialized: {run_dir}")
    print(f"run_id: {run_id}")
    print(f"source_snapshot_id: {snapshot_id}")
    print(f"registered_sources: {len(sources)}")
    print("next: the primary Agent follows AGENTS.md and starts W1 with native subagents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
