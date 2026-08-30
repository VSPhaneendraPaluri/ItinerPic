"""Cleanup common Python temp directories in the workspace.

Usage:
  python tools/clean_temp.py [--prune] [--include NAME] [--dry-run]

Defaults remove: __pycache__, .venv, .pytest_cache and typo variants.
Use `--prune` to also include build/config directories such as `dist` and `config`.
Use `--include NAME` to add additional directory names to target (repeatable).
Use `--dry-run` to list targets without deleting.
"""
from pathlib import Path
import shutil
import argparse
from typing import List


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PATTERNS = ["__pycache__", ".venv", ".pytest_cache", ".pytest_chace"]
PRUNE_PATTERNS = ["dist", "config"]


def find_targets(root: Path, patterns: List[str]) -> List[Path]:
    targets: List[Path] = []
    for p in root.rglob("*"):
        if not p.is_dir():
            continue
        name = p.name
        # match by exact directory name
        if name in patterns:
            targets.append(p)
            continue
        # also match common venv folder names (endswith)
        for pat in patterns:
            if pat and pat.startswith('.') is False and pat in name:
                targets.append(p)
                break
    # dedupe and sort for stable output
    unique = sorted({t.resolve() for t in targets}, key=lambda p: str(p))
    return unique


def remove_path(p: Path) -> None:
    try:
        shutil.rmtree(p)
        print(f"Removed: {p}")
    except Exception as e:
        print(f"Failed to remove {p}: {e}")


def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Cleanup common temp directories")
    parser.add_argument("--prune", action="store_true", help="Also remove build/config dirs (dist, config)")
    parser.add_argument(
        "--include",
        "-i",
        action="append",
        default=[],
        help="Additional directory names to remove (repeatable)",
    )
    parser.add_argument("--dry-run", action="store_true", help="List targets without deleting")
    args = parser.parse_args(argv)

    patterns = list(DEFAULT_PATTERNS)
    if args.prune:
        patterns += PRUNE_PATTERNS
    if args.include:
        patterns += args.include

    targets = find_targets(ROOT, patterns)
    if not targets:
        print("No temp directories found.")
        return

    print(f"Found {len(targets)} target(s):")
    for t in targets:
        print(f"  - {t}")

    if args.dry_run:
        print("Dry-run mode; no changes made.")
        return

    print("Removing targets...")
    for t in targets:
        remove_path(t)


if __name__ == "__main__":
    main()
