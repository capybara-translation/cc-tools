#!/bin/sh
input=$(cat)
cwd=$(echo "$input" | jq -r '.workspace.current_dir')
project_dir=$(echo "$input" | jq -r '.workspace.project_dir')
model=$(echo "$input" | jq -r '.model.display_name // empty')
used_pct=$(echo "$input" | jq -r '.context_window.used_percentage // empty')

# Shorten paths by replacing $HOME with ~
home="$HOME"
cwd_display="${cwd/#$home/~}"
project_display="${project_dir/#$home/~}"

# Get git branch (skip optional locks to avoid contention)
branch=$(git -C "$cwd" --no-optional-locks branch --show-current 2>/dev/null)

# Line 1: path and branch
line1="cwd: ${cwd_display}  |  project: ${project_display}"
if [ -n "$branch" ]; then
    line1="${line1}  |  branch: ${branch}"
fi

# Line 2: model and context usage
line2=""
if [ -n "$model" ]; then
    line2="${model}"
fi
if [ -n "$used_pct" ]; then
    used_int=$(printf '%.0f' "$used_pct")
    if [ -n "$line2" ]; then
        line2="${line2}  |  ctx: ${used_int}%"
    else
        line2="ctx: ${used_int}%"
    fi
fi

echo "$line1"
if [ -n "$line2" ]; then
    echo "$line2"
fi
