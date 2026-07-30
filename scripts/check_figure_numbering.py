#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / "chapters"
FIG_RE = re.compile(r"图\d+-\d+")


def main() -> int:
    failed = False
    checked = 0
    for md in sorted(CHAPTERS.glob("chapter*/chapter*.md")):
        checked += 1
        seen = set()
        for lineno, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
            if line.startswith("!["):
                continue
            for fig in FIG_RE.findall(line):
                if fig in seen:
                    print(f"{md}:{lineno}: 重复图号 {fig}")
                    failed = True
                seen.add(fig)
    if failed:
        return 1
    print(f"OK: 已检查 {checked} 个章节文件，未发现重复图号。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
