#!/usr/bin/env python3
"""The pull request check. Looks only at what this pull request changes:
one new file, members/<your-github-username>.md, filled in, and nothing else touched.
Says what to fix in plain English, in the log, on the file in "Files changed", and on the summary page."""
import os, pathlib, subprocess, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from members import parse_text  # noqa: E402

EXAMPLE = "---\nname: Ada Lovelace\nprogram: Computing, 2nd year\nfun: building a site for my band\n---"


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def main():
    base, head = os.environ["BASE_SHA"], os.environ["HEAD_SHA"]
    login = os.environ["PR_AUTHOR"].lower()
    want = f"members/{login}.md"
    errors = []  # (file or None, message)

    added = []
    for row in git("diff", "--name-status", "--no-renames", f"{base}...{head}").splitlines():
        status, path = row.split("\t", 1)
        if status == "A" and path.startswith("members/"):
            added.append(path)
        elif path.startswith("members/"):
            verb = "edited" if status == "M" else "deleted"
            errors.append((path, f"You {verb} {path}, which isn't yours. Put it back, so this pull request only adds your own file."))
        else:
            errors.append((path, f"You changed {path}. This pull request should only add your one file in members/. Undo that change, commit, and push again."))

    if not added:
        errors.append((None, f"There's no new file in members/. Add {want}, commit, and push again."))
    elif len(added) > 1:
        errors.append((None, "You added more than one file in members/: " + ", ".join(added) + f". Keep only {want}."))

    for path in added:
        if path.lower() != want:
            errors.append((path, f"Name your file {want} (your GitHub username, then .md). Yours is {path}."))
        try:
            text = git("show", f"{head}:{path}")
        except (subprocess.CalledProcessError, UnicodeDecodeError):
            errors.append((path, "Git can't read this file as plain text. Copy the template again and fill it in."))
            continue
        _, err = parse_text(text)
        if err:
            errors.append((path, f"{path} {err}."))

    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if errors:
        print("Almost there. Fix this, then git add, git commit, git push. The check runs again on its own.\n")
        for f, msg in errors:
            print("  - " + msg)
            print(f"::error {'file=' + f + ',' if f else ''}title=Fix this::{msg}")
        print(f"\nYour file is {want} and should look like this:\n\n{EXAMPLE}")
        if summary:
            with open(summary, "a") as s:
                s.write("## Almost there\n\nFix this, then `git add`, `git commit`, `git push`. The check runs again on its own.\n\n")
                s.writelines(f"- {msg}\n" for _, msg in errors)
                s.write(f"\nYour file is `{want}` and should look like this:\n\n```\n{EXAMPLE}\n```\n")
        sys.exit(1)

    print("Looks good. Once a QWeb exec merges this, you're on the wall.")
    if summary:
        with open(summary, "a") as s:
            s.write("## Looks good\n\nOnce a QWeb exec merges this, you're on the wall.\n")


if __name__ == "__main__":
    main()
