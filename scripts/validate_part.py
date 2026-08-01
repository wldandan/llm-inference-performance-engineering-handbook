#!/usr/bin/env python3
"""Validate textbook part/chapter structure for this repository."""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


PART_CHAPTERS = {
    1: range(1, 5),
    2: range(5, 9),
    3: range(9, 13),
    4: range(13, 17),
    5: range(17, 21),
    6: range(21, 25),
    7: range(25, 30),
}

REQUIRED_TEMPLATE_A_MARKERS = [
    "学习目标",
    "核心问题",
    "Demo",
    "本章总结",
]

IMAGE_RE = re.compile(r"!\[[^\]]*]\((figures/[^)]+\.svg)\)")
CAPTION_RE = re.compile(r"图(\d+)-(\d+)[：:]")
SECTION_RE = re.compile(r"^##\s+\d+\.\d+\s+", re.MULTILINE)


def chapter_dir(root: Path, chapter: int) -> Path:
    return root / f"chapter{chapter:02d}"


def validate_svg(path: Path, errors: list[str]) -> None:
    try:
        ET.parse(path)
    except ET.ParseError as exc:
        errors.append(f"{path}: invalid SVG XML: {exc}")


def validate_chapter(root: Path, chapter: int) -> list[str]:
    errors: list[str] = []
    chapter_path = chapter_dir(root, chapter)
    chapter_file = chapter_path / f"chapter{chapter:02d}.md"
    review_file = chapter_path / "review.md"
    storyboard_file = chapter_path / "storyboard.md"
    figures_dir = chapter_path / "figures"

    if not chapter_path.is_dir():
        return [f"{chapter_path}: missing chapter directory"]

    for required in [chapter_file, review_file, storyboard_file, figures_dir]:
        if not required.exists():
            errors.append(f"{required}: missing")

    if not chapter_file.exists():
        return errors

    text = chapter_file.read_text(encoding="utf-8")

    for marker in REQUIRED_TEMPLATE_A_MARKERS:
        if marker not in text:
            errors.append(f"{chapter_file}: missing Template A marker `{marker}`")

    if len(SECTION_RE.findall(text)) < 6:
        errors.append(f"{chapter_file}: expected at least 6 numbered content sections")

    for marker in ["课堂案例", "补充案例 A", "补充案例 B"]:
        if marker not in text:
            errors.append(f"{chapter_file}: missing teaching case marker `{marker}`")

    image_links = IMAGE_RE.findall(text)
    if len(image_links) != 10:
        errors.append(f"{chapter_file}: expected 10 SVG image links, found {len(image_links)}")

    for link in image_links:
        target = chapter_path / link
        if not target.exists():
            errors.append(f"{chapter_file}: missing image target {link}")
        else:
            validate_svg(target, errors)

    captions = [(int(ch), int(idx)) for ch, idx in CAPTION_RE.findall(text)]
    own_captions = [idx for ch, idx in captions if ch == chapter]
    expected = list(range(1, 11))
    if own_captions != expected:
        errors.append(
            f"{chapter_file}: expected captions 图{chapter}-1..图{chapter}-10, "
            f"found {own_captions}"
        )

    if figures_dir.exists():
        svgs = sorted(figures_dir.glob(f"fig{chapter:02d}-*.svg"))
        if len(svgs) != 10:
            errors.append(f"{figures_dir}: expected 10 SVG files, found {len(svgs)}")
        for svg in svgs:
            validate_svg(svg, errors)

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--part", type=int, help="Part number to validate, 1-7")
    parser.add_argument("--chapter", type=int, help="Single chapter number to validate")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path.cwd()

    if args.chapter:
        chapters = [args.chapter]
        part_numbers: list[int] = []
    elif args.part:
        if args.part not in PART_CHAPTERS:
            print(f"Unknown part: {args.part}", file=sys.stderr)
            return 2
        chapters = list(PART_CHAPTERS[args.part])
        part_numbers = [args.part]
    else:
        print("Use --part N or --chapter N", file=sys.stderr)
        return 2

    errors: list[str] = []
    for part in part_numbers:
        part_file = root / f"part{part:02d}.md"
        if not part_file.exists():
            errors.append(f"{part_file}: missing Part introduction")

    for chapter in chapters:
        errors.extend(validate_chapter(root, chapter))

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    target = f"part {args.part}" if args.part else f"chapter {args.chapter}"
    print(f"Validation passed for {target}: {len(chapters)} chapter(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
