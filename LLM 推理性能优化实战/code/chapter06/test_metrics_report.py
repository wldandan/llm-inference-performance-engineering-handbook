import importlib.util
import math
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("metrics_report.py")


def load_metrics_report():
    if not MODULE_PATH.exists():
        raise AssertionError("code/chapter06/metrics_report.py must exist")
    spec = importlib.util.spec_from_file_location("chapter06_metrics_report", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def record(
    request_id,
    start_ms,
    token_times_ms,
    end_ms,
    prompt_tokens=10,
    output_tokens=None,
    success=True,
    cost_usd=0.01,
):
    if output_tokens is None:
        output_tokens = len(token_times_ms)
    return {
        "request_id": request_id,
        "start_ms": start_ms,
        "token_times_ms": token_times_ms,
        "end_ms": end_ms,
        "prompt_tokens": prompt_tokens,
        "output_tokens": output_tokens,
        "success": success,
        "cost_usd": cost_usd,
    }


class MetricsReportTests(unittest.TestCase):
    def setUp(self):
        self.metrics = load_metrics_report()

    def test_request_metrics_compute_ttft_e2e_and_itl(self):
        metrics = self.metrics.request_metrics(record("a", 100, [160, 200, 250], 270))
        self.assertEqual(metrics["ttft_ms"], 60)
        self.assertEqual(metrics["e2e_ms"], 170)
        self.assertEqual(metrics["itls_ms"], [40, 50])

    def test_tpot_excludes_first_token_interval(self):
        metrics = self.metrics.request_metrics(record("a", 0, [100, 140, 200], 210))
        self.assertEqual(metrics["tpot_ms"], 50)

    def test_throughput_uses_shared_wall_clock_window(self):
        records = [
            record("a", 0, [100, 150], 200),
            record("b", 50, [120, 180, 240], 250),
        ]
        report = self.metrics.build_report(records, ttft_slo_ms=200, e2e_slo_ms=400)
        self.assertTrue(math.isclose(report["throughput"]["output_tokens_per_second"], 20))
        self.assertTrue(math.isclose(report["throughput"]["requests_per_second"], 8))

    def test_goodput_requires_success_and_both_slos(self):
        records = [
            record("good", 0, [100, 140], 160),
            record("slow", 0, [250, 290], 320),
            record("failed", 0, [], 100, output_tokens=0, success=False),
        ]
        report = self.metrics.build_report(records, ttft_slo_ms=200, e2e_slo_ms=300)
        self.assertEqual(report["throughput"]["good_requests"], 1)
        self.assertTrue(
            math.isclose(report["throughput"]["goodput_requests_per_second"], 3.125)
        )

    def test_nearest_rank_percentile_is_explicit_and_deterministic(self):
        values = list(range(1, 101))
        self.assertEqual(self.metrics.nearest_rank_percentile(values, 50), 50)
        self.assertEqual(self.metrics.nearest_rank_percentile(values, 95), 95)
        self.assertEqual(self.metrics.nearest_rank_percentile(values, 99), 99)

    def test_cost_metrics_name_their_denominators(self):
        records = [
            record("a", 0, [10, 20], 30, cost_usd=0.02),
            record("b", 0, [10, 20, 30], 40, cost_usd=0.03),
        ]
        report = self.metrics.build_report(records, ttft_slo_ms=50, e2e_slo_ms=50)
        self.assertTrue(
            math.isclose(report["cost"]["usd_per_million_output_tokens"], 10_000)
        )
        self.assertTrue(math.isclose(report["cost"]["usd_per_successful_request"], 0.025))

    def test_invalid_or_inconsistent_records_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "sorted"):
            self.metrics.request_metrics(record("a", 0, [100, 90], 120))
        with self.assertRaisesRegex(ValueError, "output_tokens"):
            self.metrics.request_metrics(record("b", 0, [100], 120, output_tokens=2))
        with self.assertRaisesRegex(ValueError, "failed"):
            self.metrics.request_metrics(
                record("c", 0, [100], 120, output_tokens=1, success=False)
            )

    def test_report_carries_measurement_contract_and_percentile_method(self):
        report = self.metrics.build_report(
            [record("a", 0, [100, 150], 180)],
            ttft_slo_ms=200,
            e2e_slo_ms=300,
            workload={"name": "interactive-chat", "concurrency": 1},
        )
        self.assertEqual(report["mode"], "synthetic_client_metrics")
        self.assertEqual(report["measurement_contract"]["clock"], "client_wall_clock_ms")
        self.assertEqual(report["measurement_contract"]["percentile_method"], "nearest_rank")
        self.assertEqual(report["workload"]["name"], "interactive-chat")
        self.assertIn("不是 Benchmark", report["note"])


if __name__ == "__main__":
    unittest.main()
