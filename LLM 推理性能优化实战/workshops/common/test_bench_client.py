import json
import os
import tempfile
import unittest

from bench_client import (
    MetricsCollector,
    build_payload,
    build_report,
    load_request_plan,
    percentile,
    summarize,
)


class BuildPayloadTest(unittest.TestCase):
    def test_build_payload_uses_chat_completion_shape(self):
        payload = build_payload(model="Qwen/Qwen2.5-0.5B", prompt="hello", max_tokens=32, temperature=0.0)

        self.assertEqual(payload["model"], "Qwen/Qwen2.5-0.5B")
        self.assertEqual(payload["messages"][0]["role"], "user")
        self.assertEqual(payload["messages"][0]["content"], "hello")
        self.assertEqual(payload["max_tokens"], 32)
        self.assertTrue(payload["stream"])
        self.assertEqual(payload["stream_options"], {"include_usage": True})


class MetricsCollectorTest(unittest.TestCase):
    def test_computes_ttft_itl_and_tps(self):
        collector = MetricsCollector(start_time=10.0)
        collector.on_token(10.25, "A")
        collector.on_token(10.35, "B")
        collector.on_token(10.50, "C")
        collector.set_usage(prompt_tokens=100, completion_tokens=3)
        result = collector.finish(end_time=10.70)

        self.assertAlmostEqual(result["ttft_ms"], 250.0)
        self.assertAlmostEqual(result["itl_avg_ms"], 125.0)
        self.assertAlmostEqual(result["total_latency_ms"], 700.0)
        self.assertAlmostEqual(result["tokens_per_second"], 4.29)


class PercentileTest(unittest.TestCase):
    def test_percentile(self):
        self.assertEqual(percentile([1, 2, 3, 4], 50), 2.5)
        self.assertEqual(percentile([1, 2, 3, 4], 95), 3.85)
        self.assertIsNone(percentile([], 95))


class LoadRequestPlanTest(unittest.TestCase):
    def _write_jsonl(self, rows):
        fd, path = tempfile.mkstemp(suffix=".jsonl")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            for row in rows:
                f.write(json.dumps(row) + "\n")
        self.addCleanup(os.remove, path)
        return path

    def test_loads_prompt_and_max_tokens_per_line(self):
        path = self._write_jsonl(
            [
                {"prompt": "short prompt", "max_tokens": 32},
                {"prompt": "a much longer prompt " * 50, "max_tokens": 256},
            ]
        )

        plan = load_request_plan(path, count=2)

        self.assertEqual(len(plan), 2)
        self.assertEqual(plan[0]["prompt"], "short prompt")
        self.assertEqual(plan[0]["max_tokens"], 32)
        self.assertEqual(plan[1]["max_tokens"], 256)

    def test_cycles_when_count_exceeds_file_length(self):
        path = self._write_jsonl([{"prompt": "only one line", "max_tokens": 16}])

        plan = load_request_plan(path, count=5)

        self.assertEqual(len(plan), 5)
        self.assertTrue(all(item["prompt"] == "only one line" for item in plan))

    def test_defaults_max_tokens_when_missing(self):
        path = self._write_jsonl([{"prompt": "no max tokens field"}])

        plan = load_request_plan(path, count=1, default_max_tokens=64)

        self.assertEqual(plan[0]["max_tokens"], 64)

    def test_rejects_empty_file(self):
        path = self._write_jsonl([])

        with self.assertRaises(ValueError):
            load_request_plan(path, count=1)


class SummarizeTest(unittest.TestCase):
    def test_summarize_reports_success_and_percentiles(self):
        results = [
            {"success": True, "ttft_ms": 100.0, "itl_avg_ms": 20.0, "total_latency_ms": 500.0, "tokens_per_second": 10.0},
            {"success": True, "ttft_ms": 200.0, "itl_avg_ms": 30.0, "total_latency_ms": 600.0, "tokens_per_second": 12.0},
            {"success": False, "error": "boom"},
        ]

        summary = summarize(results)

        self.assertEqual(summary["requests"], 3)
        self.assertEqual(summary["successes"], 2)
        self.assertEqual(summary["failures"], 1)
        self.assertAlmostEqual(summary["ttft_avg_ms"], 150.0)
        self.assertEqual(len(summary["failures_detail"]), 1)


class BuildReportTest(unittest.TestCase):
    def test_build_report_includes_label_and_config(self):
        report = build_report(
            label="baseline",
            started_at="2026-09-03T00:00:00+0800",
            base_url="http://127.0.0.1:8000/v1",
            model="Qwen/Qwen2.5-0.5B",
            concurrency=4,
            config={"block-size": "8 (undersized)"},
            results=[{"success": True, "ttft_ms": 1.0}],
            before_gpu=None,
            after_gpu=None,
        )

        self.assertEqual(report["label"], "baseline")
        self.assertEqual(report["concurrency"], 4)
        self.assertEqual(report["config"]["block-size"], "8 (undersized)")


if __name__ == "__main__":
    unittest.main()
