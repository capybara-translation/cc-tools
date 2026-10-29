#!/usr/bin/env python3
"""Claude Code Stop hook: block replies that mention a GitHub issue/PR without a link.

Flags bare references such as `#123`, `owner/repo#123`, `PR 123` or `Issue #7`
in the last assistant message, ignoring code blocks, inline code, Markdown
links and URLs. When found, it blocks the stop once so Claude rewrites the
reference as a Markdown link to the full URL. It never blocks twice in a row
(stop_hook_active), so it cannot loop.
"""
import json
import re
import subprocess
import sys

FENCE = re.compile(r"```.*?```|~~~.*?~~~", re.S)
INLINE_CODE = re.compile(r"`[^`\n]*`")
MD_LINK = re.compile(r"\[[^\]\n]*\]\([^)\s]*\)")
URL = re.compile(r"https?://\S+")
BARE_REFS = [
    # #123 / owner/repo#123 (not part of a word, an HTML entity like &#123; or a URL fragment)
    re.compile(r"(?<![\w&/])(?:[\w.-]+/[\w.-]+)?#\d+\b"),
    # PR 123 / Issue #7 / issue 7 / pull request 12
    re.compile(r"\b(?:PR|[Ii]ssues?|[Pp]ull [Rr]equests?)\s*#?\d+\b"),
]


def last_message(data):
    msg = data.get("last_assistant_message")
    if isinstance(msg, str):
        return msg
    # Fallback for versions without last_assistant_message: read the transcript.
    path = data.get("transcript_path")
    if not path:
        return ""
    text = ""
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                except ValueError:
                    continue
                if entry.get("type") != "assistant":
                    continue
                content = (entry.get("message") or {}).get("content")
                if isinstance(content, list):
                    parts = [c.get("text", "") for c in content if c.get("type") == "text"]
                    if parts:
                        text = "\n".join(parts)
    except OSError:
        return ""
    return text


def find_bare_refs(text):
    for pattern in (FENCE, INLINE_CODE, MD_LINK, URL):
        text = pattern.sub(" ", text)
    found = []
    for pattern in BARE_REFS:
        for m in pattern.finditer(text):
            if m.group(0) not in found:
                found.append(m.group(0))
    return found


def repo_of(cwd):
    try:
        url = subprocess.run(
            ["git", "-C", cwd or ".", "remote", "get-url", "origin"],
            capture_output=True, text=True, timeout=5,
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None
    m = re.search(r"github\.com[:/]([\w.-]+/[\w.-]+?)(?:\.git)?$", url)
    return m.group(1) if m else None


def main():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return 0
    if data.get("stop_hook_active"):
        return 0  # already re-prompted once; do not loop
    refs = find_bare_refs(last_message(data))
    if not refs:
        return 0
    repo = repo_of(data.get("cwd"))
    hint = f" The current repository is {repo}." if repo else ""
    reason = (
        "Your last reply mentions GitHub issues/PRs without links: "
        + ", ".join(refs)
        + ". Per CLAUDE.md, give each as a Markdown link to its full URL "
        "(e.g. [owner/repo#123](https://github.com/owner/repo/issues/123))."
        + hint
        + " Briefly restate only the affected sentences with links; do not repeat the whole reply."
    )
    print(json.dumps({"decision": "block", "reason": reason}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
