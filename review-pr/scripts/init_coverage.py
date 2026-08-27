#!/usr/bin/env python3
"""Build a COVERAGE.md inventory from a unified diff on stdin.

Counts new-file (+) line numbers only. Binary / empty patches are skipped.
Usage:
  gh pr diff <n> | python3 scripts/init_coverage.py --head-sha SHA > COVERAGE.md
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field


@dataclass
class FileCov:
    path: str
    added: list[int] = field(default_factory=list)
    binary: bool = False


def parse_diff(text: str) -> list[FileCov]:
    files: list[FileCov] = []
    current: FileCov | None = None
    new_line = 0
    for raw in text.splitlines():
        if raw.startswith("diff --git "):
            current = None
            continue
        if raw.startswith("+++ "):
            path = raw[4:].strip()
            if path.startswith("b/"):
                path = path[2:]
            if path == "/dev/null":
                current = None
                continue
            current = FileCov(path=path)
            files.append(current)
            continue
        if raw.startswith("GIT binary patch") or raw.startswith("Binary files "):
            if current is not None:
                current.binary = True
            continue
        if current is None or current.binary:
            continue
        if raw.startswith("@@"):
            # @@ -old,count +new,count @@
            plus = raw.split("@@")[1].strip().split(" ")
            new_hunk = next(p for p in plus if p.startswith("+"))
            start = new_hunk[1:].split(",")[0]
            new_line = int(start)
            continue
        if raw.startswith("+") and not raw.startswith("+++"):
            current.added.append(new_line)
            new_line += 1
        elif raw.startswith("-") and not raw.startswith("---"):
            continue
        else:
            # context or other
            if raw.startswith("\\"):
                continue
            new_line += 1
    return files


def ranges(nums: list[int]) -> list[str]:
    if not nums:
        return []
    nums = sorted(set(nums))
    out: list[str] = []
    start = prev = nums[0]
    for n in nums[1:]:
        if n == prev + 1:
            prev = n
            continue
        out.append(f"{start}" if start == prev else f"{start}-{prev}")
        start = prev = n
    out.append(f"{start}" if start == prev else f"{start}-{prev}")
    return out


def render(files: list[FileCov], head_sha: str) -> str:
    rows: list[tuple[str, str, int]] = []
    total = 0
    na = 0
    for f in files:
        if f.binary or not f.added:
            if f.binary:
                na += 1
                rows.append((f.path, "binary", 0))
            continue
        for r in ranges(f.added):
            if "-" in r:
                a, b = r.split("-")
                count = int(b) - int(a) + 1
            else:
                count = 1
            total += count
            rows.append((f.path, r, count))

    lines = [
        "---",
        f"head_sha: {head_sha}",
        f"total_changed_lines: {total}",
        "human_presented: 0",
        "agent_reviewed_not_shown: 0",
        "not_reviewed: " + str(total),
        f"not_applicable: {na}",
        "---",
        "",
        "# Coverage",
        "",
        "Status: `not_reviewed` | `human_presented` | `agent_reviewed_not_shown` | `not_applicable`",
        "",
        "| path | lines | count | status | reason | shown_in |",
        "| --- | --- | ---: | --- | --- | --- |",
    ]
    for path, rng, count in rows:
        if rng == "binary":
            lines.append(f"| {path} | — | 0 | not_applicable | binary | |")
        else:
            lines.append(f"| {path} | {rng} | {count} | not_reviewed | | |")
    lines.append("")
    lines.append("## Totals")
    lines.append("")
    lines.append("| status | lines | pct |")
    lines.append("| --- | ---: | ---: |")
    lines.append(f"| human_presented | 0 | 0% |")
    lines.append(f"| agent_reviewed_not_shown | 0 | 0% |")
    lines.append(f"| not_reviewed | {total} | 100% |")
    lines.append(f"| not_applicable | {na} | — |")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--head-sha", default="unknown")
    args = p.parse_args()
    text = sys.stdin.read()
    sys.stdout.write(render(parse_diff(text), args.head_sha))


if __name__ == "__main__":
    main()
