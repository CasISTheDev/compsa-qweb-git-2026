#!/usr/bin/env python3
"""Reads members/*.md. `--check` validates them (the PR check); otherwise prints members.json for the wall."""
import json, pathlib, re, sys

FIELDS = ("name", "program", "fun")
DIR = pathlib.Path(__file__).resolve().parent.parent / "members"


def parse(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\s*$", text, re.S)
    if not m:
        return None, "needs a --- line before and after the three fields"
    data = dict(line.split(":", 1) for line in m.group(1).splitlines() if ":" in line)
    data = {k.strip(): v.strip() for k, v in data.items()}
    missing = [f for f in FIELDS if not data.get(f)]
    if missing:
        return None, "fill in: " + ", ".join(missing)
    if any(len(data[f]) > 80 for f in FIELDS):
        return None, "keep each line under 80 characters"
    return {"user": path.stem, **{f: data[f] for f in FIELDS}}, None


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
