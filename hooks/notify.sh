#!/bin/sh
# Claude Code hook: play sound and show macOS notification
# Usage: notify.sh <title> [body]

title="${1:-Claude Code}"
body="${2:-}"

# Desktop notification
osascript -e "display notification \"$body\" with title \"$title\"" &

# Sound (use macOS system sound)
afplay /System/Library/Sounds/Glass.aiff &

wait
