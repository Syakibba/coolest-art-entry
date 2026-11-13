#!/usr/bin/env python3
"""Writes the entry image (bundled in this repository) to /output/entry.png."""
import os, shutil

INPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "art.png")
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    shutil.copyfile(INPUT, os.path.join(OUTPUT_DIR, "entry.png"))

if __name__ == "__main__":
    main()
