#!/bin/sh
input=$(cat)
cwd=$(echo "$input" | jq -r '.workspace.current_dir')
project_dir=$(echo "$input" | jq -r '.workspace.project_dir')
session_id=$(echo "$input" | jq -r '.session_id // empty')
model=$(echo "$input" | jq -r '.model.display_name // empty')
used_pct=$(echo "$input" | jq -r '.context_window.used_percentage // empty')

# Shorten paths by replacing $HOME with ~
home="$HOME"
cwd_display="${cwd/#$home/~}"
project_display="${project_dir/#$home/~}"

# Get git branch (skip optional locks to avoid contention)
branch=$(git -C "$cwd" --no-optional-locks branch --show-current 2>/dev/null)

# Line 1: project | cwd | session_id
line1="project: ${project_display}  |  cwd: ${cwd_display}"
if [ -n "$session_id" ]; then
    line1="${line1}  |  session: ${session_id}"
fi

# Line 2: branch | model | context_usage
line2=""
if [ -n "$branch" ]; then
    line2="branch: ${branch}"
fi
if [ -n "$model" ]; then
    if [ -n "$line2" ]; then
        line2="${line2}  |  ${model}"
    else
        line2="${model}"
    fi
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
