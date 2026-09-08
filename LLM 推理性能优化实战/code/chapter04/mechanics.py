#!/usr/bin/env python3
"""Build a synthetic, inspectable report of Transformer inference mechanics."""

from __future__ import annotations

import argparse
import json
import math
import random
from typing import Any


class ModelConfig:
    def __init__(
        self,
        hidden_size: int,
        num_layers: int,
        num_attention_heads: int,
        num_kv_heads: int,
        head_dim: int,
        intermediate_size: int,
        vocab_size: int,
    ) -> None:
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.num_attention_heads = num_attention_heads
        self.num_kv_heads = num_kv_heads
        self.head_dim = head_dim
        self.intermediate_size = intermediate_size
        self.vocab_size = vocab_size

    def as_dict(self) -> dict[str, int]:
        return {
            "hidden_size": self.hidden_size,
            "num_layers": self.num_layers,
            "num_attention_heads": self.num_attention_heads,
            "num_kv_heads": self.num_kv_heads,
            "head_dim": self.head_dim,
            "intermediate_size": self.intermediate_size,
            "vocab_size": self.vocab_size,
        }


DEFAULT_CONFIG = ModelConfig(
    hidden_size=896,
    num_layers=24,
    num_attention_heads=14,
    num_kv_heads=2,
    head_dim=64,
    intermediate_size=4864,
    vocab_size=151936,
)


def validate_config(config: ModelConfig) -> None:
    values = config.as_dict()
    if any(value <= 0 for value in values.values()):
        raise ValueError("all model dimensions must be positive")
    if config.num_attention_heads % config.num_kv_heads != 0:
        raise ValueError("num_attention_heads must be divisible by num_kv_heads")
    if config.hidden_size != config.num_attention_heads * config.head_dim:
        raise ValueError("hidden_size must equal num_attention_heads * head_dim")


def stage_shapes(
    config: ModelConfig, batch_size: int, sequence_length: int
) -> dict[str, list[int]]:
    validate_config(config)
    if batch_size <= 0:
        raise ValueError("batch_size must be positive")
    if sequence_length <= 0:
        raise ValueError("sequence_length must be positive")
    return {
        "token_ids": [batch_size, sequence_length],
        "hidden_states": [batch_size, sequence_length, config.hidden_size],
        "query": [
            batch_size,
            config.num_attention_heads,
            sequence_length,
            config.head_dim,
        ],
        "key": [
            batch_size,
            config.num_kv_heads,
            sequence_length,
            config.head_dim,
        ],
        "value": [
            batch_size,
            config.num_kv_heads,
            sequence_length,
            config.head_dim,
        ],
        "attention_output": [batch_size, sequence_length, config.hidden_size],
        "mlp_intermediate": [
            batch_size,
            sequence_length,
            config.intermediate_size,
        ],
        "logits": [batch_size, sequence_length, config.vocab_size],
    }


def softmax(logits: list[float], temperature: float = 1.0) -> list[float]:
    if not logits:
        raise ValueError("logits must be non-empty")
    if temperature <= 0:
        raise ValueError("temperature must be greater than zero")
    scaled = [value / temperature for value in logits]
    pivot = max(scaled)
    weights = [math.exp(value - pivot) for value in scaled]
    total = sum(weights)
    return [value / total for value in weights]


def top_k_probabilities(
    logits: list[float], temperature: float = 1.0, top_k: int = 0
) -> list[float]:
    if top_k <= 0 or top_k > len(logits):
        raise ValueError("top_k must be between 1 and the vocabulary size")
    candidate_ids = set(
        sorted(range(len(logits)), key=lambda index: logits[index], reverse=True)[:top_k]
    )
    masked_logits = [
        value if index in candidate_ids else float("-inf")
        for index, value in enumerate(logits)
    ]
    return softmax(masked_logits, temperature=temperature)


def sample_from_logits(
    logits: list[float], temperature: float, top_k: int, seed: int
) -> dict[str, Any]:
    probabilities = top_k_probabilities(
        logits, temperature=temperature, top_k=top_k
    )
    draw = random.Random(seed).random()
    cumulative = 0.0
    selected = len(probabilities) - 1
    for token_id, probability in enumerate(probabilities):
        cumulative += probability
        if draw <= cumulative:
            selected = token_id
            break
    return {
        "temperature": temperature,
        "top_k": top_k,
        "seed": seed,
        "selected_token_id": selected,
        "probabilities": probabilities,
    }


def build_execution_trace(
    prompt_tokens: int, decode_steps: int
) -> list[dict[str, int | str]]:
    if prompt_tokens <= 0:
        raise ValueError("prompt_tokens must be positive")
    if decode_steps < 0:
        raise ValueError("decode_steps must be non-negative")

    trace: list[dict[str, int | str]] = [
        {
            "phase": "prefill",
            "step": 0,
            "input_tokens": prompt_tokens,
            "cache_before": 0,
            "cache_after": prompt_tokens,
            "output_token_index": 1,
        }
    ]
    cache_length = prompt_tokens
    for step in range(1, decode_steps + 1):
        trace.append(
            {
                "phase": "decode",
                "step": step,
                "input_tokens": 1,
                "cache_before": cache_length,
                "cache_after": cache_length + 1,
                "output_token_index": step + 1,
            }
        )
        cache_length += 1
    return trace


def build_report(
    config: ModelConfig,
    prompt_tokens: int,
    decode_steps: int,
    logits: list[float],
    temperature: float,
    top_k: int,
    seed: int,
) -> dict[str, Any]:
    return {
        "mode": "synthetic_mechanics",
        "note": "结构与事件演示，不是性能 Benchmark，也没有运行真实模型。",
        "config": config.as_dict(),
        "shapes": stage_shapes(config, batch_size=1, sequence_length=prompt_tokens),
        "sampling": sample_from_logits(
            logits, temperature=temperature, top_k=top_k, seed=seed
        ),
        "execution_trace": build_execution_trace(
            prompt_tokens=prompt_tokens, decode_steps=decode_steps
        ),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt-tokens", type=int, default=8)
    parser.add_argument("--decode-steps", type=int, default=4)
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument(
        "--logits",
        type=float,
        nargs="+",
        default=[0.1, 1.4, 0.2, 0.8, -0.3],
    )
    parser.add_argument("--output")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    report = build_report(
        config=DEFAULT_CONFIG,
        prompt_tokens=args.prompt_tokens,
        decode_steps=args.decode_steps,
        logits=args.logits,
        temperature=args.temperature,
        top_k=args.top_k,
        seed=args.seed,
    )
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    print(rendered)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(rendered + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
