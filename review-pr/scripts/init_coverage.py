#!/usr/bin/env python3
"""Build a COVERAGE.md inventory from a unified diff on stdin.

Each inventory row is one changed diff hunk (or a rename-only / binary file).
Usage:
  gh pr diff <n> | python3 scripts/init_coverage.py --head-sha SHA > COVERAGE.md
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field


_HUNK_RE = re.compile(
    r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@"
)
_DIFF_GIT_RE = re.compile(r"^diff --git (?:a/)?(\S+) (?:b/)?(\S+)\s*$")


@dataclass
class Hunk:
    path: str
    spec: str
    added: int
    deleted: int
    kind: str = "hunk"  # hunk | rename | binary


@dataclass
class FileDiff:
    path: str
    old_path: str
    rename: bool = False
    binary: bool = False
    hunks: list[Hunk] = field(default_factory=list)


def _unprefix(path: str) -> str:
    if path.startswith("a/") or path.startswith("b/"):
        return path[2:]
    return path


def parse_diff(text: str) -> list[FileDiff]:
    files: list[FileDiff] = []
    current: FileDiff | None = None
    hunk: Hunk | None = None

    def finish_file() -> None:
        nonlocal current
        if current is None:
            return
        if current.binary:
            current.hunks = [
                Hunk(path=current.path, spec="binary", added=0, deleted=0, kind="binary")
            ]
        elif current.rename and not current.hunks:
            current.hunks = [
                Hunk(path=current.path, spec="rename", added=0, deleted=0, kind="rename")
            ]
        files.append(current)
        current = None

    for raw in text.splitlines():
        if raw.startswith("diff --git "):
            finish_file()
            m = _DIFF_GIT_RE.match(raw)
            if m:
                old_p, new_p = m.group(1), m.group(2)
            else:
                parts = raw.split()
                old_p = _unprefix(parts[2]) if len(parts) > 2 else "unknown"
                new_p = _unprefix(parts[3]) if len(parts) > 3 else old_p
            path = new_p if new_p != "/dev/null" else old_p
            current = FileDiff(path=path, old_path=old_p)
            hunk = None
            continue
        if current is None:
            continue
        if raw.startswith("rename from "):
            current.rename = True
            current.old_path = raw[len("rename from ") :].strip()
            continue
        if raw.startswith("rename to "):
            current.rename = True
            current.path = raw[len("rename to ") :].strip()
            continue
        if raw.startswith("GIT binary patch") or raw.startswith("Binary files "):
            current.binary = True
            hunk = None
            continue
        if raw.startswith("--- "):
            p = raw[4:].strip()
            if p != "/dev/null":
                current.old_path = _unprefix(p)
                if current.path in ("", "/dev/null"):
                    current.path = current.old_path
            continue
        if raw.startswith("+++ "):
            p = raw[4:].strip()
            if p == "/dev/null":
                current.path = current.old_path
            else:
                current.path = _unprefix(p)
            continue
        if current.binary:
            continue
        hm = _HUNK_RE.match(raw)
        if hm:
            old_start, old_count, new_start, new_count = hm.group(1, 2, 3, 4)
            old_c = 1 if old_count is None else int(old_count)
            new_c = 1 if new_count is None else int(new_count)
            spec = f"-{old_start},{old_c} +{new_start},{new_c}"
            hunk = Hunk(path=current.path, spec=spec, added=0, deleted=0)
            current.hunks.append(hunk)
            continue
        if hunk is None:
            continue
        if raw.startswith("+") and not raw.startswith("+++"):
            hunk.added += 1
        elif raw.startswith("-") and not raw.startswith("---"):
            hunk.deleted += 1
        elif raw.startswith("\\"):
            continue
    finish_file()
    return files


def render(files: list[FileDiff], head_sha: str) -> str:
    rows: list[Hunk] = []
    na = 0
    added_lines = 0
    deleted_lines = 0
    for f in files:
        for h in f.hunks:
            if h.kind == "binary":
                na += 1
                rows.append(h)
                continue
            h.path = f.path
            added_lines += h.added
            deleted_lines += h.deleted
            rows.append(h)

    changed = sum(1 for h in rows if h.kind != "binary")

    lines = [
        "---",
        f"head_sha: {head_sha}",
        f"changed_hunks: {changed}",
        f"added_lines: {added_lines}",
        f"deleted_lines: {deleted_lines}",
        "human_presented: 0",
        "agent_reviewed_not_shown: 0",
        "not_reviewed: " + str(changed),
        f"not_applicable: {na}",
        "---",
        "",
        "# Coverage",
        "",
        "Unit: one row per changed hunk (rename-only files are one row). "
        "`human_presented` means the exact changed product code was shown in chat; "
        "it does not mean a human reviewed or understood those lines.",
        "",
        "Status: `not_reviewed` | `human_presented` | `agent_reviewed_not_shown` | `not_applicable`",
        "",
        "| path | hunk | + | - | count | status | reason | shown_in |",
        "| --- | --- | ---: | ---: | ---: | --- | --- | --- |",
    ]
    for h in rows:
        if h.kind == "binary":
            lines.append(
                f"| {h.path} | binary | 0 | 0 | 0 | not_applicable | binary | |"
            )
        else:
            lines.append(
                f"| {h.path} | `{h.spec}` | {h.added} | {h.deleted} | 1 | not_reviewed | | |"
            )
    lines.append("")
    lines.append("## Totals")
    lines.append("")
    lines.append("Percents use `changed_hunks` as the denominator (exclude `not_applicable`).")
    lines.append("")
    lines.append("| status | hunks | pct |")
    lines.append("| --- | ---: | ---: |")
    lines.append("| human_presented | 0 | 0% |")
    lines.append("| agent_reviewed_not_shown | 0 | 0% |")
    lines.append(f"| not_reviewed | {changed} | {100 if changed else 0}% |")
    lines.append(f"| not_applicable | {na} | — |")
    lines.append("")
    lines.append("## Human oversight")
    lines.append("")
    lines.append("Separate from presentation counts. Record only explicit user decisions:")
    lines.append("")
    lines.append("- claims confirmed:")
    lines.append("- architecture/boundary decisions reviewed:")
    lines.append("- findings approved/rejected/edited:")
    lines.append("- unresolved business questions answered:")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--head-sha", default="unknown")
    args = p.parse_args()
    sys.stdout.write(render(parse_diff(sys.stdin.read()), args.head_sha))


if __name__ == "__main__":
    main()
