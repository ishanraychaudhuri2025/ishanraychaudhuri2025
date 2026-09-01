#!/usr/bin/env python3
"""Merge projects.json with live GitHub metadata for the projects panel."""
import json, os, sys, urllib.request

TOKEN = os.environ.get("GITHUB_TOKEN", "")


def gh(url):
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {TOKEN}" if TOKEN else "",
            "User-Agent": "ishan-profile-projects",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.load(response)


def main():
    with open("projects.json", encoding="utf-8") as f:
        projects = json.load(f)

    for project in projects:
        repo = project["repo"].strip().replace("https://github.com/", "").replace("http://github.com/", "").rstrip("/")
        project["repo"] = repo
        try:
            info = gh(f"https://api.github.com/repos/{repo}")
            project["stars"] = info.get("stargazers_count", 0)
            project["forks"] = info.get("forks_count", 0)
            project["pushed_at"] = info.get("pushed_at")
            project["languages"] = gh(f"https://api.github.com/repos/{repo}/languages")
            if not project.get("description"):
                project["description"] = info.get("description") or ""
        except Exception as exc:
            print(f"warning: could not fetch {repo}: {exc}", file=sys.stderr)
            project.setdefault("stars", 0)
            project.setdefault("forks", 0)
            project.setdefault("pushed_at", None)
            project.setdefault("languages", {})

    with open("merged.json", "w", encoding="utf-8") as f:
        json.dump(projects, f, indent=2)

    print(f"merged {len(projects)} projects")


if __name__ == "__main__":
    main()
