"""Reusable load-testing client shared by every workshop.

Sends real streaming chat-completion requests to an OpenAI-compatible server
(vLLM, SGLang, ...) and reports client-observed TTFT / ITL / throughput. This
module intentionally has no vLLM/SGLang import and no network mocking: the
metrics math is pure and unit-tested, the network path is exercised for real
when a workshop actually runs it against a live server.

Each workshop supplies its own `requests.jsonl` (one JSON object per line:
`{"prompt": "...", "max_tokens": 128}`) so the *shape* of the load (long vs
short prompts, shared prefixes, ...) lives in the workshop directory, not in
this shared client.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Any


def build_payload(model: str, prompt: str, max_tokens: int, temperature: float = 0.0) -> dict[str, Any]:
    return {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": True,
        "stream_options": {"include_usage": True},
    }


def percentile(values: list[float], pct: float) -> float | None:
    if not values:
        return None
    values = sorted(values)
    if len(values) == 1:
        return values[0]
    rank = (len(values) - 1) * pct / 100.0
    lo = int(rank)
    hi = min(lo + 1, len(values) - 1)
    weight = rank - lo
    return values[lo] * (1 - weight) + values[hi] * weight


@dataclass
class MetricsCollector:
    start_time: float
    first_token_time: float | None = None
    last_token_time: float | None = None
    token_timestamps: list[float] = field(default_factory=list)
    chunks: int = 0
    characters: int = 0
    prompt_tokens: int | None = None
    completion_tokens: int | None = None

    def on_token(self, timestamp: float, text: str) -> None:
        if text == "":
            return
        if self.first_token_time is None:
            self.first_token_time = timestamp
        self.last_token_time = timestamp
        self.token_timestamps.append(timestamp)
        self.chunks += 1
        self.characters += len(text)

    def set_usage(self, prompt_tokens: int | None, completion_tokens: int | None) -> None:
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens

    def finish(self, end_time: float) -> dict[str, Any]:
        timestamps = self.token_timestamps
        intervals = [
            (timestamps[i] - timestamps[i - 1]) * 1000.0 for i in range(1, len(timestamps))
        ]
        output_units = self.completion_tokens if self.completion_tokens is not None else self.chunks
        total_seconds = max(end_time - self.start_time, 1e-9)
        return {
            "success": True,
            "prompt_tokens": self.prompt_tokens,
            "output_tokens": self.completion_tokens,
            "stream_chunks": self.chunks,
            "output_characters": self.characters,
            "ttft_ms": round((self.first_token_time - self.start_time) * 1000.0, 2)
            if self.first_token_time is not None
            else None,
            "itl_avg_ms": round(sum(intervals) / len(intervals), 2) if intervals else None,
            "itl_p95_ms": round(percentile(intervals, 95), 2) if intervals else None,
            "total_latency_ms": round(total_seconds * 1000.0, 2),
            "tokens_per_second": round(output_units / total_seconds, 2) if output_units else None,
        }


def load_request_plan(path: str, count: int, default_max_tokens: int = 128) -> list[dict[str, Any]]:
    """Load a workshop's requests.jsonl and cycle it out to `count` items.

    Each line is a JSON object with at least a "prompt" field and an
    optional "max_tokens" field. Cycling (rather than requiring the file to
    already have `count` lines) lets a workshop keep a short, readable
    requests.jsonl that still supports arbitrary concurrency/request counts.
    """
    rows: list[dict[str, Any]] = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            if "prompt" not in row:
                raise ValueError(f"{path}: every line must have a 'prompt' field")
            row.setdefault("max_tokens", default_max_tokens)
            rows.append(row)
    if not rows:
        raise ValueError(f"{path}: no request rows found")
    return [rows[i % len(rows)] for i in range(count)]


def parse_sse_payload(line: bytes) -> dict[str, Any] | None:
    text = line.decode("utf-8").strip()
    if not text or not text.startswith("data:"):
        return None
    data = text[len("data:") :].strip()
    if data == "[DONE]":
        return {"done": True}
    return json.loads(data)


def extract_delta_text(payload: dict[str, Any]) -> str:
    choices = payload.get("choices") or []
    if not choices:
        return ""
    delta = choices[0].get("delta") or {}
    content = delta.get("content")
    return content if isinstance(content, str) else ""


def extract_usage(payload: dict[str, Any]) -> tuple[int | None, int | None]:
    usage = payload.get("usage")
    if not usage:
        return None, None
    return usage.get("prompt_tokens"), usage.get("completion_tokens")


def request_once(
    base_url: str,
    api_key: str,
    model: str,
    prompt: str,
    max_tokens: int,
    temperature: float,
    timeout: float,
) -> dict[str, Any]:
    url = base_url.rstrip("/") + "/chat/completions"
    payload = build_payload(model=model, prompt=prompt, max_tokens=max_tokens, temperature=temperature)
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    start = time.perf_counter()
    collector = MetricsCollector(start_time=start)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            for raw_line in response:
                now = time.perf_counter()
                parsed = parse_sse_payload(raw_line)
                if parsed is None:
                    continue
                if parsed.get("done"):
                    break
                prompt_tokens, completion_tokens = extract_usage(parsed)
                if prompt_tokens is not None or completion_tokens is not None:
                    collector.set_usage(prompt_tokens, completion_tokens)
                collector.on_token(now, extract_delta_text(parsed))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        return {"success": False, "error": f"HTTP {exc.code}: {detail}"}
    except Exception as exc:  # pragma: no cover - real network failure path
        return {"success": False, "error": str(exc)}
    return collector.finish(end_time=time.perf_counter())


def gpu_snapshot() -> dict[str, Any] | None:
    if not shutil.which("nvidia-smi"):
        return None
    cmd = [
        "nvidia-smi",
        "--query-gpu=name,utilization.gpu,memory.used,memory.total",
        "--format=csv,noheader,nounits",
    ]
    try:
        output = subprocess.check_output(cmd, text=True, timeout=5).strip()
    except Exception:
        return None
    gpus = []
    for line in output.splitlines():
        name, util, mem_used, mem_total = [part.strip() for part in line.split(",")]
        gpus.append(
            {
                "name": name,
                "gpu_util_pct": float(util),
                "memory_used_mb": float(mem_used),
                "memory_total_mb": float(mem_total),
            }
        )
    return {"gpus": gpus}


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    successes = [item for item in results if item.get("success")]
    failures = [item for item in results if not item.get("success")]

    def values(key: str) -> list[float]:
        return [float(item[key]) for item in successes if item.get(key) is not None]

    return {
        "requests": len(results),
        "successes": len(successes),
        "failures": len(failures),
        "ttft_avg_ms": round(sum(values("ttft_ms")) / len(values("ttft_ms")), 2) if values("ttft_ms") else None,
        "ttft_p95_ms": round(percentile(values("ttft_ms"), 95), 2) if values("ttft_ms") else None,
        "itl_avg_ms": round(sum(values("itl_avg_ms")) / len(values("itl_avg_ms")), 2) if values("itl_avg_ms") else None,
        "itl_p95_ms": round(percentile(values("itl_avg_ms"), 95), 2) if values("itl_avg_ms") else None,
        "total_latency_p50_ms": round(percentile(values("total_latency_ms"), 50), 2)
        if values("total_latency_ms")
        else None,
        "total_latency_p95_ms": round(percentile(values("total_latency_ms"), 95), 2)
        if values("total_latency_ms")
        else None,
        "tokens_per_second_sum": round(sum(values("tokens_per_second")), 2) if values("tokens_per_second") else None,
        "failures_detail": failures[:3],
    }


def build_report(
    label: str,
    started_at: str,
    base_url: str,
    model: str,
    concurrency: int,
    config: dict[str, Any],
    results: list[dict[str, Any]],
    before_gpu: dict[str, Any] | None,
    after_gpu: dict[str, Any] | None,
) -> dict[str, Any]:
    return {
        "label": label,
        "started_at": started_at,
        "base_url": base_url,
        "model": model,
        "concurrency": concurrency,
        "config": config,
        "summary": summarize(results),
        "gpu_before": before_gpu,
        "gpu_after": after_gpu,
        "results": results,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a workshop's requests.jsonl against a live OpenAI-compatible server "
        "and write a JSON report for compare.py",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--base-url", default="http://127.0.0.1:8000/v1")
    parser.add_argument("--api-key", default="EMPTY")
    parser.add_argument("--model", required=True)
    parser.add_argument("--requests-file", required=True, help="Path to this workshop's requests.jsonl")
    parser.add_argument("--requests", type=int, default=32, help="Total requests to send (cycles requests-file)")
    parser.add_argument("--concurrency", type=int, default=8)
    parser.add_argument("--label", required=True, help='e.g. "baseline" or "optimized"')
    parser.add_argument("--config-note", default="", help="Free-text note describing the config under test")
    parser.add_argument("--timeout", type=float, default=300.0)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--output", required=True)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.requests <= 0 or args.concurrency <= 0:
        raise SystemExit("--requests and --concurrency must be > 0")

    plan = load_request_plan(args.requests_file, count=args.requests)
    before_gpu = gpu_snapshot()
    started_at = time.strftime("%Y-%m-%dT%H:%M:%S%z")

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as executor:
        futures = [
            executor.submit(
                request_once,
                args.base_url,
                args.api_key,
                args.model,
                item["prompt"],
                item["max_tokens"],
                args.temperature,
                args.timeout,
            )
            for item in plan
        ]
        results = [future.result() for future in futures]
    after_gpu = gpu_snapshot()

    report = build_report(
        label=args.label,
        started_at=started_at,
        base_url=args.base_url,
        model=args.model,
        concurrency=args.concurrency,
        config={"note": args.config_note, "requests_file": args.requests_file},
        results=results,
        before_gpu=before_gpu,
        after_gpu=after_gpu,
    )
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))

    if report["summary"]["failures"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
