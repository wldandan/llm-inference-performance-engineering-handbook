import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


FIGURE_DIR = Path(__file__).parent / "figures"
SVG_NS = "http://www.w3.org/2000/svg"

EXPECTED_FIGURES = {
    "fig03-01_inference_system_architecture.svg": "LLM 推理系统全局架构",
    "fig03-02_client_gateway_boundary.svg": "Client 与 Gateway 边界",
    "fig03-03_scheduler_responsibility.svg": "三层流量决策",
    "fig03-04_worker_runtime_accelerator.svg": "Worker、Runtime 与 Accelerator",
    "fig03-05_serving_state_types.svg": "推理服务的三类状态",
    "fig03-06_deployment_patterns.svg": "LLM Serving 部署形态",
    "fig03-07_system_layer_mapping.svg": "成熟系统的架构层级映射",
    "fig03-08_architecture_to_analysis.svg": "从现象到组件和观测点",
    "fig03-09_demo_architecture_contract.svg": "架构契约 Demo",
    "fig03-10_chapter_boundary.svg": "Chapter 3 的章节边界",
}


class FigureSystemTests(unittest.TestCase):
    def test_figure_set_is_complete(self):
        self.assertEqual(
            set(EXPECTED_FIGURES),
            {path.name for path in FIGURE_DIR.glob("*.svg")},
        )

    def test_every_figure_uses_v2_visual_contract(self):
        for filename, expected_title in EXPECTED_FIGURES.items():
            with self.subTest(filename=filename):
                path = FIGURE_DIR / filename
                source = path.read_text(encoding="utf-8")
                root = ET.fromstring(source)

                self.assertEqual(root.attrib.get("width"), "1280")
                self.assertEqual(root.attrib.get("height"), "720")
                self.assertEqual(root.attrib.get("viewBox"), "0 0 1280 720")
                self.assertEqual(
                    root.attrib.get("data-figure-system"), "chapter03-v2"
                )
                self.assertIn("aria-labelledby", root.attrib)

                title = root.find(f"{{{SVG_NS}}}title")
                description = root.find(f"{{{SVG_NS}}}desc")
                self.assertIsNotNone(title)
                self.assertIsNotNone(description)
                self.assertIn(expected_title, title.text or "")
                self.assertGreater(len((description.text or "").strip()), 20)

                self.assertIn("PingFang SC", source)
                self.assertIn("关键结论", source)
                self.assertNotIn("Key Takeaway", source)
                self.assertIn("marker-end", source)

                font_sizes = [
                    int(value)
                    for value in re.findall(r"font-size:\s*(\d+)px", source)
                ]
                self.assertTrue(font_sizes)
                self.assertGreaterEqual(min(font_sizes), 14)


if __name__ == "__main__":
    unittest.main()
