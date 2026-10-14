# iorlas-my-language

A Claude Code plugin that carries one person's chat register: six message shapes with word caps, five rules fired by the draft, and a banned word and phrase list, all mined from real pushback.

## What it does

- `SessionStart` hook (`startup|compact`): prints the ~3k-char core from `skills/my-language/SKILL.md` into context, so the rules are present from the first message and return after every compaction.
- `Stop` hook: logs banned phrases in each reply to `~/.claude/my-language-lint.jsonl`. Log only; never blocks.
- `my-language` skill: the same core, loadable on demand; `reference.md` holds each rule's reason and the incident behind it.

## Install

```sh
claude plugin marketplace add iorlas/iorlas-marketplace
claude plugin install iorlas-my-language@iorlas-marketplace
```

The rules are written for one reader. Fork and replace the shapes and word lists with your own.
