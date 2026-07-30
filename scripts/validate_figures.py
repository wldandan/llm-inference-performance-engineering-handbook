#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / "chapters"


def main() -> int:
    failed = False
    count = 0
    for fig in sorted(CHAPTERS.glob("chapter*/figures/*")):
        if fig.name == ".gitkeep" or not fig.is_file():
            continue
        count += 1
        if fig.suffix.lower() not in {".svg", ".png", ".jpg", ".jpeg"}:
            print(f"{fig}: 不支持的插图格式")
            failed = True
        elif fig.stat().st_size == 0:
            print(f"{fig}: 文件为空")
            failed = True
    if failed:
        return 1
    print(f"OK: 已检查 {count} 个插图文件。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
