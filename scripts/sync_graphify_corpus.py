from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT_FILES = [
    "map-widget.html",
    "seat-results-widget.html",
    "key-battles-widget.html",
]

ROOT_DIRS = [
    "iframe embeds",
]


def copy_file(src: Path, dst: Path, dry_run: bool) -> None:
    if dry_run:
        print(f"COPY {src} -> {dst}")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def mirror_dir(src_dir: Path, dst_dir: Path, dry_run: bool) -> None:
    if dry_run:
        print(f"MIRROR {src_dir} -> {dst_dir}")
        return

    dst_dir.mkdir(parents=True, exist_ok=True)

    src_paths = {path.relative_to(src_dir) for path in src_dir.rglob("*")}

    for existing in sorted(
        dst_dir.rglob("*"),
        key=lambda path: len(path.relative_to(dst_dir).parts),
        reverse=True,
    ):
        rel = existing.relative_to(dst_dir)
        if rel not in src_paths:
            if existing.is_dir():
                shutil.rmtree(existing)
            else:
                existing.unlink()

    for path in src_dir.rglob("*"):
        rel = path.relative_to(src_dir)
        target = dst_dir / rel
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Mirror canonical widget/embed files into graphify-corpus/."
    )
    parser.add_argument("--dry-run", action="store_true", help="Print planned actions without copying")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    corpus_root = repo_root / "graphify-corpus"

    if not corpus_root.exists():
        raise SystemExit(f"Missing graphify-corpus directory: {corpus_root}")

    copied = 0
    for rel_path in ROOT_FILES:
        src = repo_root / rel_path
        dst = corpus_root / rel_path
        if not src.exists():
            raise SystemExit(f"Missing source file: {src}")
        copy_file(src, dst, args.dry_run)
        copied += 1

    for rel_dir in ROOT_DIRS:
        src_dir = repo_root / rel_dir
        dst_dir = corpus_root / rel_dir
        if not src_dir.exists():
            raise SystemExit(f"Missing source directory: {src_dir}")
        mirror_dir(src_dir, dst_dir, args.dry_run)

    if args.dry_run:
        print("Dry run complete.")
    else:
        print(f"Synchronized {copied} files and {len(ROOT_DIRS)} directories into graphify-corpus/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
