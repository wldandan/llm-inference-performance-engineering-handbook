#!/usr/bin/env python3
"""Build a synthetic GPU constraint report without loading a model or GPU."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def _positive(name: str, value: float) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be positive")


def model_weight_bytes(model_parameters: int, bytes_per_parameter: float) -> float:
    _positive("model_parameters", model_parameters)
    _positive("bytes_per_parameter", bytes_per_parameter)
    return model_parameters * bytes_per_parameter


def kv_cache_bytes(
    num_layers: int,
    num_kv_heads: int,
    head_dim: int,
    total_tokens: int,
    bytes_per_element: float,
) -> float:
    for name, value in [
        ("num_layers", num_layers),
        ("num_kv_heads", num_kv_heads),
        ("head_dim", head_dim),
        ("total_tokens", total_tokens),
        ("bytes_per_element", bytes_per_element),
    ]:
        _positive(name, value)
    return 2 * num_layers * num_kv_heads * head_dim * total_tokens * bytes_per_element


def memory_budget(
    model_bytes: float,
    kv_bytes: float,
    workspace_bytes: float,
    gpu_memory_bytes: float,
    reserve_fraction: float,
) -> dict[str, float | bool]:
    for name, value in [
        ("model_bytes", model_bytes),
        ("kv_bytes", kv_bytes),
        ("workspace_bytes", workspace_bytes),
        ("gpu_memory_bytes", gpu_memory_bytes),
    ]:
        if value < 0:
            raise ValueError(f"{name} cannot be negative")
    _positive("gpu_memory_bytes", gpu_memory_bytes)
    if not 0 <= reserve_fraction < 1:
        raise ValueError("reserve_fraction must be in [0, 1)")

    usable_bytes = gpu_memory_bytes * (1 - reserve_fraction)
    required_bytes = model_bytes + kv_bytes + workspace_bytes
    remaining_bytes = usable_bytes - required_bytes
    return {
        "gpu_memory_bytes": gpu_memory_bytes,
        "reserve_bytes": gpu_memory_bytes * reserve_fraction,
        "usable_bytes": usable_bytes,
        "model_bytes": model_bytes,
        "kv_bytes": kv_bytes,
        "workspace_bytes": workspace_bytes,
        "required_bytes": required_bytes,
        "remaining_bytes": remaining_bytes,
        "fits": remaining_bytes >= 0,
    }


def execution_lower_bounds(
    operations_flop: float,
    bytes_moved: float,
    peak_tflops: float,
    memory_bandwidth_gbps: float,
    kernel_count: int,
    launch_us: float,
) -> dict[str, float | str]:
    for name, value in [
        ("operations_flop", operations_flop),
        ("bytes_moved", bytes_moved),
        ("peak_tflops", peak_tflops),
        ("memory_bandwidth_gbps", memory_bandwidth_gbps),
        ("kernel_count", kernel_count),
        ("launch_us", launch_us),
    ]:
        _positive(name, value)

    compute_ms = operations_flop / (peak_tflops * 1e12) * 1000
    bandwidth_ms = bytes_moved / (memory_bandwidth_gbps * 1e9) * 1000
    launch_ms = kernel_count * launch_us / 1000
    candidates = {
        "compute_throughput": compute_ms,
        "memory_bandwidth": bandwidth_ms,
        "launch_overhead": launch_ms,
    }
    dominant_constraint = max(candidates, key=candidates.get)
    return {
        "compute_ms": compute_ms,
        "bandwidth_ms": bandwidth_ms,
        "launch_ms": launch_ms,
        "execution_floor_ms": max(compute_ms, bandwidth_ms) + launch_ms,
        "arithmetic_intensity_flop_per_byte": operations_flop / bytes_moved,
        "ridge_point_flop_per_byte": peak_tflops * 1e12 / (memory_bandwidth_gbps * 1e9),
        "dominant_constraint": dominant_constraint,
    }


def build_report(
    *,
    model_parameters: int,
    bytes_per_parameter: float,
    num_layers: int,
    num_kv_heads: int,
    head_dim: int,
    active_tokens: int,
    kv_bytes_per_element: float,
    workspace_bytes: float,
    gpu_memory_bytes: float,
    reserve_fraction: float,
    operations_flop: float,
    bytes_moved: float,
    peak_tflops: float,
    memory_bandwidth_gbps: float,
    kernel_count: int,
    launch_us: float,
) -> dict[str, object]:
    weights = model_weight_bytes(model_parameters, bytes_per_parameter)
    kv = kv_cache_bytes(
        num_layers,
        num_kv_heads,
        head_dim,
        active_tokens,
        kv_bytes_per_element,
    )
    capacity = memory_budget(
        weights,
        kv,
        workspace_bytes,
        gpu_memory_bytes,
        reserve_fraction,
    )
    execution = execution_lower_bounds(
        operations_flop,
        bytes_moved,
        peak_tflops,
        memory_bandwidth_gbps,
        kernel_count,
        launch_us,
    )
    dominant = (
        "memory_capacity" if not capacity["fits"] else execution["dominant_constraint"]
    )
    constraints = {
        "compute_throughput": {
            "question": "完成这些运算至少需要多久？",
            "lower_bound_ms": execution["compute_ms"],
        },
        "memory_capacity": {
            "question": "权重、KV Cache 和工作区能否同时放下？",
            "fits": capacity["fits"],
            "remaining_bytes": capacity["remaining_bytes"],
        },
        "memory_bandwidth": {
            "question": "搬运这些数据至少需要多久？",
            "lower_bound_ms": execution["bandwidth_ms"],
        },
        "launch_overhead": {
            "question": "提交大量短 Kernel 的固定开销有多大？",
            "lower_bound_ms": execution["launch_ms"],
        },
    }
    return {
        "mode": "synthetic_gpu_mental_model",
        "note": "这是按输入假设计算的理论下界与容量预算，不是 Benchmark，也没有探测真实 GPU。",
        "dominant_constraint": dominant,
        "memory_budget": capacity,
        "execution_lower_bounds": execution,
        "constraints": constraints,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-parameters", type=int, default=500_000_000)
    parser.add_argument("--bytes-per-parameter", type=float, default=2)
    parser.add_argument("--num-layers", type=int, default=24)
    parser.add_argument("--num-kv-heads", type=int, default=2)
    parser.add_argument("--head-dim", type=int, default=64)
    parser.add_argument("--active-tokens", type=int, default=4096)
    parser.add_argument("--kv-bytes-per-element", type=float, default=2)
    parser.add_argument("--workspace-gb", type=float, default=0.2)
    parser.add_argument("--gpu-memory-gb", type=float, default=2)
    parser.add_argument("--reserve-fraction", type=float, default=0.10)
    parser.add_argument("--operations-gflop", type=float, default=1)
    parser.add_argument("--bytes-moved-gb", type=float, default=20)
    parser.add_argument("--peak-tflops", type=float, default=100)
    parser.add_argument("--memory-bandwidth-gbps", type=float, default=2000)
    parser.add_argument("--kernel-count", type=int, default=10)
    parser.add_argument("--launch-us", type=float, default=5)
    parser.add_argument("--output", type=Path)
    return parser


def main() -> int:
    args = _parser().parse_args()
    report = build_report(
        model_parameters=args.model_parameters,
        bytes_per_parameter=args.bytes_per_parameter,
        num_layers=args.num_layers,
        num_kv_heads=args.num_kv_heads,
        head_dim=args.head_dim,
        active_tokens=args.active_tokens,
        kv_bytes_per_element=args.kv_bytes_per_element,
        workspace_bytes=args.workspace_gb * 1e9,
        gpu_memory_bytes=args.gpu_memory_gb * 1e9,
        reserve_fraction=args.reserve_fraction,
        operations_flop=args.operations_gflop * 1e9,
        bytes_moved=args.bytes_moved_gb * 1e9,
        peak_tflops=args.peak_tflops,
        memory_bandwidth_gbps=args.memory_bandwidth_gbps,
        kernel_count=args.kernel_count,
        launch_us=args.launch_us,
    )
    output = json.dumps(report, ensure_ascii=False, indent=2)
    print(output)
    if args.output:
        args.output.write_text(output + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
