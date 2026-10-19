"""Create a portable SHA-256 manifest for an external data or model release."""

import argparse
import hashlib
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path, help="release directory to inventory")
    parser.add_argument("--output", type=Path, default=Path("SHA256SUMS"))
    args = parser.parse_args()

    root = args.directory.resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")

    files = sorted(path for path in root.rglob("*") if path.is_file())
    with args.output.open("w", encoding="utf-8", newline="\n") as manifest:
        for path in files:
            manifest.write(f"{sha256(path)}  {path.relative_to(root).as_posix()}\n")


if __name__ == "__main__":
    main()
