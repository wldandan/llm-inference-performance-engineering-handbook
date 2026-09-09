import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


FIGURE_DIR = Path(__file__).parent
SVG_NS = "http://www.w3.org/2000/svg"
EXPECTED_FIGURES = {
    "fig01-01_client_service_observation.svg": "一次流式请求的两个视角",
    "fig01-02_first_service_runbook.svg": "启动服务并完成第一次调用",
    "fig01-03_demo_observation_mapping.svg": "Demo 字段映射到客户端观察点",
    "fig01-04_chapter_boundary.svg": "第 1 章只负责跑通与观察",
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

    def test_overview_separates_client_observations_from_server_preview(self):
        source = (
            FIGURE_DIR / "fig01-01_client_service_observation.svg"
        ).read_text(encoding="utf-8")
        for label in ["客户端观察", "服务内部", "首个 chunk", "持续流式返回"]:
            self.assertIn(label, source)
        self.assertNotIn("Gateway", source)

    def test_chapter_uses_four_continuous_figures_without_mechanism_sections(self):
        chapter_source = (Path(__file__).parent.parent / "ch01.md").read_text(
            encoding="utf-8"
        )
        image_links = re.findall(r"!\[[^\]]*\]\((figures/[^)]+\.svg)\)", chapter_source)
        self.assertEqual(
            image_links,
            [f"figures/{filename}" for filename in EXPECTED_FIGURES],
        )
        captions = re.findall(r"图1-(\d+)[：:]", chapter_source)
        self.assertEqual(captions, ["1", "2", "3", "4"])
        for heading in ["Gateway", "Queue", "Prefill", "Decode", "KV Cache"]:
            self.assertNotRegex(chapter_source, rf"(?m)^##\s+1\.\d+\s+{heading}")
        self.assertIn("本章不把客户端观察值直接归因到某个服务端阶段", chapter_source)


if __name__ == "__main__":
    unittest.main()
