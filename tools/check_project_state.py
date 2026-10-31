"""Offline consistency checks for a scientific evidence snapshot.

PROJECT_STATE.yaml is intentionally the JSON subset of YAML 1.2 so that
the standard library can parse it without installing another dependency.
This is a source-linked research registry, not a job queue or controller.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "PROJECT_STATE.yaml"
SHA = re.compile(r"^[0-9a-f]{40}$")
RUN = re.compile(
    r"^https://github\.com/MatPomGit/eeg-neurolyze/actions/runs/[1-9]\d*$"
)
MILESTONES = {f"M{i:02d}" for i in range(1, 8)}
LEVELS = {
    "PLANNED",
    "SOFTWARE_TESTED",
    "REAL_DATA_ANALYSIS",
    "HARDWARE_MEASURED",
    "DATASET_VALIDATED",
}
IMPLEMENTATIONS = {"present", "partial", "planned"}
BLOCKER_STATES = {"WAITING_FOR_USER", "HUMAN_REQUIRED", "UNRESOLVED"}
ELEVATED = {"REAL_DATA_ANALYSIS", "HARDWARE_MEASURED", "DATASET_VALIDATED"}


def read_state(path: Path = STATE) -> dict:
    """Load the deliberately restricted JSON-compatible YAML snapshot."""
    with path.open(encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError("snapshot root must be a mapping")
    return value


def validate_state(state: dict, root: Path = ROOT) -> list[str]:
    """Return violations without modifying files or contacting GitHub."""
    errors: list[str] = []

    def error(location: str, message: str) -> None:
        errors.append(f"{location}: {message}")

    def check_paths(paths: object, location: str, allow_empty: bool = False) -> None:
        if not isinstance(paths, list) or (not paths and not allow_empty):
            error(location, "source paths must be a nonempty list")
            return
        for value in paths:
            if not isinstance(value, str) or not value:
                error(location, "empty or invalid path")
                continue
            relative = Path(value)
            target = (root / relative).resolve()
            if relative.is_absolute() or not target.is_relative_to(root.resolve()):
                error(location, f"path escapes repository: {value}")
            elif not target.is_file():
                error(location, f"missing file: {value}")

    def check_issue_ids(values: object, location: str) -> None:
        if not isinstance(values, list) or any(
            type(value) is not int or value <= 0 for value in values
        ):
            error(location, "issue references must be positive integers")
        elif len(values) != len(set(values)):
            error(location, "duplicate issue reference")

    if state.get("schema_version") != 1:
        error("schema_version", "unsupported schema version")
    if state.get("kind") != "scientific_evidence_snapshot":
        error("kind", "must not be a work queue or approval controller")
    if state.get("repository") != "MatPomGit/eeg-neurolyze":
        error("repository", "incorrect owning repository")

    baseline = state.get("snapshot")
    if not isinstance(baseline, dict):
        error("snapshot", "missing baseline and provenance")
    else:
        if not SHA.fullmatch(str(baseline.get("base_sha", ""))):
            error("snapshot.base_sha", "invalid full commit SHA")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(baseline.get("observed_date", ""))):
            error("snapshot.observed_date", "invalid observation date")
        if not baseline.get("note"):
            error("snapshot.note", "state that this is not live authorization")

    check_paths(state.get("authoritative_sources"), "authoritative_sources")
    if set(state.get("scientific_evidence_levels", [])) != LEVELS:
        error("scientific_evidence_levels", "unexpected scientific level vocabulary")

    milestones = state.get("milestones")
    if not isinstance(milestones, list):
        error("milestones", "missing milestone list")
        milestones = []
    ids: list[str] = []
    for item in milestones:
        if not isinstance(item, dict):
            error("milestones", "entry is not a mapping")
            continue
        mid = item.get("id")
        location = f"milestones.{mid}"
        ids.append(mid)
        implementation = item.get("implementation")
        level = item.get("evidence_level")
        if implementation not in IMPLEMENTATIONS:
            error(location, "unknown implementation status")
        if level not in LEVELS:
            error(location, "unknown scientific evidence level")
        if implementation == "planned" and level != "PLANNED":
            error(location, "planned feature cannot claim validation")
        if not isinstance(item.get("verified_scope"), str) or not item["verified_scope"]:
            error(location, "verified_scope is required")
        check_paths(item.get("source_paths"), location)
        check_issue_ids(item.get("related_issues"), location)
        verification = item.get("verification")
        if level == "SOFTWARE_TESTED":
            if not isinstance(verification, dict):
                error(location, "software test requires source-pinned CI evidence")
            else:
                if verification.get("kind") != "github_actions":
                    error(location, "unsupported CI source")
                if not RUN.fullmatch(str(verification.get("run_url", ""))):
                    error(location, "invalid CI run URL")
                if not SHA.fullmatch(str(verification.get("sha", ""))):
                    error(location, "CI must cite the full exact revision")
                if verification.get("scope") != "software_only":
                    error(location, "software evidence must be scoped")
                check_paths(verification.get("test_paths"), location + ".verification")
        if level == "PLANNED" and verification is not None:
            error(location, "planned feature cannot contain verified CI evidence")
        if level in ELEVATED:
            artifact = item.get("scientific_artifact")
            if not isinstance(artifact, str) or not artifact:
                error(location, "higher scientific level requires an evidence artifact")
            else:
                check_paths([artifact], location + ".scientific_artifact")
            if item.get("reviewed_provenance") is not True:
                error(location, "higher scientific level requires explicit provenance review")
        if mid == "M02" and item.get("synthetic_only") is not True:
            if level not in ELEVATED:
                error(location, "real-data claim without scientific evidence")
        if mid == "M03" and item.get("physical_qualification") is True:
            if level not in {"HARDWARE_MEASURED", "DATASET_VALIDATED"}:
                error(location, "hardware qualification exceeds evidence level")

    if len(ids) != len(set(ids)) or set(ids) != MILESTONES:
        error("milestones", "M01-M07 must each appear exactly once")

    publications = state.get("publications")
    if not isinstance(publications, list) or not publications:
        error("publications", "missing publication map")
        publications = []
    paper_ids: list[str] = []
    for item in publications:
        if not isinstance(item, dict):
            error("publications", "entry is not a mapping")
            continue
        pid = item.get("id")
        paper_ids.append(pid)
        location = f"publications.{pid}"
        if type(item.get("origin_issue")) is not int or item["origin_issue"] <= 0:
            error(location, "missing originating issue")
        if item.get("status") != "proposed":
            error(location, "unsupported manuscript state requires a reviewed schema change")
        if item.get("evidence_level") != "PLANNED":
            error(location, "paper proposal cannot claim research results")
        if any(item.get(key) is not None for key in
               ("manuscript_path", "approved_title", "submission")):
            error(location, "proposal cannot invent manuscript, title or submission")
        check_paths(item.get("source_paths"), location)
        if "depends_on_issues" in item:
            check_issue_ids(item["depends_on_issues"], location)
    if len(paper_ids) != len(set(paper_ids)):
        error("publications", "duplicate paper ID")

    blockers = state.get("blockers")
    if not isinstance(blockers, list):
        error("blockers", "missing unresolved scientific/safety blockers")
        blockers = []
    blocker_ids: list[int] = []
    for item in blockers:
        if not isinstance(item, dict):
            error("blockers", "entry is not a mapping")
            continue
        number = item.get("issue")
        if type(number) is not int or number <= 0:
            error("blockers", "invalid referenced issue")
        else:
            blocker_ids.append(number)
        if item.get("status") not in BLOCKER_STATES:
            error("blockers", "unknown blocker status")
        if not item.get("domain") or not item.get("evidence"):
            error("blockers", "missing domain or explicit blocker explanation")
    if len(blocker_ids) != len(set(blocker_ids)):
        error("blockers", "duplicate blocker")

    linked = state.get("issue_references")
    check_issue_ids(linked, "issue_references")
    if isinstance(linked, list) and not set(range(21, 36)).issubset(set(linked)):
        error("issue_references", "missing source Issue in #21-#35")
    return errors


def main() -> int:
    try:
        errors = validate_state(read_state())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"[FAIL] Cannot load evidence snapshot: {exc}")
        return 1
    for message in errors:
        print(f"[FAIL] {message}")
    if errors:
        print(f"[FAIL] {len(errors)} scientific index checks")
        return 1
    print("[DONE] Scientific evidence index: schema, paths and evidence gates PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
