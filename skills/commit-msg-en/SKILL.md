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
   - Follow existing commit history style if present
   - **NEVER include a "Co-Authored-By" line**
3. Present the commit message in a code block.
4. **Immediately copy to clipboard**: run `printf '%s' "<message>" | pbcopy`.
5. Inform the user that the message has been copied to the clipboard.

If no changes are detected, inform the user that there are no changes to commit.
