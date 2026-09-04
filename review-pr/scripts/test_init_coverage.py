#!/usr/bin/env python3
"""Public-contract tests for init_coverage.py hunk inventory."""
from __future__ import annotations

import unittest

from init_coverage import parse_diff, render


ADD_ONLY = """diff --git a/new.py b/new.py
new file mode 100644
index 0000000..1111111
--- /dev/null
+++ b/new.py
@@ -0,0 +1,3 @@
+a
+b
+c
"""

DELETE_ONLY = """diff --git a/old.py b/old.py
deleted file mode 100644
index 1111111..0000000
--- a/old.py
+++ /dev/null
@@ -1,3 +0,0 @@
-a
-b
-c
"""

MIXED = """diff --git a/x.py b/x.py
index 1111111..2222222 100644
--- a/x.py
+++ b/x.py
@@ -10,4 +10,5 @@
 context
-old
+new
+added
 context
"""

RENAME_WITH_HUNKS = """diff --git a/old.py b/new.py
similarity index 80%
rename from old.py
rename to new.py
--- a/old.py
+++ b/new.py
@@ -1,3 +1,3 @@
 a
-b
+c
 d
"""

RENAME_ONLY = """diff --git a/old.py b/new.py
similarity index 100%
rename from old.py
rename to new.py
"""


def _frontmatter(md: str) -> dict[str, str]:
    body = md.split("---", 2)[1]
    out: dict[str, str] = {}
    for line in body.strip().splitlines():
        k, _, v = line.partition(":")
        out[k.strip()] = v.strip()
    return out


class InitCoverageTests(unittest.TestCase):
    def test_addition_only_reports_added_hunks(self) -> None:
        files = parse_diff(ADD_ONLY)
        md = render(files, "abc")
        fm = _frontmatter(md)
        self.assertEqual(fm["changed_hunks"], "1")
        self.assertEqual(fm["added_lines"], "3")
        self.assertEqual(fm["deleted_lines"], "0")
        self.assertIn("| new.py | `-0,0 +1,3` | 3 | 0 | 1 |", md)
        self.assertNotIn("total_changed_lines", md)

    def test_deletion_only_file_is_not_omitted(self) -> None:
        files = parse_diff(DELETE_ONLY)
        md = render(files, "abc")
        fm = _frontmatter(md)
        self.assertEqual(fm["changed_hunks"], "1")
        self.assertEqual(fm["added_lines"], "0")
        self.assertEqual(fm["deleted_lines"], "3")
        self.assertIn("| old.py | `-1,3 +0,0` | 0 | 3 | 1 |", md)

    def test_mixed_hunk_reports_both_counts(self) -> None:
        files = parse_diff(MIXED)
        md = render(files, "abc")
        fm = _frontmatter(md)
        self.assertEqual(fm["changed_hunks"], "1")
        self.assertEqual(fm["added_lines"], "2")
        self.assertEqual(fm["deleted_lines"], "1")
        self.assertIn("| x.py | `-10,4 +10,5` | 2 | 1 | 1 |", md)

    def test_rename_with_hunks_uses_new_path(self) -> None:
        files = parse_diff(RENAME_WITH_HUNKS)
        md = render(files, "abc")
        fm = _frontmatter(md)
        self.assertEqual(fm["changed_hunks"], "1")
        self.assertEqual(fm["added_lines"], "1")
        self.assertEqual(fm["deleted_lines"], "1")
        self.assertIn("| new.py | `-1,3 +1,3` | 1 | 1 | 1 |", md)
        self.assertNotIn("| old.py |", md)

    def test_rename_only_emits_one_row(self) -> None:
        files = parse_diff(RENAME_ONLY)
        md = render(files, "abc")
        fm = _frontmatter(md)
        self.assertEqual(fm["changed_hunks"], "1")
        self.assertEqual(fm["added_lines"], "0")
        self.assertEqual(fm["deleted_lines"], "0")
        self.assertEqual(md.count("| new.py | `rename` | 0 | 0 | 1 |"), 1)


if __name__ == "__main__":
    unittest.main()
