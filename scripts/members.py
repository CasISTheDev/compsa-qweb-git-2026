#!/usr/bin/env python3
"""Reads members/*.md. `--check` validates them all; otherwise prints members.json for the wall.
The pull request check (scripts/check_pr.py) uses parse() so both read files the same way."""
import json, pathlib, re, sys

FIELDS = ("name", "program", "fun")
# What _template.md says. A file that still says this hasn't been filled in.
TEMPLATE = {"name": "your name", "program": "e.g. computing, 2nd year", "fun": "one thing you're into right now"}
DIR = pathlib.Path(__file__).resolve().parent.parent / "members"


def parse_text(text):
    """Return (data, None) if the file is good, or (None, a plain-English fix) if not."""
    text = text.replace("\r\n", "\n").lstrip("﻿")
    m = re.match(r"^---\n(.*?)\n---\s*$", text, re.S)
    if not m:
        return None, "needs a --- line before and after the three fields, like the template"
    data = dict(line.split(":", 1) for line in m.group(1).splitlines() if ":" in line)
    data = {k.strip().lower(): v.strip() for k, v in data.items()}
    missing = [f for f in FIELDS if not data.get(f)]
    if missing:
        return None, "fill in: " + ", ".join(missing)
    same = [f for f in FIELDS if data[f].lower() == TEMPLATE[f]]
    if same:
        return None, "still has the template text in: " + ", ".join(same) + ". Replace it with your own"
    if any(len(data[f]) > 80 for f in FIELDS):
        return None, "keep each line under 80 characters"
    return {f: data[f] for f in FIELDS}, None


def parse(path):
    data, err = parse_text(path.read_text(encoding="utf-8", errors="replace"))
    return ({"user": path.stem, **data} if data else None), err


def members():
    return [p for p in sorted(DIR.glob("*.md")) if not p.name.startswith("_")]


if __name__ == "__main__":
    if "--check" in sys.argv:
        bad = [(p.name, err) for p in members() for _, err in [parse(p)] if err]
        for name, err in bad:
            print(f"members/{name}: {err}")
        print("All member files look good." if not bad else f"{len(bad)} file(s) to fix.")
        sys.exit(1 if bad else 0)
    print(json.dumps([m for p in members() for m, _ in [parse(p)] if m], indent=1))
