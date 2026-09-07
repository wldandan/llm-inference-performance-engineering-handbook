"""Print a baseline-vs-optimized comparison table from bench_client.py reports.

Usage:
    python3 compare.py baseline.json optimized.json [more.json ...]

The first file passed is treated as the baseline; every later file gets a
"vs baseline" percentage column. This mirrors every workshop's Step 5
("对比总结") without each workshop needing its own table-printing code.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

DEFAULT_METRICS = [
    "ttft_avg_ms",
    "ttft_p95_ms",
    "itl_avg_ms",
    "total_latency_p95_ms",
    "tokens_per_second_sum",
]


def pct_change(baseline: float | None, value: float | None) -> float | None:
    if baseline is None or value is None or baseline == 0:
        return None
    return round((value - baseline) / baseline * 100.0, 1)


def load_reports(paths: list[str]) -> list[dict[str, Any]]:
    reports = []
    for path in paths:
        with open(path, encoding="utf-8") as f:
            reports.append(json.load(f))
    return reports


def format_table(reports: list[dict[str, Any]], metrics: list[str] | None = None) -> str:
    metrics = metrics or DEFAULT_METRICS
    baseline_summary = reports[0]["summary"]

    header = ["metric"] + [r.get("label", f"run{i}") for i, r in enumerate(reports)]
    lines = [" | ".join(header)]

    for metric in metrics:
        row = [metric]
        for i, report in enumerate(reports):
            value = report["summary"].get(metric)
            cell = "n/a" if value is None else str(value)
            if i > 0:
                change = pct_change(baseline_summary.get(metric), value)
                if change is not None:
                    sign = "+" if change >= 0 else ""
                    cell += f" ({sign}{change}%)"
            row.append(cell)
        lines.append(" | ".join(row))

    for i, report in enumerate(reports):
        failures = report["summary"].get("failures", 0)
        if failures:
            lines.append(f"WARNING: {report.get('label', f'run{i}')} has failures={failures}")

    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("reports", nargs="+", help="bench_client.py JSON report files, baseline first")
    parser.add_argument("--metrics", nargs="*", default=None, help="Override the default metric list")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    reports = load_reports(args.reports)
    print(format_table(reports, metrics=args.metrics))
    if any(r["summary"].get("failures") for r in reports):
        sys.exit(1)


if __name__ == "__main__":
    main()
