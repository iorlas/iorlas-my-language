#!/usr/bin/env python3
"""Stop hook: count my-language lint hits in the reply that just went out.

Log-only, on purpose. A blocking gate was measured against 4,959 of my past turns
and fires on 28% of them -- every third or fourth reply would cost an extra model
turn, and he would have seen the bad message anyway, because assistant text streams
and no hook runs before it reaches him.

So this writes a line per violation to ~/.claude/my-language-lint.jsonl and exits 0.
`mine.py --lint` reads it. That turns the skill's "run mine.py every few weeks"
into something that happens whether or not anyone remembers.

Never blocks, never prints, never fails the turn: every error path exits 0.
"""
import json
import os
import re
import sys
from datetime import datetime, timezone

LOG = os.path.expanduser("~/.claude/my-language-lint.jsonl")

# Phrases only. Measured at 0% of his 5,316 messages and 2-10% of mine, which is
# what makes them safe for a machine. Single words are not: `carries a version
# number` is his and literal, `the row carries its own next move` is mine and
# personified, and no regex separates those.
PHRASES = [
    "here's the honest", "your call", "say the word and i'll", "if you'd rather",
    "want me to write", "whenever you want", "worth knowing", "worth flagging",
    "two things worth", "one thing worth", "your instinct", "is genuinely",
    "you asked", "per your",
]
WORDS = [
    "genuinely", "here's", "verified", "confirmed", "flagged", "deliberately",
    "strongest", "sharpest", "seam", "spine", "provenance", "invariant", "framing",
    "instinct", "trap", "load-bearing", "moat", "landmine", "lede", "tension",
    "arc", "headroom", "payoff", "collapses", "settles", "clears", "rides", "pins",
]


def last_assistant_text(transcript_path: str) -> str:
    text = []
    with open(transcript_path, encoding="utf-8") as handle:
        for line in handle:
            try:
                entry = json.loads(line)
            except ValueError:
                continue
            if entry.get("type") != "assistant":
                continue
            content = entry.get("message", {}).get("content", [])
            block = [c.get("text", "") for c in content if c.get("type") == "text"]
            if block:
                text = block
    return "\n".join(text)


def main() -> None:
    payload = json.load(sys.stdin)
    reply = last_assistant_text(payload.get("transcript_path", ""))
    if not reply.strip():
        return
    hits = [p for p in PHRASES
            if re.search(r"\b" + p.replace(" ", r"\s+") + r"\b", reply, re.I)]
    hits += [w for w in WORDS if re.search(r"\b" + re.escape(w), reply, re.I)]
    if not hits:
        return
    with open(LOG, "a", encoding="utf-8") as handle:
        handle.write(json.dumps({
            "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "session": payload.get("session_id", ""),
            "cwd": payload.get("cwd", ""),
            "chars": len(reply),
            "hits": hits,
        }) + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
