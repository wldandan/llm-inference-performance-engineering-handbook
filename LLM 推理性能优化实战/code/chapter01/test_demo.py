import unittest

from demo import DEFAULT_MODEL, MetricsCollector, build_report, build_payload, percentile


class Chapter01DemoTest(unittest.TestCase):
    def test_default_model_supports_chat_requests(self):
        self.assertEqual(DEFAULT_MODEL, "Qwen/Qwen2.5-0.5B-Instruct")

    def test_build_payload_uses_chat_completion_shape(self):
        payload = build_payload(
            model="Qwen/Qwen2.5-0.5B-Instruct",
            prompt="hello",
            max_tokens=32,
            temperature=0.0,
        )

        self.assertEqual(payload["model"], "Qwen/Qwen2.5-0.5B-Instruct")
        self.assertEqual(payload["messages"][0]["role"], "user")
        self.assertEqual(payload["messages"][0]["content"], "hello")
        self.assertEqual(payload["max_tokens"], 32)
        self.assertTrue(payload["stream"])
        self.assertEqual(payload["stream_options"], {"include_usage": True})

    def test_metrics_collector_computes_ttft_itl_and_tps(self):
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
        self.assertEqual(result["prompt_tokens"], 100)
        self.assertEqual(result["output_tokens"], 3)

    def test_percentile(self):
        self.assertEqual(percentile([1, 2, 3, 4], 50), 2.5)
        self.assertEqual(percentile([1, 2, 3, 4], 95), 3.85)
        self.assertIsNone(percentile([], 95))

    def test_build_report_includes_prompt(self):
        report = build_report(
            started_at="2026-07-30T00:00:00+0800",
            base_url="http://127.0.0.1:8000/v1",
            model="Qwen/Qwen2.5-0.5B-Instruct",
            prompt="hello",
            prompt_repeat=1,
            max_tokens=8,
            concurrency=1,
            results=[{"success": True, "ttft_ms": 1.0}],
            before_gpu=None,
            after_gpu=None,
        )

        self.assertEqual(report["prompt"], "hello")


if __name__ == "__main__":
    unittest.main()
