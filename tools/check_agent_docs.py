"""Validate maintained agent-facing Markdown and MkDocs navigation offline."""

from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
LIMITS = {
    "AGENTS.md": 12_000,
    "README.md": 12_000,
    "docs/index.md": 10_000,
    "docs/architecture/PROJECT-CONCEPT.md": 16_000,
    "docs/architecture/ROADMAP.md": 12_000,
    "docs/research/index.md": 10_000,
    "docs/development/agent-workflow.md": 16_000,
    "docs/development/coding-standards.md": 12_000,
    "docs/development/testing.md": 10_000,
    "docs/development/writing-standards.md": 12_000,
    "docs/development/document-budgets.md": 10_000,
    "docs/issue-operating-procedure.md": 10_000,
    "docs/research/reproducibility.md": 12_000,
    "docs/teaching-standards.md": 10_000,
    "docs/glossary.md": 10_000,
}
NEW_POLICY_DOCS = {
    "AGENTS.md",
    "README.md",
    *[name for name in LIMITS if name.startswith("docs/development/")],
    "docs/issue-operating-procedure.md",
    "docs/research/reproducibility.md",
    "docs/teaching-standards.md",
    "docs/glossary.md",
}
NAV_REQUIRED = {
    "docs/development/agent-workflow.md",
    "docs/development/coding-standards.md",
    "docs/development/testing.md",
    "docs/development/writing-standards.md",
    "docs/development/document-budgets.md",
    "docs/issue-operating-procedure.md",
    "docs/research/reproducibility.md",
    "docs/teaching-standards.md",
    "docs/glossary.md",
}
LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
NAV_PATTERN = re.compile(r"^\s*-\s+[^:\n]+:\s+([^\s#]+\.md)\s*$", re.MULTILINE)


def main() -> int:
    errors: list[str] = []
    counts = 0
    for name, limit in LIMITS.items():
        path = ROOT / name
        if not path.is_file():
            errors.append(f"MISSING {name}")
            continue
        text = path.read_text(encoding="utf-8")
        counts += 1
        if len(text) > limit:
            errors.append(f"BUDGET {name}: {len(text)} > {limit}")
        if name in NEW_POLICY_DOCS and ("\u2013" in text or "\u2014" in text):
            errors.append(f"DASH {name}: U+2013/U+2014")
        for match in LINK_PATTERN.finditer(text):
            raw = match.group(1).split("#", 1)[0].strip()
            if not raw or raw.startswith(("http://", "https://", "mailto:")):
                continue
            if raw.startswith("/"):
                errors.append(f"ABSOLUTE_LINK {name}: {raw}")
                continue
            target = (path.parent / raw).resolve()
            if not target.is_relative_to(ROOT) or not target.exists():
                errors.append(f"BROKEN_LINK {name}: {raw}")
        if name in NAV_REQUIRED:
            back = "index.md" if path.parent == ROOT / "docs" else "../index.md"
            if f"({back})" not in text:
                errors.append(f"NO_BACKLINK {name}: {back}")
    agent = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    headers = re.findall(r"^## (.+)$", agent, re.MULTILINE)
    if len(headers) != 2:
        errors.append(f"AGENTS_SECTION_COUNT: {len(headers)}")
    nav = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    nav_files = set(NAV_PATTERN.findall(nav))
    for name in sorted(NAV_REQUIRED):
        if name.removeprefix("docs/") not in nav_files:
            errors.append(f"NOT_IN_NAV {name}")
    for nav_file in nav_files:
        if not (ROOT / "docs" / nav_file).is_file():
            errors.append(f"NAV_MISSING_FILE {nav_file}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if "(AGENTS.md)" not in readme or "(docs/index.md)" not in agent:
        errors.append("ENTRYPOINT_LINKS")
    for err in errors:
        print(f"[FAIL] {err}")
    if errors:
        print(f"[FAIL] {len(errors)} documentation checks")
        return 1
    print(f"[DONE] {counts} Markdown budgets, links, policy, and navigation checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
