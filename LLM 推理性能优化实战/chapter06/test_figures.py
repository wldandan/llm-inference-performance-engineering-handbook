import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


CHAPTER_DIR = Path(__file__).parent
FIGURE_DIR = CHAPTER_DIR / "figures"
SVG_NS = "http://www.w3.org/2000/svg"
EXPECTED_FIGURES = {
    "fig06-01_metric_question_map.svg": "指标先回答问题",
    "fig06-02_measurement_boundaries.svg": "客户端与服务端测量边界",
    "fig06-03_ttft_tpot_itl_timeline.svg": "TTFT、TPOT 与 ITL",
    "fig06-04_throughput_and_goodput.svg": "TPS、RPS 与 Goodput",
    "fig06-05_percentiles_and_tail.svg": "P50、P95 与 P99",
    "fig06-06_resource_vs_outcome.svg": "资源指标与结果指标",
    "fig06-07_cost_denominators.svg": "成本指标的分母",
    "fig06-08_metric_contract.svg": "可比较的指标合同",
    "fig06-09_demo_metrics_report.svg": "Demo 输出指标报告",
}


class ChapterSixFigureTests(unittest.TestCase):
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
                self.assertEqual(root.attrib.get("data-figure-system"), "chapter06-v2")
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
        source = (CHAPTER_DIR / "chapter06.md").read_text(encoding="utf-8")
        links = re.findall(r"!\[[^\]]*\]\((figures/[^)]+\.svg)\)", source)
        self.assertEqual(links, [f"figures/{name}" for name in EXPECTED_FIGURES])
        self.assertEqual(re.findall(r"图6-(\d+)[：:]", source), [str(i) for i in range(1, 10)])
        self.assertIn("nearest-rank", source)
        self.assertIn("Goodput", source)
        self.assertIn("成本分母", source)


if __name__ == "__main__":
    unittest.main()
