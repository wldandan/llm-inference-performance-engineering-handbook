import re
import unittest
from pathlib import Path


COURSE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = COURSE_ROOT.parent
CODE_DIR = REPOSITORY_ROOT / "code"

EXPECTED_IMPLEMENTED_FILES = {
    1: {"README.md", "demo.py", "start_vllm.py", "test_demo.py", "test_start_vllm.py"},
    2: {"README.md", "lifecycle_trace.py", "sample-events.jsonl", "test_lifecycle_trace.py"},
    3: {
        "README.md",
        "architecture_contract.py",
        "reference-architecture.json",
        "test_architecture_contract.py",
    },
    4: {"README.md", "mechanics.py", "test_mechanics.py"},
    5: {"README.md", "gpu_model.py", "test_gpu_model.py"},
    6: {"README.md", "metrics_report.py", "sample.jsonl", "test_metrics_report.py"},
    7: {
        "README.md",
        "performance_model.py",
        "sample_agent.json",
        "sample_llm_request.json",
        "sample_rag.json",
        "test_performance_model.py",
    },
}


class CentralCodeLayoutTests(unittest.TestCase):
    def test_code_directory_is_at_repository_root(self):
        self.assertTrue(CODE_DIR.is_dir())
        self.assertFalse((COURSE_ROOT / "code").exists())

    def test_implemented_demos_live_in_chapter_named_code_directories(self):
        for chapter, expected_files in EXPECTED_IMPLEMENTED_FILES.items():
            with self.subTest(chapter=chapter):
                chapter_dir = CODE_DIR / f"chapter{chapter:02d}"
                self.assertTrue(chapter_dir.is_dir())
                self.assertEqual(
                    {path.name for path in chapter_dir.iterdir() if path.name != "__pycache__"},
                    expected_files,
                )

    def test_legacy_demo_directories_are_removed(self):
        legacy = [
            COURSE_ROOT / f"chapter{chapter:02d}" / "demo"
            for chapter in range(1, 31)
            if (COURSE_ROOT / f"chapter{chapter:02d}" / "demo").exists()
        ]
        self.assertEqual(legacy, [])

    def test_code_index_names_all_thirty_chapters_and_implemented_paths(self):
        index = (CODE_DIR / "README.md").read_text(encoding="utf-8")
        self.assertEqual(
            re.findall(r"^\| Ch(\d{2}) \|", index, flags=re.MULTILINE),
            [f"{chapter:02d}" for chapter in range(1, 31)],
        )
        for chapter in EXPECTED_IMPLEMENTED_FILES:
            self.assertIn(f"[code/chapter{chapter:02d}](chapter{chapter:02d}/README.md)", index)

    def test_chapter_readmes_use_repository_root_commands(self):
        index = (CODE_DIR / "README.md").read_text(encoding="utf-8")
        self.assertIn("从 Git 仓库根目录运行", index)

        for chapter in EXPECTED_IMPLEMENTED_FILES:
            with self.subTest(chapter=chapter):
                source = (CODE_DIR / f"chapter{chapter:02d}" / "README.md").read_text(
                    encoding="utf-8"
                )
                self.assertIn("从 Git 仓库根目录", source)
                self.assertIn(
                    f"python3 -m unittest discover -s code/chapter{chapter:02d} "
                    "-p 'test_*.py'",
                    source,
                )

    def test_active_course_markdown_contains_no_legacy_demo_paths(self):
        documents = list(COURSE_ROOT.glob("*.md"))
        for chapter in range(1, 31):
            chapter_dir = COURSE_ROOT / f"chapter{chapter:02d}"
            documents.extend(chapter_dir.glob("*.md"))
            documents.extend((chapter_dir / "figures").glob("*.md"))

        violations = []
        legacy_path = re.compile(r"(?<!code/)chapter\d{2}/demo(?:/|\b)|\]\(demo/")
        for document in documents:
            if legacy_path.search(document.read_text(encoding="utf-8")):
                violations.append(document.relative_to(COURSE_ROOT).as_posix())
        self.assertEqual(violations, [])


if __name__ == "__main__":
    unittest.main()
