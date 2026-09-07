import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).with_name("validate_part.py")
SPEC = importlib.util.spec_from_file_location("validate_part", SCRIPT_PATH)
validate_part = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validate_part)


class ValidatePartTests(unittest.TestCase):
    def test_chapter_one_accepts_four_purposeful_figures(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            chapter_dir = root / "chapter01"
            figures_dir = chapter_dir / "figures"
            figures_dir.mkdir(parents=True)
            (chapter_dir / "review.md").write_text("# Review\n", encoding="utf-8")
            (chapter_dir / "storyboard.md").write_text("# Storyboard\n", encoding="utf-8")

            links = []
            captions = []
            for index in range(1, 5):
                filename = f"fig01-{index:02d}_purposeful.svg"
                (figures_dir / filename).write_text(
                    '<svg xmlns="http://www.w3.org/2000/svg"/>', encoding="utf-8"
                )
                links.append(f"![图](figures/{filename})")
                captions.append(f"图1-{index}：图标题。")

            sections = "\n".join(f"## 1.{index} 小节" for index in range(6))
            chapter_text = "\n".join(
                [
                    "# Chapter 1",
                    "学习目标 核心问题 Demo 本章总结",
                    sections,
                    "课堂案例 补充案例 A 补充案例 B",
                    *links,
                    *captions,
                ]
            )
            (chapter_dir / "chapter01.md").write_text(chapter_text, encoding="utf-8")

            self.assertEqual(validate_part.validate_chapter(root, 1), [])

    def test_chapter_four_accepts_eight_mechanics_figures(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            chapter_dir = root / "chapter04"
            figures_dir = chapter_dir / "figures"
            figures_dir.mkdir(parents=True)
            (chapter_dir / "review.md").write_text("# Review\n", encoding="utf-8")
            (chapter_dir / "storyboard.md").write_text("# Storyboard\n", encoding="utf-8")

            links = []
            captions = []
            for index in range(1, 9):
                filename = f"fig04-{index:02d}_purposeful.svg"
                (figures_dir / filename).write_text(
                    '<svg xmlns="http://www.w3.org/2000/svg"/>', encoding="utf-8"
                )
                links.append(f"![图](figures/{filename})")
                captions.append(f"图4-{index}：图标题。")

            sections = "\n".join(f"## 4.{index} 小节" for index in range(6))
            chapter_text = "\n".join(
                [
                    "# Chapter 4",
                    "学习目标 核心问题 Demo 本章总结",
                    sections,
                    "课堂案例 补充案例 A 补充案例 B",
                    *links,
                    *captions,
                ]
            )
            (chapter_dir / "chapter04.md").write_text(chapter_text, encoding="utf-8")

            self.assertEqual(validate_part.validate_chapter(root, 4), [])

    def test_chapter_five_accepts_eight_gpu_mental_model_figures(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            chapter_dir = root / "chapter05"
            figures_dir = chapter_dir / "figures"
            figures_dir.mkdir(parents=True)
            (chapter_dir / "review.md").write_text("# Review\n", encoding="utf-8")
            (chapter_dir / "storyboard.md").write_text("# Storyboard\n", encoding="utf-8")

            links = []
            captions = []
            for index in range(1, 9):
                filename = f"fig05-{index:02d}_purposeful.svg"
                (figures_dir / filename).write_text(
                    '<svg xmlns="http://www.w3.org/2000/svg"/>', encoding="utf-8"
                )
                links.append(f"![图](figures/{filename})")
                captions.append(f"图5-{index}：图标题。")

            sections = "\n".join(f"## 5.{index} 小节" for index in range(6))
            chapter_text = "\n".join(
                [
                    "# Chapter 5",
                    "学习目标 核心问题 Demo 本章总结",
                    sections,
                    "课堂案例 补充案例 A 补充案例 B",
                    *links,
                    *captions,
                ]
            )
            (chapter_dir / "chapter05.md").write_text(chapter_text, encoding="utf-8")

            self.assertEqual(validate_part.validate_chapter(root, 5), [])

    def test_chapter_six_accepts_nine_metrics_figures(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            chapter_dir = root / "chapter06"
            figures_dir = chapter_dir / "figures"
            figures_dir.mkdir(parents=True)
            (chapter_dir / "review.md").write_text("# Review\n", encoding="utf-8")
            (chapter_dir / "storyboard.md").write_text("# Storyboard\n", encoding="utf-8")

            links = []
            captions = []
            for index in range(1, 10):
                filename = f"fig06-{index:02d}_purposeful.svg"
                (figures_dir / filename).write_text(
                    '<svg xmlns="http://www.w3.org/2000/svg"/>', encoding="utf-8"
                )
                links.append(f"![图](figures/{filename})")
                captions.append(f"图6-{index}：图标题。")

            sections = "\n".join(f"## 6.{index} 小节" for index in range(6))
            chapter_text = "\n".join(
                [
                    "# Chapter 6",
                    "学习目标 核心问题 Demo 本章总结",
                    sections,
                    "课堂案例 补充案例 A 补充案例 B",
                    *links,
                    *captions,
                ]
            )
            (chapter_dir / "chapter06.md").write_text(chapter_text, encoding="utf-8")

            self.assertEqual(validate_part.validate_chapter(root, 6), [])


if __name__ == "__main__":
    unittest.main()
