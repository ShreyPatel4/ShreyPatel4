#!/usr/bin/env python3
"""Refresh the "Recent pushes" block in README.md.

One block, one job. If anything goes wrong the block is left exactly as it was,
because a stale line reads better on a public profile than a placeholder that
says the automation is broken.
"""

import os
import re
import sys
import urllib.request
import urllib.error
import json

README = "README.md"
START = "<!-- ACTIVITY_START -->"
END = "<!-- ACTIVITY_END -->"
USER = os.environ.get("REPO_OWNER", "ShreyPatel4")
LIMIT = 6

# Repos that exist only to hold this profile, or that are someone else's work.
SKIP = {USER}


def api(path):
    req = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "profile-readme-updater",
            **(
                {"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"}
                if os.environ.get("GITHUB_TOKEN")
                else {}
            ),
        },
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def recent_pushes():
    """One row per repo, newest push first.

    The public events feed no longer inlines commit messages (payload.commits
    comes back null), so take the head sha from the event and resolve it.
    """
    rows, seen = [], set()
    for ev in api(f"/users/{USER}/events/public?per_page=100"):
        if ev.get("type") != "PushEvent":
            continue
        repo = ev["repo"]["name"]
        if repo in seen or repo.split("/")[-1] in SKIP:
            continue
        head = ev["payload"].get("head")
        if not head:
            continue
        try:
            msg = api(f"/repos/{repo}/commits/{head}")["commit"]["message"]
        except (urllib.error.URLError, KeyError, ValueError):
            continue
        msg = msg.splitlines()[0].strip()
        if len(msg) > 68:
            msg = msg[:67].rstrip() + "…"
        seen.add(repo)
        rows.append((repo, msg, ev["created_at"][:10]))
        if len(rows) >= LIMIT:
            break
    return rows


def render(rows):
    if not rows:
        return None
    out = ["| Repo | Last commit | When |", "| :-- | :-- | :-- |"]
    for repo, msg, when in rows:
        name = repo.split("/")[-1]
        safe = msg.replace("|", "\\|")
        out.append(f"| [{name}](https://github.com/{repo}) | {safe} | {when} |")
    return "\n".join(out)


def main():
    try:
        block = render(recent_pushes())
    except (urllib.error.URLError, KeyError, ValueError) as exc:
        print(f"skipping refresh: {exc}", file=sys.stderr)
        return 0

    if not block:
        print("no public pushes found, leaving block alone", file=sys.stderr)
        return 0

    text = open(README, encoding="utf-8").read()
    pattern = re.compile(
        re.escape(START) + r".*?" + re.escape(END), re.S
    )
    if not pattern.search(text):
        print("activity markers missing, nothing to do", file=sys.stderr)
        return 0

    updated = pattern.sub(f"{START}\n\n{block}\n\n{END}", text)
    if updated != text:
        open(README, "w", encoding="utf-8").write(updated)
        print("README updated")
    else:
        print("no change")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
