#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / "chapters"
IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def main() -> int:
    failed = False
    checked = 0
    for md in sorted(CHAPTERS.glob("chapter*/chapter*.md")):
        checked += 1
        base = md.parent
        for target in IMG_RE.findall(md.read_text(encoding="utf-8")):
            if "://" in target or target.startswith("#"):
                continue
            path = base / target
            if not path.exists():
                print(f"{md}: 图片不存在 -> {target}")
                failed = True
    if failed:
        return 1
    print(f"OK: 已检查 {checked} 个章节文件，所有本地图片链接有效。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
