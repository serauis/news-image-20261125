#!/usr/bin/env python3
"""news-image-20261125 entrypoint.

Copies the shipped front-page image to the output directory.
Deterministic: the same bytes are written on every run.
"""
import hashlib
import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    with open(src, "rb") as f:
        data = f.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG")
    if len(data) > 1048576:
        raise SystemExit("entry.png exceeds 1 MiB")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst, len(data), "bytes",
          "sha256", hashlib.sha256(data).hexdigest()[:16])


if __name__ == "__main__":
    sys.exit(main())
