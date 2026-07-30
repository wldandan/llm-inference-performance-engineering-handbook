#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / "chapters"
OUT = ROOT / "chapter-status.md"
IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def yes(value: bool) -> str:
    return "是" if value else "否"


def main() -> int:
    rows = ["# Chapter Status", "", "| 章节 | Markdown | Review | Storyboard | Figures |", "|---|---|---|---:|---:|"]
    for chapter in sorted(CHAPTERS.glob("chapter*")):
        if not chapter.is_dir():
            continue
        md = chapter / f"{chapter.name}.md"
        review = chapter / "review.md"
        storyboard = chapter / "storyboard.md"
        figures = 0
        if md.exists():
            figures = len(IMG_RE.findall(md.read_text(encoding="utf-8")))
        rows.append(f"| {chapter.name} | {yes(md.exists())} | {yes(review.exists())} | {yes(storyboard.exists())} | {figures} |")
    OUT.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
