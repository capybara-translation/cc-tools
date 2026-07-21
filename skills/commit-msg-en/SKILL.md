---
name: commit-msg-en
description: Generate a commit message in English from staged/unstaged changes since the last commit and copy it to the clipboard.
disable-model-invocation: true
---

## Context: Current Git Changes

### Recent commit history (for style reference)
!`git log --oneline -10 2>/dev/null || echo "No git history found"`

### Staged changes
!`git diff --cached --stat 2>/dev/null || echo "No staged changes"`

### Unstaged changes
!`git diff --stat 2>/dev/null || echo "No unstaged changes"`

### Detailed diff (staged + unstaged)
!`git diff HEAD 2>/dev/null || git diff 2>/dev/null || echo "No changes detected"`

## Your Task

0. If the commit history shows "No git history found", the repository is uninitialized or has no commits yet. In this case, run `git init && git add .`, then re-fetch the diff with `git diff --cached --stat` and `git diff --cached` before proceeding.
1. Analyze the diff and recent commit history above to understand the project's commit message style.
2. Generate a concise, structured commit message following these rules:
   - Use Conventional Commits format: `type(scope): description`
   - Types: feat, fix, refactor, docs, test, chore, style, perf, ci, build
   - **The description MUST be written in English** (e.g., `feat(auth): add OAuth authentication to login screen`)
   - Use imperative mood in the subject line (e.g., "add" not "added" or "adds")
   - Keep the subject line under 72 characters
   - Add a body with bullet points after a blank line if needed to explain "why"
   - **The subject line and each bullet point MUST be written on a single line** (do not insert line breaks mid-sentence; line breaks are only allowed between the subject and body, and between bullet points)
   - Follow existing commit history style if present
   - **NEVER include a "Co-Authored-By" line**
3. Present the commit message in a code block.
4. **Copy to clipboard**, preserving UTF-8 + LF so it reaches the GUI clipboard intact. Do it in two steps:
   1. Write the message to a temp file as **exact bytes (LF line endings)**. Using the Write tool is the most reliable. If doing it in the shell only, use a quoted heredoc to avoid variable expansion / escaping issues (it appends one trailing newline, which git strips — harmless):
      ```sh
      cat > "${TMPDIR:-/tmp}/claude-commit-msg.txt" <<'COMMIT_MSG_EOF'
      <the commit message body, verbatim>
      COMMIT_MSG_EOF
      ```
   2. Read that temp file as UTF-8 and set the GUI clipboard (works in both CLI and desktop Claude Code):
      ```sh
      osascript -e 'set the clipboard to (read POSIX file "'"${TMPDIR:-/tmp}/claude-commit-msg.txt"'" as «class utf8»)'
      ```
   - **Do NOT use `pbcopy` or `do shell script "cat …"`.** In desktop Claude Code, Bash is detached from the GUI (Aqua) session, so `pbcopy` writes to an isolated pasteboard that never reaches the GUI clipboard; and `osascript`'s `do shell script` converts LF→CR, destroying the subject/body `\n\n` boundary (breaking the GUI Git client's Title/Description auto-split).
   - Only use line breaks intentionally (the blank line between subject and body, and between bullet points); do not break sentences or bullets across multiple lines.
5. Inform the user that the message has been copied to the clipboard.

If no changes are detected, inform the user that there are no changes to commit.
