#!/usr/bin/env python3
"""Calculate a synthetic client-side LLM metrics report from JSONL records."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def nearest_rank_percentile(values: list[float], percentile: float) -> float:
    if not values:
        raise ValueError("values cannot be empty")
    if not 0 < percentile <= 100:
        raise ValueError("percentile must be in (0, 100]")
    ordered = sorted(values)
    rank = math.ceil(percentile / 100 * len(ordered))
    return ordered[rank - 1]


def _number(record: dict, name: str) -> float:
    value = record.get(name)
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{name} must be a number")
    return value


def request_metrics(record: dict) -> dict[str, object]:
    request_id = record.get("request_id")
    if not isinstance(request_id, str) or not request_id:
        raise ValueError("request_id must be a non-empty string")
    start_ms = _number(record, "start_ms")
    end_ms = _number(record, "end_ms")
    if end_ms < start_ms:
        raise ValueError("end_ms must not precede start_ms")

    success = record.get("success")
    if not isinstance(success, bool):
        raise ValueError("success must be a boolean")
    prompt_tokens = record.get("prompt_tokens")
    output_tokens = record.get("output_tokens")
    if not isinstance(prompt_tokens, int) or prompt_tokens < 0:
        raise ValueError("prompt_tokens must be a non-negative integer")
    if not isinstance(output_tokens, int) or output_tokens < 0:
        raise ValueError("output_tokens must be a non-negative integer")
    cost_usd = _number(record, "cost_usd")
    if cost_usd < 0:
        raise ValueError("cost_usd cannot be negative")

    token_times = record.get("token_times_ms")
    if not isinstance(token_times, list) or any(
        not isinstance(value, (int, float)) or isinstance(value, bool)
        for value in token_times
    ):
        raise ValueError("token_times_ms must be a list of numbers")
    if token_times != sorted(token_times):
        raise ValueError("token_times_ms must be sorted")
    if token_times and (token_times[0] < start_ms or token_times[-1] > end_ms):
        raise ValueError("token timestamps must stay inside the request window")

    if not success:
        if token_times or output_tokens:
            raise ValueError("failed records cannot claim completed output tokens")
        return {
            "request_id": request_id,
            "success": False,
            "prompt_tokens": prompt_tokens,
            "output_tokens": 0,
            "cost_usd": cost_usd,
            "e2e_ms": end_ms - start_ms,
            "ttft_ms": None,
            "itls_ms": [],
            "tpot_ms": None,
        }

    if output_tokens <= 0:
        raise ValueError("successful records require output_tokens > 0")
    if len(token_times) != output_tokens:
        raise ValueError("output_tokens must equal the token_times_ms count")

    itls = [current - previous for previous, current in zip(token_times, token_times[1:])]
    return {
        "request_id": request_id,
        "success": True,
        "prompt_tokens": prompt_tokens,
        "output_tokens": output_tokens,
        "cost_usd": cost_usd,
        "e2e_ms": end_ms - start_ms,
        "ttft_ms": token_times[0] - start_ms,
        "itls_ms": itls,
        "tpot_ms": sum(itls) / len(itls) if itls else None,
    }


def _distribution(values: list[float]) -> dict[str, float | int | None]:
    if not values:
        return {"count": 0, "mean": None, "p50": None, "p95": None, "p99": None}
    return {
        "count": len(values),
        "mean": sum(values) / len(values),
        "p50": nearest_rank_percentile(values, 50),
        "p95": nearest_rank_percentile(values, 95),
        "p99": nearest_rank_percentile(values, 99),
    }


def build_report(
    records: list[dict],
    *,
    ttft_slo_ms: float,
    e2e_slo_ms: float,
    workload: dict | None = None,
) -> dict[str, object]:
    if not records:
        raise ValueError("records cannot be empty")
    if ttft_slo_ms <= 0 or e2e_slo_ms <= 0:
        raise ValueError("SLO thresholds must be positive")

    per_request = [request_metrics(record) for record in records]
    successful = [item for item in per_request if item["success"]]
    failed = [item for item in per_request if not item["success"]]
    starts = [_number(record, "start_ms") for record in records]
    ends = [_number(record, "end_ms") for record in records]
    window_ms = max(ends) - min(starts)
    if window_ms <= 0:
        raise ValueError("measurement window must be positive")
    window_seconds = window_ms / 1000

    output_tokens = sum(int(item["output_tokens"]) for item in successful)
    good_requests = sum(
        1
        for item in successful
        if float(item["ttft_ms"]) <= ttft_slo_ms
        and float(item["e2e_ms"]) <= e2e_slo_ms
    )
    ttfts = [float(item["ttft_ms"]) for item in successful]
    e2es = [float(item["e2e_ms"]) for item in successful]
    tpots = [float(item["tpot_ms"]) for item in successful if item["tpot_ms"] is not None]
    itls = [float(value) for item in successful for value in item["itls_ms"]]
    total_cost = sum(float(item["cost_usd"]) for item in per_request)

    return {
        "mode": "synthetic_client_metrics",
        "note": "报告用于演示指标口径，不是 Benchmark，也不代表任何真实服务性能。",
        "measurement_contract": {
            "source": "synthetic_request_records",
            "clock": "client_wall_clock_ms",
            "window": "min(start_ms) to max(end_ms)",
            "percentile_method": "nearest_rank",
            "tpot_definition": "mean interval between observed output tokens",
            "slo": {"ttft_ms": ttft_slo_ms, "e2e_ms": e2e_slo_ms},
        },
        "workload": workload or {},
        "requests": {
            "total": len(per_request),
            "successful": len(successful),
            "failed": len(failed),
        },
        "latency_ms": {
            "ttft": _distribution(ttfts),
            "e2e": _distribution(e2es),
            "tpot": _distribution(tpots),
            "itl": _distribution(itls),
        },
        "throughput": {
            "measurement_window_seconds": window_seconds,
            "output_tokens": output_tokens,
            "output_tokens_per_second": output_tokens / window_seconds,
            "requests_per_second": len(successful) / window_seconds,
            "good_requests": good_requests,
            "goodput_requests_per_second": good_requests / window_seconds,
        },
        "cost": {
            "total_cost_usd": total_cost,
            "usd_per_million_output_tokens": (
                total_cost / output_tokens * 1_000_000 if output_tokens else None
            ),
            "usd_per_successful_request": (
                total_cost / len(successful) if successful else None
            ),
        },
        "per_request": per_request,
    }


def load_jsonl(path: Path) -> list[dict]:
    records = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"line {line_number}: invalid JSON: {exc.msg}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"line {line_number}: record must be an object")
        records.append(value)
    return records


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, nargs="?", default=Path(__file__).with_name("sample.jsonl"))
    parser.add_argument("--ttft-slo-ms", type=float, default=250)
    parser.add_argument("--e2e-slo-ms", type=float, default=800)
    parser.add_argument("--output", type=Path)
    return parser


def main() -> int:
    args = _parser().parse_args()
    report = build_report(
        load_jsonl(args.input),
        ttft_slo_ms=args.ttft_slo_ms,
        e2e_slo_ms=args.e2e_slo_ms,
        workload={"name": "sample-interactive-chat", "source": args.input.name},
    )
    output = json.dumps(report, ensure_ascii=False, indent=2)
    print(output)
    if args.output:
        args.output.write_text(output + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
