import copy
import importlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


def reference_architecture():
    return {
        "name": "single-replica-reference",
        "components": [
            {"id": "client", "role": "client", "deployment_unit": "caller"},
            {"id": "gateway", "role": "gateway", "deployment_unit": "api-process"},
            {"id": "router", "role": "router", "deployment_unit": "api-process"},
            {"id": "admission", "role": "admission", "deployment_unit": "engine-core"},
            {"id": "scheduler", "role": "scheduler", "deployment_unit": "engine-core"},
            {"id": "worker", "role": "worker", "deployment_unit": "worker-0"},
            {"id": "runtime", "role": "runtime", "deployment_unit": "worker-0"},
            {"id": "accelerator", "role": "accelerator", "deployment_unit": "gpu-0"},
        ],
        "flows": [
            {"from": "client", "to": "gateway", "kind": "request"},
            {"from": "gateway", "to": "router", "kind": "request"},
            {"from": "router", "to": "admission", "kind": "request"},
            {"from": "admission", "to": "scheduler", "kind": "request"},
            {"from": "scheduler", "to": "worker", "kind": "request"},
            {"from": "worker", "to": "runtime", "kind": "request"},
            {"from": "runtime", "to": "accelerator", "kind": "request"},
            {"from": "accelerator", "to": "runtime", "kind": "response"},
            {"from": "runtime", "to": "worker", "kind": "response"},
            {"from": "worker", "to": "gateway", "kind": "response"},
            {"from": "gateway", "to": "client", "kind": "response"},
        ],
    }


class ArchitectureContractTest(unittest.TestCase):
    def load_module(self):
        try:
            return importlib.import_module("architecture_contract")
        except ModuleNotFoundError:
            self.fail("architecture_contract module has not been implemented")

    def test_reference_architecture_exposes_request_response_and_deployment_boundaries(self):
        architecture_contract = self.load_module()

        report = architecture_contract.validate_architecture(reference_architecture())

        self.assertEqual(
            report["request_path"],
            ["client", "gateway", "router", "admission", "scheduler", "worker", "runtime", "accelerator"],
        )
        self.assertEqual(
            report["response_path"],
            ["accelerator", "runtime", "worker", "gateway", "client"],
        )
        self.assertEqual(report["deployment_units"]["api-process"], ["gateway", "router"])
        self.assertEqual(report["deployment_units"]["worker-0"], ["worker", "runtime"])

    def test_role_contracts_keep_routing_and_engine_scheduling_separate(self):
        architecture_contract = self.load_module()

        report = architecture_contract.validate_architecture(reference_architecture())

        self.assertIn("role_contracts", report, "role contracts have not been implemented")
        self.assertIn("target_selection", report["role_contracts"]["router"])
        self.assertNotIn("iteration_plan", report["role_contracts"]["router"])
        self.assertIn("iteration_plan", report["role_contracts"]["scheduler"])
        self.assertIn("kv_budget", report["role_contracts"]["scheduler"])

    def test_missing_required_role_is_rejected(self):
        architecture_contract = self.load_module()
        spec = reference_architecture()
        spec["components"] = [item for item in spec["components"] if item["role"] != "router"]
        spec["flows"] = [flow for flow in spec["flows"] if "router" not in {flow["from"], flow["to"]}]

        with self.assertRaisesRegex(ValueError, "missing roles: router"):
            architecture_contract.validate_architecture(spec)

    def test_duplicate_component_id_is_rejected(self):
        architecture_contract = self.load_module()
        spec = reference_architecture()
        spec["components"].append(copy.deepcopy(spec["components"][0]))

        with self.assertRaisesRegex(ValueError, "duplicate component id: client"):
            architecture_contract.validate_architecture(spec)

    def test_flow_with_unknown_component_is_rejected(self):
        architecture_contract = self.load_module()
        spec = reference_architecture()
        spec["flows"].append({"from": "router", "to": "missing-worker", "kind": "request"})

        with self.assertRaisesRegex(ValueError, "unknown component: missing-worker"):
            architecture_contract.validate_architecture(spec)

    def test_unsupported_flow_kind_is_rejected(self):
        architecture_contract = self.load_module()
        spec = reference_architecture()
        spec["flows"][0]["kind"] = "magic"

        with self.assertRaisesRegex(ValueError, "unsupported flow kind: magic"):
            architecture_contract.validate_architecture(spec)

    def test_broken_request_path_is_rejected(self):
        architecture_contract = self.load_module()
        spec = reference_architecture()
        spec["flows"] = [
            flow
            for flow in spec["flows"]
            if not (flow["from"] == "scheduler" and flow["to"] == "worker" and flow["kind"] == "request")
        ]

        with self.assertRaisesRegex(ValueError, "complete request path"):
            architecture_contract.validate_architecture(spec)

    def test_broken_response_path_is_rejected(self):
        architecture_contract = self.load_module()
        spec = reference_architecture()
        spec["flows"] = [
            flow
            for flow in spec["flows"]
            if not (flow["from"] == "worker" and flow["to"] == "gateway" and flow["kind"] == "response")
        ]

        with self.assertRaisesRegex(ValueError, "complete response path"):
            architecture_contract.validate_architecture(spec)

    def test_json_spec_is_loaded(self):
        architecture_contract = self.load_module()
        self.assertTrue(hasattr(architecture_contract, "load_spec"), "load_spec has not been implemented")
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "architecture.json"
            input_path.write_text(json.dumps(reference_architecture()), encoding="utf-8")

            loaded = architecture_contract.load_spec(input_path)

        self.assertEqual(loaded["name"], "single-replica-reference")
        self.assertEqual(len(loaded["components"]), 8)

    def test_invalid_json_spec_is_rejected(self):
        architecture_contract = self.load_module()
        self.assertTrue(hasattr(architecture_contract, "load_spec"), "load_spec has not been implemented")
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "architecture.json"
            input_path.write_text("{not-json}", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "invalid JSON"):
                architecture_contract.load_spec(input_path)

    def test_cli_prints_the_architecture_report(self):
        script = Path(__file__).with_name("architecture_contract.py")
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "architecture.json"
            input_path.write_text(json.dumps(reference_architecture()), encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(script), "--input", str(input_path)],
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotEqual(result.stdout.strip(), "", "CLI has not been implemented")
        self.assertEqual(json.loads(result.stdout)["request_path"][-1], "accelerator")

    def test_cli_can_save_the_architecture_report(self):
        script = Path(__file__).with_name("architecture_contract.py")
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "architecture.json"
            output_path = Path(temp_dir) / "report.json"
            input_path.write_text(json.dumps(reference_architecture()), encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--input",
                    str(input_path),
                    "--output",
                    str(output_path),
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(output_path.exists(), "CLI did not create the requested report")
            self.assertEqual(json.loads(output_path.read_text())["response_path"][0], "accelerator")

    def test_bundled_reference_architecture_is_valid(self):
        architecture_contract = self.load_module()
        input_path = Path(__file__).with_name("reference-architecture.json")
        self.assertTrue(input_path.exists(), "reference architecture has not been created")

        report = architecture_contract.validate_architecture(architecture_contract.load_spec(input_path))

        self.assertEqual(report["request_path"][0], "client")
        self.assertEqual(report["request_path"][-1], "accelerator")


if __name__ == "__main__":
    unittest.main()
