"""Validate the logical request and response paths of an LLM serving architecture."""

from __future__ import annotations

import argparse
import json
from collections import OrderedDict, defaultdict
from pathlib import Path
from typing import Any


REQUEST_ROLES_BY_PROFILE = {
    "single_instance": ["client", "gateway", "scheduler", "worker", "runtime", "accelerator"],
    "scale_out": [
        "client",
        "gateway",
        "router",
        "admission",
        "scheduler",
        "worker",
        "runtime",
        "accelerator",
    ],
}
RESPONSE_ROLES = ["accelerator", "runtime", "worker", "gateway", "client"]
ALLOWED_FLOW_KINDS = {"request", "response", "control", "telemetry"}
ROLE_CONTRACTS = {
    "client": ["request_creation", "user_observation"],
    "gateway": ["protocol_boundary", "authentication", "response_streaming"],
    "router": ["target_selection"],
    "admission": ["accept_reject", "global_queue"],
    "scheduler": ["iteration_plan", "token_budget", "kv_budget"],
    "worker": ["model_state", "execute_plan"],
    "runtime": ["operator_dispatch", "kernel_launch"],
    "accelerator": ["tensor_compute", "device_memory"],
}


def _find_role_path(
    components: dict[str, dict[str, Any]], flows: list[dict[str, Any]], kind: str, roles: list[str]
) -> list[str] | None:
    edges: dict[str, list[str]] = defaultdict(list)
    for flow in flows:
        if flow.get("kind") == kind:
            edges[flow["from"]].append(flow["to"])

    def walk(component_id: str, role_index: int) -> list[str] | None:
        if role_index == len(roles) - 1:
            return [component_id]
        next_role = roles[role_index + 1]
        for target in edges.get(component_id, []):
            if components[target].get("role") != next_role:
                continue
            suffix = walk(target, role_index + 1)
            if suffix:
                return [component_id, *suffix]
        return None

    for component_id, component in components.items():
        if component.get("role") == roles[0]:
            path = walk(component_id, 0)
            if path:
                return path
    return None


def validate_architecture(spec: dict[str, Any]) -> dict[str, Any]:
    profile = spec.get("profile", "scale_out")
    if profile not in REQUEST_ROLES_BY_PROFILE:
        raise ValueError(f"unsupported architecture profile: {profile}")
    request_roles = REQUEST_ROLES_BY_PROFILE[profile]
    components: dict[str, dict[str, Any]] = {}
    for item in spec["components"]:
        component_id = item["id"]
        if component_id in components:
            raise ValueError(f"duplicate component id: {component_id}")
        components[component_id] = item

    present_roles = {item.get("role") for item in components.values()}
    missing_roles = [role for role in request_roles if role not in present_roles]
    if missing_roles:
        raise ValueError(f"missing roles: {', '.join(missing_roles)}")

    flows = spec["flows"]
    for flow in flows:
        kind = flow.get("kind")
        if kind not in ALLOWED_FLOW_KINDS:
            raise ValueError(f"unsupported flow kind: {kind}")
        for endpoint in (flow.get("from"), flow.get("to")):
            if endpoint not in components:
                raise ValueError(f"unknown component: {endpoint}")

    request_path = _find_role_path(components, flows, "request", request_roles)
    if request_path is None:
        raise ValueError("architecture has no complete request path")
    response_path = _find_role_path(components, flows, "response", RESPONSE_ROLES)
    if response_path is None:
        raise ValueError("architecture has no complete response path")

    deployment_units: OrderedDict[str, list[str]] = OrderedDict()
    for component in spec["components"]:
        deployment_units.setdefault(component["deployment_unit"], []).append(component["id"])

    return {
        "profile": profile,
        "request_path": request_path,
        "response_path": response_path,
        "deployment_units": deployment_units,
        "role_contracts": ROLE_CONTRACTS,
        "optional_roles_absent": [
            role for role in ("router", "admission") if role not in present_roles
        ],
    }


def load_spec(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON: {exc.msg}") from exc


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate an LLM serving architecture contract")
    parser.add_argument("--input", type=Path, required=True, help="Architecture JSON file")
    parser.add_argument("--output", type=Path, default=None, help="Optional JSON report path")
    args = parser.parse_args()

    report_text = json.dumps(validate_architecture(load_spec(args.input)), ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(report_text + "\n", encoding="utf-8")
    print(report_text)


if __name__ == "__main__":
    main()
