#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  cat <<EOF
Usage: ./install.sh [skill...] [--project [dir]]

Copy skills from this repo into Cursor.

  (no args)              active skills (not old/) → ~/.cursor/skills/
  skill ...              those skills only (old/ allowed by name)
  --project              → \$PWD/.cursor/skills/
  --project DIR          → DIR/.cursor/skills/

Re-run after git pull to update. Does not remove other installed skills.
EOF
}

is_project_dir_arg() {
  local arg="$1"
  [[ "$arg" == . || "$arg" == .. || "$arg" == ~* || "$arg" == /* || "$arg" == ./* || "$arg" == ../* ]] && return 0
  [[ "$arg" == */* ]] && return 0
  [[ -d "$arg" ]] && return 0
  return 1
}

project_mode=0
project_dir=""
skills=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    --project=*)
      project_mode=1
      project_dir="${1#--project=}"
      shift
      ;;
    --project)
      project_mode=1
      if [[ $# -gt 1 && "$2" != -* ]] && is_project_dir_arg "$2"; then
        project_dir="$2"
        shift 2
      else
        shift
      fi
      ;;
    -*)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
    *)
      skills+=("$1")
      shift
      ;;
  esac
done

if [[ "$project_mode" -eq 1 ]]; then
  [[ -n "$project_dir" ]] || project_dir="$PWD"
  if [[ ! -d "$project_dir" ]]; then
    echo "Project directory does not exist: $project_dir" >&2
    exit 1
  fi
  project_dir="$(cd "$project_dir" && pwd)"
  dest="$project_dir/.cursor/skills"
else
  dest="${HOME}/.cursor/skills"
fi

default_skills() {
  local d name
  for d in "$ROOT"/*/; do
    name="$(basename "$d")"
    [[ "$name" == "old" ]] && continue
    [[ -f "$d/SKILL.md" ]] && printf '%s\n' "$name"
  done | sort
}

resolve_skill() {
  local name="$1"
  if [[ -f "$ROOT/$name/SKILL.md" ]]; then
    printf '%s\n' "$ROOT/$name"
  elif [[ -f "$ROOT/old/$name/SKILL.md" ]]; then
    printf '%s\n' "$ROOT/old/$name"
  else
    return 1
  fi
}

if [[ ${#skills[@]} -eq 0 ]]; then
  skills=()
  while IFS= read -r _name; do
    skills+=("$_name")
  done < <(default_skills)
fi

if [[ ${#skills[@]} -eq 0 ]]; then
  echo "No skills to install." >&2
  exit 1
fi

mkdir -p "$dest"

installed=()
for name in "${skills[@]}"; do
  src="$(resolve_skill "$name")" || {
    echo "Unknown skill: $name" >&2
    exit 1
  }
  rm -rf "$dest/$name"
  cp -R "$src" "$dest/$name"
  installed+=("$name")
done

echo "Installed ${#installed[@]} skill(s) → $dest"
printf '  %s\n' "${installed[@]}"
