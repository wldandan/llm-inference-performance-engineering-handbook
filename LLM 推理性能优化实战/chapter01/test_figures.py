import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


FIGURE_DIR = Path(__file__).parent / "figures"
SVG_NS = "http://www.w3.org/2000/svg"
EXPECTED_FIGURES = {
    "fig01-01_request_lifecycle_overview.svg": "第一个请求与生命周期总览",
    "fig01-02_gateway_request_entry.svg": "Gateway 请求入口",
    "fig01-03_queue_scheduler.svg": "Queue 与 Scheduler",
    "fig01-04_prefill_position.svg": "Prefill 在生命周期中的位置",
    "fig01-05_first_token_streaming.svg": "首个 token 与流式返回",
    "fig01-06_decode_loop.svg": "Decode Loop",
    "fig01-07_kv_cache_lifecycle.svg": "KV Cache 生命周期",
    "fig01-08_finish_cleanup.svg": "请求结束与资源回收",
    "fig01-09_demo_field_mapping.svg": "Demo 字段映射到生命周期",
    "fig01-10_lifecycle_boundaries.svg": "本章与后续章节边界",
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
                self.assertEqual(root.attrib.get("data-figure-system"), "chapter01-v2")
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

                font_sizes = [int(value) for value in re.findall(r"font-size:\s*(\d+)px", source)]
                self.assertTrue(font_sizes)
                self.assertGreaterEqual(min(font_sizes), 14)

                note = path.with_suffix(".figure-note.md")
                self.assertTrue(note.exists())
                note_source = note.read_text(encoding="utf-8")
                self.assertIn("来源段落", note_source)
                self.assertIn("关键结论", note_source)


if __name__ == "__main__":
    unittest.main()
