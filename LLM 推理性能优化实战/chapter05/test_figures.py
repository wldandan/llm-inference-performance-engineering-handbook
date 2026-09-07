import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


CHAPTER_DIR = Path(__file__).parent
FIGURE_DIR = CHAPTER_DIR / "figures"
SVG_NS = "http://www.w3.org/2000/svg"
EXPECTED_FIGURES = {
    "fig05-01_four_gpu_constraints.svg": "GPU 的四类工程约束",
    "fig05-02_llm_work_to_gpu_resources.svg": "LLM 工作怎样落到 GPU 资源",
    "fig05-03_memory_capacity_budget.svg": "显存容量预算",
    "fig05-04_memory_bandwidth_path.svg": "显存带宽",
    "fig05-05_compute_and_roofline.svg": "算力与 Roofline 直觉",
    "fig05-06_kernel_launch_overhead.svg": "Kernel Launch Overhead",
    "fig05-07_advanced_gpu_map.svg": "进阶硬件地图",
    "fig05-08_demo_gpu_report.svg": "Demo 输出 GPU 约束报告",
}


class ChapterFiveFigureTests(unittest.TestCase):
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
                self.assertEqual(root.attrib.get("data-figure-system"), "chapter05-v2")
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

    def test_chapter_links_eight_continuous_figures(self):
        source = (CHAPTER_DIR / "chapter05.md").read_text(encoding="utf-8")
        links = re.findall(r"!\[[^\]]*\]\((figures/[^)]+\.svg)\)", source)
        self.assertEqual(links, [f"figures/{name}" for name in EXPECTED_FIGURES])
        self.assertEqual(re.findall(r"图5-(\d+)[：:]", source), [str(i) for i in range(1, 9)])
        self.assertIn("四类约束", source)
        self.assertIn("Bridge", source)
        self.assertNotRegex(source, r"(?m)^##\s+5\.\d+\s+.*选购")
        self.assertNotRegex(source, r"(?m)^##\s+5\.\d+\s+.*CUDA 编程")


if __name__ == "__main__":
    unittest.main()
