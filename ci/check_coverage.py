"""Учебный quality gate для coverage.py JSON после объединения тестовых jobs."""

from __future__ import annotations

import json
import sys
from pathlib import Path


MIN_LINE = 80.0
MIN_BRANCH = 70.0
MIN_CRITICAL_LINE = 95.0
MIN_CRITICAL_BRANCH = 90.0
CRITICAL_AREAS = ("auth", "pricing", "orders", "payments")


def pct(numerator: int, denominator: int) -> float:
    return 100.0 * numerator / denominator if denominator else 0.0


def percentages(summary: dict) -> tuple[float, float]:
    return (
        pct(summary["covered_lines"], summary["num_statements"]),
        pct(summary["covered_branches"], summary["num_branches"]),
    )


def is_in_area(filename: str, area: str) -> bool:
    normalized = filename.replace("\\", "/")
    return f"/shop/{area}/" in normalized or normalized.endswith(f"/shop/{area}.py")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_coverage.py reports/coverage.json", file=sys.stderr)
        return 2

    report = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    total_line, total_branch = percentages(report["totals"])
    failures: list[str] = []
    print(f"Total: lines {total_line:.2f}% (min {MIN_LINE}%), "
          f"branches {total_branch:.2f}% (min {MIN_BRANCH}%)")
    if total_line < MIN_LINE:
        failures.append("overall line coverage")
    if total_branch < MIN_BRANCH:
        failures.append("overall branch coverage")

    for area in CRITICAL_AREAS:
        summaries = [entry["summary"] for name, entry in report["files"].items()
                     if is_in_area(name, area)]
        if not summaries:
            failures.append(f"missing critical area: {area}")
            continue
        combined = {key: sum(item[key] for item in summaries)
                    for key in ("covered_lines", "num_statements", "covered_branches", "num_branches")}
        line, branch = percentages(combined)
        print(f"{area}: lines {line:.2f}% (min {MIN_CRITICAL_LINE}%), "
              f"branches {branch:.2f}% (min {MIN_CRITICAL_BRANCH}%)")
        if line < MIN_CRITICAL_LINE:
            failures.append(f"{area} line coverage")
        if branch < MIN_CRITICAL_BRANCH:
            failures.append(f"{area} branch coverage")

    if failures:
        print("FAILED: " + ", ".join(failures), file=sys.stderr)
        return 1
    print("Coverage gate passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
