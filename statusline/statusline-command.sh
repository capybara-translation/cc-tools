#!/bin/sh
input=$(cat)
cwd=$(echo "$input" | jq -r '.workspace.current_dir')
project_dir=$(echo "$input" | jq -r '.workspace.project_dir')

# Shorten paths by replacing $HOME with ~
home="$HOME"
cwd_display="${cwd/#$home/~}"
project_display="${project_dir/#$home/~}"

# Get git branch (skip optional locks to avoid contention)
branch=$(git -C "$cwd" --no-optional-locks branch --show-current 2>/dev/null)

# Build status line
if [ -n "$branch" ]; then
    printf "cwd: %s  |  project: %s  |  branch: %s" "$cwd_display" "$project_display" "$branch"
else
    printf "cwd: %s  |  project: %s" "$cwd_display" "$project_display"
fi