import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


CHAPTER_DIR = Path(__file__).parent.parent
FIGURE_DIR = CHAPTER_DIR / "figures"
SVG_NS = "http://www.w3.org/2000/svg"
EXPECTED_FIGURES = {
    "fig03-01_token_generation_pipeline.svg": "从文本到下一个 token",
    "fig03-02_decoder_block.svg": "Decoder-only Transformer Block",
    "fig03-03_causal_self_attention.svg": "Causal Self-Attention",
    "fig03-04_gqa_heads.svg": "MHA 与 GQA",
    "fig03-05_prefill_execution.svg": "Prefill",
    "fig03-06_sampling_pipeline.svg": "Sampling",
    "fig03-07_decode_kv_loop.svg": "Decode 与 KV Cache",
    "fig03-08_demo_mechanics_report.svg": "Demo 输出模型机制报告",
}


class ChapterFourFigureTests(unittest.TestCase):
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
                self.assertEqual(root.attrib.get("data-figure-system"), "chapter03-v2")
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
        source = (CHAPTER_DIR / "ch03.md").read_text(encoding="utf-8")
        links = re.findall(r"!\[[^\]]*\]\((figures/[^)]+\.svg)\)", source)
        self.assertEqual(links, [f"figures/{name}" for name in EXPECTED_FIGURES])
        self.assertEqual(re.findall(r"图3-(\d+)[：:]", source), [str(i) for i in range(1, 9)])
        self.assertIn("合成机制报告", source)
        self.assertNotRegex(source, r"(?m)^##\s+4\.\d+\s+.*性能分析")
        self.assertNotRegex(source, r"(?m)^##\s+4\.\d+\s+.*优化")


if __name__ == "__main__":
    unittest.main()
