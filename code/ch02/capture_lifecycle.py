#!/usr/bin/env python3
"""Capture real client and vLLM lifecycle evidence for one streaming request."""

from __future__ import annotations

import argparse
import json
import math
import platform
import re
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Iterable


DEFAULT_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
DEFAULT_PROMPT = "请用三句话解释一次 LLM 请求为什么会经过 Queue、Prefill 和 Decode。"

PROMETHEUS_METRICS = {
    "vllm:request_queue_time_seconds_sum",
    "vllm:request_queue_time_seconds_count",
    "vllm:request_prefill_time_seconds_sum",
    "vllm:request_prefill_time_seconds_count",
    "vllm:request_decode_time_seconds_sum",
    "vllm:request_decode_time_seconds_count",
    "vllm:e2e_request_latency_seconds_sum",
    "vllm:e2e_request_latency_seconds_count",
    "vllm:time_to_first_token_seconds_sum",
    "vllm:time_to_first_token_seconds_count",
    "vllm:request_success_total",
}

REQUIRED_SERVER_METRICS = (
    "queue_time_ms",
    "time_to_first_token_ms",
    "generation_time_ms",
)


def server_metrics_complete(metrics: dict[str, float | None] | None) -> bool:
    if not isinstance(metrics, dict):
        return False
    return all(
        isinstance(metrics.get(name), (int, float))
        and math.isfinite(float(metrics[name]))
        and float(metrics[name]) >= 0
        for name in REQUIRED_SERVER_METRICS
    )


REQUIRED_ENVIRONMENT_FIELDS = (
    "python_version",
    "vllm_version",
    "gpu",
    "model",
    "model_revision",
    "server_command",
)


def environment_complete(environment: dict[str, str] | None) -> bool:
    return isinstance(environment, dict) and all(
        isinstance(environment.get(name), str) and bool(environment[name].strip())
        for name in REQUIRED_ENVIRONMENT_FIELDS
    )


