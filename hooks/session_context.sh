#!/bin/sh
# SessionStart (startup|compact): print the my-language core so it is in context from the
# first message and comes back after every compaction. Frontmatter stripped; one source file.
f="${CLAUDE_PLUGIN_ROOT}/skills/my-language/SKILL.md"
[ -r "$f" ] || exit 0
echo "my-language rules (from the iorlas-my-language plugin) apply to every chat reply to Denis:"
awk 'n>=2 {print} /^---$/ {n++}' "$f"
exit 0
