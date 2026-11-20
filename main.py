#!/usr/bin/env python3
"""Entry program for THE WORLD WIRE, 20 November 2026 edition.

The poster itself ships in this repository as ``entry.png`` (drawn by
``build/poster.py``). This program's whole job is to place those exact
bytes at ``/output/entry.png`` so the judge sees the front page just as
it was typeset — same file, every run, no network, no randomness.
"""

import hashlib
import os
import shutil
import sys

POSTER_NAME = "entry.png"
OUTPUT_DIR = "/output"


def poster_path():
    """The poster lives beside this script, wherever the repo is checked out."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, POSTER_NAME)


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    src = poster_path()
    if not os.path.isfile(src):
        print(f"poster missing: {src}", file=sys.stderr)
        return 1
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    dest = os.path.join(OUTPUT_DIR, POSTER_NAME)
    shutil.copyfile(src, dest)
    if digest(src) != digest(dest):
        print("copy drifted: output bytes differ from the poster", file=sys.stderr)
        return 2
    print(f"wrote {dest} ({os.path.getsize(dest)} bytes, sha256 {digest(dest)[:16]}…)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
