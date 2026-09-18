#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INSTALL="$REPO/install.sh"

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

root_auto="$(mktemp -d)"
mkdir "$root_auto/.cursor" "$root_auto/.claude"
touch "$root_auto/.codex"
"$INSTALL" grill-me --project "$root_auto" >/dev/null
[[ -f "$root_auto/.cursor/skills/grill-me/SKILL.md" ]] || fail "auto-detect did not write Cursor dest"
[[ -f "$root_auto/.claude/skills/grill-me/SKILL.md" ]] || fail "auto-detect did not write Claude dest"
[[ -f "$root_auto/.codex" ]] || fail "auto-detect removed a Codex file marker"
[[ ! -d "$root_auto/.codex" ]] || fail "auto-detect treated a Codex file as a dest"

root_force="$(mktemp -d)"
"$INSTALL" grill-me --project "$root_force" --codex >/dev/null
[[ -f "$root_force/.codex/skills/grill-me/SKILL.md" ]] || fail "override did not create Codex dest without marker"
[[ ! -e "$root_force/.cursor/skills" ]] || fail "override --codex also wrote Cursor dest"
[[ ! -e "$root_force/.claude/skills" ]] || fail "override --codex also wrote Claude dest"

root_empty="$(mktemp -d)"
set +e
empty_out="$("$INSTALL" grill-me --project "$root_empty" 2>&1)"
empty_st=$?
set -e
[[ "$empty_st" -ne 0 ]] || fail "no markers should exit non-zero"
[[ "$empty_out" == *"--cursor"* && "$empty_out" == *"--claude"* && "$empty_out" == *"--codex"* ]] || fail "empty error should name --cursor --claude --codex"

echo "OK"
