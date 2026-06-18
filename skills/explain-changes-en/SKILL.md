---
name: explain-changes-en
description: Explain the code changes you applied, ordered by importance, with prose plus representative code snippets, in English. Accepts an optional scope argument (base branch, git range, or PR number).
disable-model-invocation: true
---

## Context: Explanation Target

### Arguments
The user may provide an optional scope argument.
- Base branch name (e.g. `/explain-changes-en main`): explain `git diff <branch>...HEAD`
- Git range (e.g. `/explain-changes-en main...HEAD`, `abc123..def456`): explain that range
- PR number / `#N` / PR URL (e.g. `/explain-changes-en 14`): explain `gh pr diff <N>`
- Empty: explain uncommitted changes (`git diff HEAD`); if there are none, fall back to the current branch vs its base (`git diff <base>...HEAD`, base = merge-base with main/master)

Argument value: $ARGUMENTS

### Current branch
!`git branch --show-current 2>/dev/null`

### Recent commits (for orientation)
!`git log --oneline -15 2>/dev/null || echo "No git history"`

### Default scope: uncommitted changes (stat)
!`git diff --stat HEAD 2>/dev/null || echo "No uncommitted changes"`

### Default scope: uncommitted changes (diff)
!`git diff HEAD 2>/dev/null`

## Your Task

The user wants to understand the changes you (or someone) applied. Organize the diff **by importance** and explain it with **prose plus representative code snippets**. Do not paste the raw diff verbatim — synthesize it so the reader grasps the design decisions.

### Steps

0. **Resolve the target diff** based on the argument (`$ARGUMENTS`):
   - Branch name → `git diff <branch>...HEAD` and `git diff --stat <branch>...HEAD`
   - Git range (`a...b` / `a..b`) → use it directly with `git diff` / `git diff --stat`
   - PR number / `#N` / PR URL → `gh pr diff <N>` (use `gh pr diff <N> --name-only` for the file list if needed)
   - Empty → use the uncommitted changes above. If there are none, find the base via `git merge-base HEAD main || git merge-base HEAD master` and use `git diff <base>...HEAD`
   If the diff is empty, tell the user there are no changes to explain and stop.

1. **Grasp the whole picture**: infer intent from the diffstat and diff. Factor in CLAUDE.md design conventions if present.

2. **Group by importance**: reorder files into an **importance-ranked hierarchy**, NOT by path or diff order. A rough ladder:
   - Core logic / behavior changes (the feature's "brain": algorithms, state transitions, invariants)
   - Public interfaces / wiring (APIs, routing, DI, signature changes)
   - Persistence / schema / migrations
   - Frontend / UI
   - Tests / docs / mechanical follow-up edits / formatting (mention briefly, last)

3. **File-by-file explanation**: starting from the most important, state each file's **changes/additions** and the **"why"** in one to a few sentences. Note whether it is a new file or a modification.

4. **Intersperse representative code snippets**: for the most important files, include a code block with **only the key lines**.
   - Precede each block with a one-line "what this shows".
   - Do not paste whole files or whole methods. Focus on the few lines that carry the decision; elide the rest with `// ...` / `# ...`.
   - You may trim comments as long as the original intent stays clear.
   - For mechanical churn (signature-follow test edits, gofmt formatting, etc.), do not add snippets — cover it in one or two sentences at the end.

5. **Design takeaways**: end with 2–4 bullets capturing the **through-line** of the change (the overall spine, not individual files).

### Rules
- Order **by importance**, not by path, alphabetically, or diff order.
- Snippets are **key lines only**. No verbose quoting or whole-file dumps.
- **Every code block gets a one-line "what this shows".**
- Do not paste the raw diff verbatim — synthesize it.
- Do not assert from guesswork. Base claims on what the diff shows; flag anything uncertain as uncertain.
- Output in English. Keep technical terms, code identifiers, and API names as-is.
- Be concise. Keep prose tight and let the snippets carry the detail.
</content>
