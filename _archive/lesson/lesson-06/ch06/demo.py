"""Chapter 06: FlashAttention demo.

This script uses deterministic synthetic data so it can run on any laptop.
Replace `simulate_run` with real benchmark/profiling collection on GX10.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass


@dataclass
class Metrics:
    ttft_ms: float
    itl_ms: float
    tokens_per_second: float
    gpu_util_pct: float
    memory_gb: float


def simulate_run(prompt_tokens: int, output_tokens: int, batch_size: int, concurrency: int) -> Metrics:
    prefill_cost = 0.018 * prompt_tokens * math.log2(max(prompt_tokens, 2))
    decode_cost = 4.5 + 0.015 * output_tokens + 0.35 * concurrency
    batching_gain = min(math.log2(batch_size + 1) * 0.18, 0.55)
    ttft_ms = prefill_cost * (1.0 - batching_gain / 2) + 45
    itl_ms = decode_cost * (1.0 - batching_gain)
    tps = 1000.0 / max(itl_ms, 0.1) * batch_size
    memory_gb = 8.0 + prompt_tokens * batch_size * 0.0009 + output_tokens * concurrency * 0.00035
    gpu_util = min(35 + batch_size * 4 + concurrency * 2 + prompt_tokens / 512, 98)
    return Metrics(round(ttft_ms, 2), round(itl_ms, 2), round(tps, 2), round(gpu_util, 2), round(memory_gb, 2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Synthetic benchmark for chapter 06: FlashAttention")
    parser.add_argument("--prompt-tokens", type=int, default=1024)
    parser.add_argument("--output-tokens", type=int, default=256)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--concurrency", type=int, default=8)
    args = parser.parse_args()
    metrics = simulate_run(args.prompt_tokens, args.output_tokens, args.batch_size, args.concurrency)
    print(json.dumps(asdict(metrics), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