def _command_output(command: list[str]) -> str:
    try:
        result = subprocess.run(
            command,
            text=True,
            capture_output=True,
            check=False,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return result.stdout.strip() if result.returncode == 0 else ""


def collect_environment(
    *, model: str, model_revision: str, server_command: str
) -> dict[str, str]:
    return {
        "python_version": platform.python_version(),
        "vllm_version": _command_output(["vllm", "--version"]),
        "gpu": _command_output(
            ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"]
        ),
        "model": model,
        "model_revision": model_revision,
        "server_command": server_command,
    }


def build_payload(model: str, prompt: str, max_tokens: int, temperature: float) -> dict[str, Any]:
    return {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "n": 1,
        "stream": True,
        "stream_options": {"include_usage": True},
    }


def parse_sse_line(raw_line: bytes) -> dict[str, Any] | None:
    line = raw_line.decode("utf-8").strip()
    if not line or not line.startswith("data:"):
        return None
    value = line[len("data:") :].strip()
    if value == "[DONE]":
        return {"done": True}
    parsed = json.loads(value)
    if not isinstance(parsed, dict):
        raise ValueError("SSE data must be a JSON object")
    return parsed


def _delta_text(payload: dict[str, Any]) -> str:
    choices = payload.get("choices") or []
    if not choices:
        return ""
    delta = choices[0].get("delta") or {}
    content = delta.get("content")
    return content if isinstance(content, str) else ""


class LifecycleCollector:
    """Collect observations without inventing unavailable server timestamps."""

    def __init__(self, start_ms: float):
        self.start_ms = start_ms
        self.headers_ms: float | None = None
        self.first_content_ms: float | None = None
        self.last_content_ms: float | None = None
        self.request_id: str | None = None
        self.content_chunks = 0
        self.output_characters = 0
        self.usage: dict[str, Any] | None = None
        self.server_metrics: dict[str, float | None] | None = None

    def on_response_open(self, timestamp_ms: float) -> None:
        self.headers_ms = timestamp_ms

    def on_payload(self, payload: dict[str, Any], timestamp_ms: float) -> None:
        request_id = payload.get("id")
        if isinstance(request_id, str):
            if self.request_id is not None and request_id != self.request_id:
                raise ValueError("stream changed request id")
            self.request_id = request_id

        text = _delta_text(payload)
        if text:
            if self.first_content_ms is None:
                self.first_content_ms = timestamp_ms
            self.last_content_ms = timestamp_ms
            self.content_chunks += 1
            self.output_characters += len(text)

        usage = payload.get("usage")
        if isinstance(usage, dict):
            self.usage = usage

        metrics = payload.get("metrics")
        if isinstance(metrics, dict):
            fields = (
                "queue_time_ms",
                "time_to_first_token_ms",
                "generation_time_ms",
                "mean_itl_ms",
                "tokens_per_second",
            )
            self.server_metrics = {
                name: float(metrics[name]) if isinstance(metrics.get(name), (int, float)) else None
                for name in fields
            }

    def finish(
        self,
        done_ms: float,
        prometheus_delta: dict[str, float] | None = None,
        environment: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        relative = lambda value: round(value - self.start_ms, 3) if value is not None else None
        server = self.server_metrics
        queue = server.get("queue_time_ms") if server else None
        first_token = server.get("time_to_first_token_ms") if server else None
        decode = server.get("generation_time_ms") if server else None

        metrics_complete = server_metrics_complete(server)
        evidence_complete = bool(
            metrics_complete
            and self.request_id
            and isinstance(self.usage, dict)
            and environment_complete(environment)
        )
        warnings: list[str] = []
        if not metrics_complete:
            warnings.append(
                "required per-request server metrics are incomplete; start vLLM with --enable-per-request-metrics"
            )
        if prometheus_delta is not None:
            warnings.append(
                "Prometheus delta is direct server-aggregate evidence; concurrent traffic prevents per-request attribution"
            )

        return {
            "mode": "real_vllm_lifecycle_evidence",
            "request_id": self.request_id,
            "environment": environment,
            "acceptance": {
                "status": "complete" if evidence_complete else "incomplete",
                "evidence_complete": evidence_complete,
                "server_metrics_complete": metrics_complete,
                "required_server_metrics": list(REQUIRED_SERVER_METRICS),
                "required_environment_fields": list(REQUIRED_ENVIRONMENT_FIELDS),
            },
            "direct_observations": {
                "client_events_ms": {
                    "request_sent": 0.0,
                    "response_headers_received": relative(self.headers_ms),
                    "first_content_chunk_received": relative(self.first_content_ms),
                    "last_content_chunk_received": relative(self.last_content_ms),
                    "stream_done": relative(done_ms),
                },
                "stream": {
                    "content_chunks": self.content_chunks,
                    "output_characters": self.output_characters,
                },
                "usage": self.usage,
                "server_per_request_metrics_ms": server,
                "server_prometheus_delta": (
                    {"scope": "server_aggregate", "values": prometheus_delta}
                    if prometheus_delta is not None
                    else None
                ),
            },
            "derived_client_durations_ms": {
                "time_to_response_headers": relative(self.headers_ms),
                "time_to_first_content_chunk": relative(self.first_content_ms),
                "stream_end_to_end": relative(done_ms),
            },
            "phase_evidence": {
                "request_received": {
                    "evidence": "inferred",
                    "reason": "the OpenAI-compatible response does not expose the server receipt timestamp",
                },
                "queue": {
                    "evidence": "direct_duration" if queue is not None else "unavailable",
                    "duration_ms": queue,
                },
                "scheduled_to_first_token": {
                    "evidence": "direct_duration" if first_token is not None else "unavailable",
                    "duration_ms": first_token,
                    "note": "do not rename this value to pure Prefill unless the server metric contract says so",
                },
                "decode": {
                    "evidence": "direct_duration" if decode is not None else "unavailable",
                    "duration_ms": decode,
                },
                "response_stream": {
                    "evidence": "direct_client_boundary",
                    "first_content_chunk_received_ms": relative(self.first_content_ms),
                    "stream_done_ms": relative(done_ms),
                },
            },
            "warnings": warnings,
        }


def parse_prometheus_totals(text: str) -> dict[str, float]:
    totals: dict[str, float] = {}
    pattern = re.compile(r"^([A-Za-z_:][A-Za-z0-9_:]*)(?:\{[^}]*\})?\s+([^\s]+)(?:\s+\d+)?$")
    for line in text.splitlines():
        if not line or line.startswith("#"):
            continue
        match = pattern.match(line.strip())
        if not match or match.group(1) not in PROMETHEUS_METRICS:
            continue
        try:
            value = float(match.group(2))
        except ValueError:
            continue
        if math.isfinite(value):
            totals[match.group(1)] = totals.get(match.group(1), 0.0) + value
    return totals


def metric_deltas(before: dict[str, float], after: dict[str, float]) -> dict[str, float]:
    return {
        name: after[name] - before[name]
        for name in sorted(before.keys() & after.keys())
        if after[name] >= before[name]
    }


def _metrics_url(base_url: str) -> str:
    value = base_url.rstrip("/")
    if value.endswith("/v1"):
        value = value[:-3]
    return value + "/metrics"


def fetch_prometheus(base_url: str, timeout: float) -> dict[str, float] | None:
    try:
        with urllib.request.urlopen(_metrics_url(base_url), timeout=timeout) as response:
            return parse_prometheus_totals(response.read().decode("utf-8", errors="replace"))
    except Exception:
        return None


def capture_request(
    *,
    base_url: str,
    api_key: str,
    model: str,
    prompt: str,
    max_tokens: int,
    temperature: float,
    timeout: float,
    model_revision: str,
    server_command: str,
) -> dict[str, Any]:
    before = fetch_prometheus(base_url, timeout=min(timeout, 5.0))
    payload = build_payload(model, prompt, max_tokens, temperature)
    request = urllib.request.Request(
        base_url.rstrip("/") + "/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    start_ms = time.perf_counter() * 1000.0
    collector = LifecycleCollector(start_ms)
    done_seen = False
    with urllib.request.urlopen(request, timeout=timeout) as response:
        collector.on_response_open(time.perf_counter() * 1000.0)
        for raw_line in response:
            parsed = parse_sse_line(raw_line)
            if parsed is None:
                continue
            if parsed.get("done"):
                done_seen = True
                break
            if "error" in parsed:
                raise RuntimeError(f"vLLM SSE error: {parsed['error']}")
            collector.on_payload(parsed, time.perf_counter() * 1000.0)
    if not done_seen:
        raise RuntimeError("stream ended without [DONE]")
    done_ms = time.perf_counter() * 1000.0
    after = fetch_prometheus(base_url, timeout=min(timeout, 5.0))
    delta = metric_deltas(before, after) if before is not None and after is not None else None
    return collector.finish(
        done_ms,
        prometheus_delta=delta,
        environment=collect_environment(
            model=model,
            model_revision=model_revision,
            server_command=server_command,
        ),
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:8000/v1")
    parser.add_argument("--api-key", default="EMPTY")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--prompt", default=DEFAULT_PROMPT)
    parser.add_argument("--max-tokens", type=int, default=128)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--timeout", type=float, default=120.0)
    parser.add_argument("--model-revision", required=True)
    parser.add_argument("--server-command", required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--require-server-metrics", action="store_true")
    parser.add_argument("--require-complete-evidence", action="store_true")
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        report = capture_request(
            base_url=args.base_url,
            api_key=args.api_key,
            model=args.model,
            prompt=args.prompt,
            max_tokens=args.max_tokens,
            temperature=args.temperature,
            timeout=args.timeout,
            model_revision=args.model_revision,
            server_command=args.server_command,
        )
    except (urllib.error.URLError, urllib.error.HTTPError, RuntimeError, ValueError) as exc:
        print(json.dumps({"success": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        return 1

    output = json.dumps(report, ensure_ascii=False, indent=2)
    print(output)
    if args.output:
        args.output.write_text(output + "\n", encoding="utf-8")
    if args.require_server_metrics and not report["acceptance"]["server_metrics_complete"]:
        return 2
    if args.require_complete_evidence and not report["acceptance"]["evidence_complete"]:
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
