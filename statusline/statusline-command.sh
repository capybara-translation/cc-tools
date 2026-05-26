#!/bin/sh
input=$(cat)
cwd=$(echo "$input" | jq -r '.workspace.current_dir')
project_dir=$(echo "$input" | jq -r '.workspace.project_dir')
session_id=$(echo "$input" | jq -r '.session_id // empty')
model=$(echo "$input" | jq -r '.model.display_name // empty')
effort=$(echo "$input" | jq -r '.effort.level // empty')
used_pct=$(echo "$input" | jq -r '.context_window.used_percentage // empty')
rl_5h=$(echo "$input" | jq -r '.rate_limits.five_hour.used_percentage // empty')
rl_7d=$(echo "$input" | jq -r '.rate_limits.seven_day.used_percentage // empty')
pr_number=$(echo "$input" | jq -r '.pr.number // empty')
pr_state=$(echo "$input" | jq -r '.pr.review_state // empty')

# Shorten paths by replacing $HOME with ~
home="$HOME"
cwd_display="${cwd/#$home/~}"
project_display="${project_dir/#$home/~}"

# Get git branch (skip optional locks to avoid contention)
branch=$(git -C "$cwd" --no-optional-locks branch --show-current 2>/dev/null)

# One item per line: project, session, cwd, branch
echo "project: ${project_display}"
[ -n "$session_id" ] && echo "session: ${session_id}"
echo "cwd: ${cwd_display}"
[ -n "$branch" ] && echo "branch: ${branch}"

# Append a field to the metrics line, separated by " | "
append_metric() {
    if [ -n "$metrics" ]; then
        metrics="${metrics}  |  $1"
    else
        metrics="$1"
    fi
}

# Metrics line: model | effort | ctx | 5h | 7d
metrics=""
[ -n "$model" ] && append_metric "model: ${model}"
[ -n "$effort" ] && append_metric "effort: ${effort}"
if [ -n "$used_pct" ]; then
    append_metric "ctx: $(printf '%.0f' "$used_pct")%"
fi
if [ -n "$rl_5h" ]; then
    append_metric "5h: $(printf '%.0f' "$rl_5h")%"
fi
if [ -n "$rl_7d" ]; then
    append_metric "7d: $(printf '%.0f' "$rl_7d")%"
fi
[ -n "$metrics" ] && echo "$metrics"

# Conditional PR line
if [ -n "$pr_number" ]; then
    if [ -n "$pr_state" ]; then
        echo "PR #${pr_number} (${pr_state})"
    else
        echo "PR #${pr_number}"
    fi
fi
