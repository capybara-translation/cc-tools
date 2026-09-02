---
name: session-id
description: Display the current Claude Code session ID (the UUID used by `claude --resume` and the transcript filename).
disable-model-invocation: true
---

Output the current session ID exactly as shown below, as a single fenced code block. Do not add any explanation, prefix, or other text before or after the block.

```
${CLAUDE_SESSION_ID}
```

If the block above still contains the literal text `${CLAUDE_SESSION_ID}` instead of a UUID, placeholder substitution did not run in this session; say so in one sentence instead of printing the block.
