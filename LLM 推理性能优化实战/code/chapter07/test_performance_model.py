import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("performance_model.py")


def load_performance_model():
    if not MODULE_PATH.exists():
        raise AssertionError("code/chapter07/performance_model.py must exist")
    spec = importlib.util.spec_from_file_location("chapter07_performance_model", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def node(node_id, duration_ms, depends_on=None, category="other"):
    return {
        "id": node_id,
        "duration_ms": duration_ms,
        "depends_on": depends_on or [],
        "category": category,
    }


class GlobalPerformanceModelTests(unittest.TestCase):
    def setUp(self):
        self.model = load_performance_model()

    def test_sequential_request_critical_path_equals_stage_sum(self):
        nodes = [
            node("ingress", 10, category="network"),
            node("queue", 40, ["ingress"], "queue"),
            node("prefill", 100, ["queue"], "prefill"),
            node("decode", 300, ["prefill"], "decode"),
            node("egress", 20, ["decode"], "network"),
        ]
        result = self.model.analyze_critical_path(nodes)
        self.assertEqual(result["critical_path_ms"], 470)
        self.assertEqual(
            result["critical_path"], ["ingress", "queue", "prefill", "decode", "egress"]
        )

    def test_parallel_rag_branches_use_longest_path_not_total_sum(self):
        nodes = [
            node("ingress", 10),
            node("dense_retrieval", 100, ["ingress"], "retrieval"),
            node("keyword_retrieval", 200, ["ingress"], "retrieval"),
            node("merge", 20, ["dense_retrieval", "keyword_retrieval"], "orchestration"),
            node("llm", 300, ["merge"], "decode"),
        ]
        result = self.model.analyze_critical_path(nodes)
        self.assertEqual(result["critical_path_ms"], 530)
        self.assertEqual(result["critical_path"], ["ingress", "keyword_retrieval", "merge", "llm"])
        self.assertEqual(result["all_node_time_ms"], 630)

    def test_cycles_are_rejected(self):
        nodes = [node("a", 1, ["b"]), node("b", 1, ["a"])]
        with self.assertRaisesRegex(ValueError, "cycle"):
            self.model.analyze_critical_path(nodes)

    def test_unknown_dependencies_and_duplicate_ids_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "unknown dependency"):
            self.model.analyze_critical_path([node("a", 1, ["missing"])])
        with self.assertRaisesRegex(ValueError, "duplicate"):
            self.model.analyze_critical_path([node("a", 1), node("a", 2)])

    def test_negative_duration_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "duration_ms"):
            self.model.analyze_critical_path([node("a", -1)])

    def test_queue_hypothesis_names_required_evidence(self):
        nodes = [
            node("queue", 500, category="queue"),
            node("prefill", 100, ["queue"], "prefill"),
        ]
        hypotheses = self.model.rank_hypotheses(nodes)
        self.assertEqual(hypotheses[0]["stage_id"], "queue")
        self.assertEqual(hypotheses[0]["hypothesis"], "scheduling_or_capacity_pressure")
        self.assertIn("waiting_requests", hypotheses[0]["evidence_needed"])

    def test_decode_hypothesis_remains_unconfirmed(self):
        nodes = [node("decode", 400, category="decode")]
        hypothesis = self.model.rank_hypotheses(nodes)[0]
        self.assertEqual(hypothesis["status"], "needs_evidence")
        self.assertIn("kernel_timeline", hypothesis["evidence_needed"])
        self.assertNotIn("root_cause", hypothesis)

    def test_agent_report_preserves_repeated_llm_and_tool_nodes(self):
        scenario = {
            "name": "agent-support-task",
            "kind": "agent",
            "nodes": [
                node("llm_plan", 220, category="prefill"),
                node("tool_crm", 500, ["llm_plan"], "tool"),
                node("tool_search", 300, ["llm_plan"], "tool"),
                node("llm_answer", 420, ["tool_crm", "tool_search"], "decode"),
            ],
        }
        report = self.model.build_report(scenario)
        self.assertEqual(report["mode"], "synthetic_global_performance_model")
        self.assertEqual(report["scenario"]["kind"], "agent")
        self.assertEqual(report["analysis"]["critical_path_ms"], 1140)
        self.assertEqual(
            report["analysis"]["critical_path"], ["llm_plan", "tool_crm", "llm_answer"]
        )
        self.assertIn("不是 Root Cause", report["note"])


if __name__ == "__main__":
    unittest.main()
