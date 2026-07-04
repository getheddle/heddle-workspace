#!/usr/bin/env python3
"""Check the small invariants that keep the Hooman docs lean."""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

LINE_BUDGETS = {
    "hooman-contract.md": 90,
    "skills/hooman-assistant/SKILL.md": 120,
}

RULE_FILES = {
    "hooman-contract.md": r"\*\*(T\d+)\s+—",
    "skills/hooman-assistant/SKILL.md": r"-\s+([a-z]+\.\d+)\s+—",
    "skills/hooman-assistant/references/workspace.md": r"-\s+(ws\.\d+)\s+—",
}

CONTRACTS_FILE = "skills/hooman-assistant/references/contracts.md"
REQUIRED_CONTRACT_MARKERS = {
    "C-R": [
        "implemented: nothing",
        "<decisions>",
        '<evidence_map coverage="inspected=N inferred=N unverified=N">',
        "<recommendation>",
        "<rejected>",
        "<not_done>",
    ],
    "C-M": [
        "scope: <the locked-scope brief this executes>",
        "<files_changed>",
        "<tests>",
        "<risks>",
        "<manual_checks>",
        "<rollback>",
    ],
    "C-A": [
        "<sources>",
        "<opposing>",
        "<implications>",
        "<uncertainty>",
    ],
}


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def check_line_budgets(errors: list[str]) -> None:
    for path, budget in LINE_BUDGETS.items():
        count = len(text(path).splitlines())
        if count > budget:
            errors.append(f"{path}: {count} lines exceeds budget {budget}")


def check_rule_ids(errors: list[str]) -> None:
    all_ids: list[tuple[str, str]] = []
    for path, pattern in RULE_FILES.items():
        found = re.findall(pattern, text(path))
        counts = Counter(found)
        for rule_id, count in counts.items():
            if count > 1:
                errors.append(f"{path}: duplicate rule id {rule_id}")
        all_ids.extend((rule_id, path) for rule_id in found)

    global_counts = Counter(rule_id for rule_id, _ in all_ids)
    for rule_id, count in global_counts.items():
        if count > 1:
            paths = sorted({path for found_id, path in all_ids if found_id == rule_id})
            errors.append(f"duplicate rule id {rule_id} across {', '.join(paths)}")


def check_contract_skeletons(errors: list[str]) -> None:
    body = text(CONTRACTS_FILE)
    for contract, markers in REQUIRED_CONTRACT_MARKERS.items():
        if f"## {contract} " not in body:
            errors.append(f"{CONTRACTS_FILE}: missing {contract} section")
            continue
        for marker in markers:
            if marker not in body:
                errors.append(f"{CONTRACTS_FILE}: {contract} skeleton missing {marker}")


def main() -> int:
    errors: list[str] = []
    check_line_budgets(errors)
    check_rule_ids(errors)
    check_contract_skeletons(errors)

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1

    print("docs ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
