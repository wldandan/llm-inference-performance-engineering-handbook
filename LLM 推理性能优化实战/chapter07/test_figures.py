import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


CHAPTER_DIR = Path(__file__).parent
FIGURE_DIR = CHAPTER_DIR / "figures"
SVG_NS = "http://www.w3.org/2000/svg"
EXPECTED_FIGURES = {
    "fig07-01_global_performance_model.svg": "Global Performance Model",
    "fig07-02_request_latency_decomposition.svg": "请求端到端延迟分解",
    "fig07-03_ttft_e2e_paths.svg": "TTFT 与 E2E 的两条路径",
    "fig07-04_stage_to_hypothesis.svg": "从阶段时间到候选假设",
    "fig07-05_workload_changes_bottleneck.svg": "Workload 改变瓶颈",
    "fig07-06_critical_path.svg": "关键路径不是简单求和",
    "fig07-07_rag_performance_path.svg": "RAG 端到端性能路径",
    "fig07-08_agent_performance_path.svg": "Agent 端到端性能路径",
    "fig07-09_demo_global_report.svg": "Demo 输出全局性能报告",
}


class ChapterSevenFigureTests(unittest.TestCase):
    def test_figure_set_matches_approved_storyboard(self):
        self.assertEqual(
            set(EXPECTED_FIGURES),
            {path.name for path in FIGURE_DIR.glob("*.svg")},
        )

    def test_every_figure_uses_visual_contract(self):
        for filename, expected_title in EXPECTED_FIGURES.items():
            with self.subTest(filename=filename):
                path = FIGURE_DIR / filename
                source = path.read_text(encoding="utf-8")
                root = ET.fromstring(source)
                self.assertEqual(root.attrib.get("width"), "1280")
                self.assertEqual(root.attrib.get("height"), "720")
                self.assertEqual(root.attrib.get("viewBox"), "0 0 1280 720")
                self.assertEqual(root.attrib.get("data-figure-system"), "chapter07-v2")
                self.assertIn("aria-labelledby", root.attrib)
                title = root.find(f"{{{SVG_NS}}}title")
                description = root.find(f"{{{SVG_NS}}}desc")
                self.assertIsNotNone(title)
                self.assertIsNotNone(description)
                self.assertIn(expected_title, title.text or "")
                self.assertGreater(len((description.text or "").strip()), 20)
                self.assertIn("PingFang SC", source)
                self.assertIn("关键结论", source)
                self.assertIn("marker-end", source)
                font_sizes = [int(value) for value in re.findall(r"font-size:\s*(\d+)px", source)]
                self.assertTrue(font_sizes)
                self.assertGreaterEqual(min(font_sizes), 14)
                note = path.with_suffix(".figure-note.md")
                self.assertTrue(note.exists())
                note_source = note.read_text(encoding="utf-8")
                self.assertIn("来源段落", note_source)
                self.assertIn("关键结论", note_source)

    def test_chapter_links_nine_continuous_figures(self):
        source = (CHAPTER_DIR / "chapter07.md").read_text(encoding="utf-8")
        links = re.findall(r"!\[[^\]]*\]\((figures/[^)]+\.svg)\)", source)
        self.assertEqual(links, [f"figures/{name}" for name in EXPECTED_FIGURES])
        self.assertEqual(re.findall(r"图7-(\d+)[：:]", source), [str(i) for i in range(1, 10)])
        self.assertIn("RAG", source)
        self.assertIn("Agent", source)
        self.assertIn("Critical Path", source)


if __name__ == "__main__":
    unittest.main()
