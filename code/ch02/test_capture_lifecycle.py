import importlib.util
import math
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("capture_lifecycle.py")


def load_capture():
    if not MODULE_PATH.exists():
        raise AssertionError("code/ch02/capture_lifecycle.py must exist")
    spec = importlib.util.spec_from_file_location("chapter02_capture_lifecycle", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class CaptureLifecycleTest(unittest.TestCase):
    def setUp(self):
        self.capture = load_capture()

    def test_payload_requests_stream_usage_for_one_generation(self):
        payload = self.capture.build_payload("demo-model", "hello", 32, 0.0)
        self.assertTrue(payload["stream"])
        self.assertEqual(payload["stream_options"], {"include_usage": True})
        self.assertEqual(payload["n"], 1)

    def test_collector_separates_client_observations_from_server_metrics(self):
        collector = self.capture.LifecycleCollector(start_ms=100.0)
        collector.on_response_open(112.0)
        collector.on_payload(
            {
                "id": "chatcmpl-1",
                "choices": [{"delta": {"content": "你"}}],
            },
            150.0,
        )
        collector.on_payload(
            {
                "id": "chatcmpl-1",
                "choices": [{"delta": {"content": "好"}}],
                "usage": {"prompt_tokens": 3, "completion_tokens": 2},
                "metrics": {
                    "queue_time_ms": 4.0,
                    "time_to_first_token_ms": 35.0,
                    "generation_time_ms": 10.0,
                    "mean_itl_ms": 10.0,
                    "tokens_per_second": 44.4,
                },
            },
            160.0,
        )

        report = collector.finish(done_ms=170.0)

        self.assertEqual(report["request_id"], "chatcmpl-1")
        self.assertEqual(report["direct_observations"]["usage"]["completion_tokens"], 2)
        self.assertEqual(
            report["direct_observations"]["server_per_request_metrics_ms"]["queue_time_ms"],
            4.0,
        )
        self.assertEqual(report["derived_client_durations_ms"]["time_to_first_content_chunk"], 50.0)
        self.assertEqual(report["phase_evidence"]["queue"]["evidence"], "direct_duration")
        self.assertEqual(
            report["phase_evidence"]["scheduled_to_first_token"]["evidence"],
            "direct_duration",
        )
        self.assertEqual(report["phase_evidence"]["request_received"]["evidence"], "inferred")

    def test_missing_server_metrics_are_reported_as_unavailable_not_zero(self):
        collector = self.capture.LifecycleCollector(start_ms=0.0)
        collector.on_response_open(2.0)
        collector.on_payload(
            {"id": "chatcmpl-2", "choices": [{"delta": {"content": "x"}}]},
            10.0,
        )
        report = collector.finish(done_ms=20.0)

        self.assertIsNone(report["direct_observations"]["server_per_request_metrics_ms"])
        self.assertEqual(report["phase_evidence"]["queue"]["evidence"], "unavailable")
        self.assertIn("--enable-per-request-metrics", report["warnings"][0])

    def test_empty_or_partial_server_metrics_fail_acceptance(self):
        collector = self.capture.LifecycleCollector(start_ms=0.0)
        collector.on_response_open(1.0)
        collector.on_payload(
            {"id": "chatcmpl-empty", "choices": [], "metrics": {}},
            2.0,
        )
        report = collector.finish(done_ms=3.0)

        self.assertFalse(report["acceptance"]["server_metrics_complete"])
        self.assertEqual(report["acceptance"]["status"], "incomplete")
        self.assertFalse(
            self.capture.server_metrics_complete(
                {"queue_time_ms": 1.0, "time_to_first_token_ms": 2.0}
            )
        )

    def test_required_server_metrics_must_be_finite_and_non_negative(self):
        valid = {
            "queue_time_ms": 1.0,
            "time_to_first_token_ms": 2.0,
            "generation_time_ms": 3.0,
        }
        self.assertTrue(self.capture.server_metrics_complete(valid))
        self.assertFalse(self.capture.server_metrics_complete({**valid, "queue_time_ms": -1.0}))
        self.assertFalse(
            self.capture.server_metrics_complete(
                {**valid, "generation_time_ms": float("nan")}
            )
        )

    def test_complete_acceptance_requires_environment_and_request_evidence(self):
        collector = self.capture.LifecycleCollector(start_ms=0.0)
        collector.on_response_open(1.0)
        collector.on_payload(
            {
                "id": "chatcmpl-complete",
                "choices": [{"delta": {"content": "x"}}],
                "usage": {"prompt_tokens": 2, "completion_tokens": 1},
                "metrics": {
                    "queue_time_ms": 1.0,
                    "time_to_first_token_ms": 2.0,
                    "generation_time_ms": 3.0,
                },
            },
            4.0,
        )
        environment = {
            "python_version": "3.12.3",
            "vllm_version": "0.11.0",
            "gpu": "NVIDIA GB10",
            "model": "Qwen/Qwen2.5-0.5B-Instruct",
            "model_revision": "local-snapshot",
            "server_command": "vllm serve ... --enable-per-request-metrics",
        }

        report = collector.finish(done_ms=5.0, environment=environment)

        self.assertEqual(report["acceptance"]["status"], "complete")
        self.assertTrue(report["acceptance"]["evidence_complete"])
        self.assertEqual(report["environment"]["gpu"], "NVIDIA GB10")

    def test_prometheus_parser_aggregates_labels_and_computes_deltas(self):
        before = """
vllm:request_queue_time_seconds_sum{model_name="m"} 1.5
vllm:request_queue_time_seconds_count{model_name="m"} 2
vllm:request_success_total{finished_reason="stop",model_name="m"} 3
"""
        after = """
vllm:request_queue_time_seconds_sum{model_name="m"} 1.7
vllm:request_queue_time_seconds_count{model_name="m"} 3
vllm:request_success_total{finished_reason="stop",model_name="m"} 4
"""
        before_values = self.capture.parse_prometheus_totals(before)
        after_values = self.capture.parse_prometheus_totals(after)
        delta = self.capture.metric_deltas(before_values, after_values)

        self.assertTrue(math.isclose(delta["vllm:request_queue_time_seconds_sum"], 0.2))
        self.assertEqual(delta["vllm:request_queue_time_seconds_count"], 1.0)
        self.assertEqual(delta["vllm:request_success_total"], 1.0)

    def test_report_labels_prometheus_delta_as_aggregate_evidence(self):
        collector = self.capture.LifecycleCollector(start_ms=0.0)
        collector.on_response_open(1.0)
        collector.on_payload(
            {"id": "chatcmpl-3", "choices": [{"delta": {"content": "x"}}]},
            5.0,
        )
        report = collector.finish(
            done_ms=8.0,
            prometheus_delta={"vllm:request_prefill_time_seconds_count": 1.0},
        )

        self.assertEqual(
            report["direct_observations"]["server_prometheus_delta"]["scope"],
            "server_aggregate",
        )
        self.assertIn("concurrent traffic", report["warnings"][-1])


if __name__ == "__main__":
    unittest.main()
