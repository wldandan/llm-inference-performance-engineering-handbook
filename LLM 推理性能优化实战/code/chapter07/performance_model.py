#!/usr/bin/env python3
"""Analyze a synthetic LLM, RAG, or Agent latency dependency graph."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


EVIDENCE_MAP = {
    "network": (
        "network_or_serialization_delay",
        ["client_server_timestamps", "payload_bytes", "network_trace"],
    ),
    "queue": (
        "scheduling_or_capacity_pressure",
        ["queue_wait_ms", "waiting_requests", "admission_reason", "kv_cache_capacity"],
    ),
    "preprocess": (
        "cpu_preprocessing_or_tokenization",
        ["tokenization_ms", "cpu_profile", "prompt_tokens"],
    ),
    "prefill": (
        "prefill_compute_or_bandwidth_pressure",
        ["prompt_tokens", "prefill_ms", "gpu_compute_throughput", "hbm_bandwidth"],
    ),
    "decode": (
        "decode_bandwidth_launch_or_scheduling_pressure",
        ["output_tokens", "tpot_ms", "hbm_bandwidth", "kernel_timeline"],
    ),
    "retrieval": (
        "retrieval_service_or_index_delay",
        ["retrieval_latency_ms", "vector_db_trace", "result_count"],
    ),
    "rerank": (
        "reranker_compute_or_queue_delay",
        ["rerank_latency_ms", "candidate_count", "reranker_trace"],
    ),
    "tool": (
        "external_tool_or_dependency_delay",
        ["tool_latency_ms", "dependency_trace", "timeout_and_retry_count"],
    ),
    "orchestration": (
        "orchestration_dependency_or_serialization_delay",
        ["task_trace", "dependency_graph", "parallelism", "retry_count"],
    ),
    "other": (
        "unclassified_stage_delay",
        ["stage_trace", "stage_inputs", "stage_outputs"],
    ),
}


def _validate_nodes(nodes: list[dict]) -> dict[str, dict]:
    if not isinstance(nodes, list) or not nodes:
        raise ValueError("nodes must be a non-empty list")
    by_id: dict[str, dict] = {}
    for item in nodes:
        if not isinstance(item, dict):
            raise ValueError("every node must be an object")
        node_id = item.get("id")
        if not isinstance(node_id, str) or not node_id:
            raise ValueError("node id must be a non-empty string")
        if node_id in by_id:
            raise ValueError(f"duplicate node id: {node_id}")
        duration = item.get("duration_ms")
        if not isinstance(duration, (int, float)) or isinstance(duration, bool) or duration < 0:
            raise ValueError(f"duration_ms must be non-negative for {node_id}")
        dependencies = item.get("depends_on", [])
        if not isinstance(dependencies, list) or any(
            not isinstance(dependency, str) or not dependency for dependency in dependencies
        ):
            raise ValueError(f"depends_on must be a list of node ids for {node_id}")
        category = item.get("category", "other")
        if not isinstance(category, str) or not category:
            raise ValueError(f"category must be a string for {node_id}")
        by_id[node_id] = {
            "id": node_id,
            "duration_ms": duration,
            "depends_on": dependencies,
            "category": category,
        }

    for item in by_id.values():
        for dependency in item["depends_on"]:
            if dependency not in by_id:
                raise ValueError(
                    f"unknown dependency {dependency} referenced by {item['id']}"
                )
    return by_id


def analyze_critical_path(nodes: list[dict]) -> dict[str, object]:
    by_id = _validate_nodes(nodes)
    state: dict[str, str] = {}
    finish: dict[str, float] = {}
    predecessor: dict[str, str | None] = {}

    def visit(node_id: str) -> float:
        if state.get(node_id) == "visiting":
            raise ValueError(f"cycle detected at {node_id}")
        if state.get(node_id) == "done":
            return finish[node_id]
        state[node_id] = "visiting"
        item = by_id[node_id]
        best_dependency = None
        best_finish = 0.0
        for dependency in item["depends_on"]:
            dependency_finish = visit(dependency)
            if best_dependency is None or dependency_finish > best_finish:
                best_dependency = dependency
                best_finish = dependency_finish
        finish[node_id] = best_finish + item["duration_ms"]
        predecessor[node_id] = best_dependency
        state[node_id] = "done"
        return finish[node_id]

    for node_id in by_id:
        visit(node_id)

    end_id = max(by_id, key=lambda node_id: finish[node_id])
    path = []
    current: str | None = end_id
    while current is not None:
        path.append(current)
        current = predecessor[current]
    path.reverse()
    path_set = set(path)
    critical_path_ms = finish[end_id]
    all_node_time_ms = sum(item["duration_ms"] for item in by_id.values())

    return {
        "critical_path_ms": critical_path_ms,
        "critical_path": path,
        "all_node_time_ms": all_node_time_ms,
        "parallel_overlap_ms": all_node_time_ms - critical_path_ms,
        "stages": [
            {
                **item,
                "earliest_finish_ms": finish[item["id"]],
                "on_critical_path": item["id"] in path_set,
                "critical_path_share": (
                    item["duration_ms"] / critical_path_ms if item["id"] in path_set else 0
                ),
            }
            for item in by_id.values()
        ],
    }


def rank_hypotheses(nodes: list[dict]) -> list[dict[str, object]]:
    analysis = analyze_critical_path(nodes)
    critical = [item for item in analysis["stages"] if item["on_critical_path"]]
    critical.sort(key=lambda item: item["duration_ms"], reverse=True)
    ranked = []
    for item in critical:
        hypothesis, evidence = EVIDENCE_MAP.get(item["category"], EVIDENCE_MAP["other"])
        ranked.append(
            {
                "stage_id": item["id"],
                "category": item["category"],
                "duration_ms": item["duration_ms"],
                "critical_path_share": item["critical_path_share"],
                "hypothesis": hypothesis,
                "evidence_needed": evidence,
                "status": "needs_evidence",
            }
        )
    return ranked


def build_report(scenario: dict) -> dict[str, object]:
    if not isinstance(scenario, dict):
        raise ValueError("scenario must be an object")
    name = scenario.get("name")
    kind = scenario.get("kind")
    if not isinstance(name, str) or not name:
        raise ValueError("scenario name must be a non-empty string")
    if kind not in {"llm_request", "rag", "agent"}:
        raise ValueError("scenario kind must be llm_request, rag, or agent")
    nodes = scenario.get("nodes")
    analysis = analyze_critical_path(nodes)
    return {
        "mode": "synthetic_global_performance_model",
        "note": "关键路径和候选假设来自输入数据，不是 Benchmark，也不是 Root Cause；每项仍需真实证据验证。",
        "scenario": {"name": name, "kind": kind},
        "analysis": analysis,
        "hypotheses": rank_hypotheses(nodes),
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "scenario",
        type=Path,
        nargs="?",
        default=Path(__file__).with_name("sample_agent.json"),
    )
    parser.add_argument("--output", type=Path)
    return parser


def main() -> int:
    args = _parser().parse_args()
    scenario = json.loads(args.scenario.read_text(encoding="utf-8"))
    report = build_report(scenario)
    output = json.dumps(report, ensure_ascii=False, indent=2)
    print(output)
    if args.output:
        args.output.write_text(output + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
