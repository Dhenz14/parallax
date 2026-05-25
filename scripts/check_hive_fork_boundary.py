#!/usr/bin/env python3
"""Verify the Hive fork-boundary note stays visible in Parallax docs."""
from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


REQUIRED = {
    "CLAUDE.md": [
        "Hive Ecosystem Fork Boundary",
        "Dhenz14/parallax",
        "upstream GradientHQ docs",
        "not itself the canonical Hive IDE",
    ],
    "README.md": [
        "Hive ecosystem fork boundary",
        "Dhenz14/parallax",
        "Gradient links, badges, Docker images",
        "Hive-specific capability and",
    ],
    "docs/user_guide/install.md": [
        "Hive operators working from the `Dhenz14/parallax` fork",
        "git clone https://github.com/Dhenz14/parallax.git",
        "upstream GradientHQ Parallax install paths",
        "git clone https://github.com/GradientHQ/parallax.git",
    ],
}


def main() -> int:
    missing: list[str] = []
    for rel, needles in REQUIRED.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                missing.append(f"{rel}: {needle}")

    if missing:
        for item in missing:
            print(f"missing fork-boundary text: {item}", file=sys.stderr)
        return 1

    print("PASS: Hive fork-boundary notes are present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
