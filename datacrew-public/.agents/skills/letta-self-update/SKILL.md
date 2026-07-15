---
name: letta-self-update
description: "How to safely update your own letta-code CLI when someone asks you to update/upgrade yourself or get the latest version. Use when: (1) a user asks you to update, upgrade, or self-update, (2) a user asks what version you're running and whether it's current. NOT for: updating any other host or agent (cubby/alix/petra) — this is scoped to bonker only."
metadata:
  version: 1.0.0
  created: 2026-07-15
---

# letta-self-update

## The trap — install alone is a phantom update

`npm install -g @letta-ai/letta-code@latest` (or `letta update` /
`letta upgrade`) only replaces the package files on disk. **It does not
reload the process you are currently running as.** Your own answers keep
coming from the OLD build until something restarts you.

This isn't theoretical — it happened on 2026-07-15: a self-update the day
before had bumped the installed package to a newer version, but
`systemctl --user show letta-datacrew.service -p ActiveEnterTimestamp`
showed the live process had been running continuously since two days
earlier. `letta --version` on disk said one thing; the process actually
answering Slack messages was a different, older build — for over 24
hours, with no signal to anyone that anything was stale.

## The fix — install AND restart, as one action

When asked to update/upgrade yourself, always run both commands, not just
the first:

```bash
npm install -g @letta-ai/letta-code@latest
systemctl --user restart letta-datacrew.service
```

The restart kills your own current process — that is expected and
correct, not an error to recover from. A fresh process starts on the new
build and serves the next message. Don't try to confirm the new version
in the same turn after issuing the restart (you won't be the process that
gets to report it) — say something like "Updating and restarting now —
I'll be running the new version for your next message," end the turn, and
let the fresh process answer any follow-up.

If you want to confirm a *previous* self-update actually took effect,
don't trust `letta --version` alone — it only reports what's installed on
disk. Compare it against when the service actually last restarted:

```bash
letta --version
systemctl --user show letta-datacrew.service -p ActiveEnterTimestamp
```

If the restart timestamp predates when you (or someone) last ran the
install, you're still running the old build — restart to pick it up.

## Scope

This only covers **bonker's** `~/.local/bin/letta` — the install
`letta-datacrew.service` actually execs, which is what you are running
as. It does not touch cubby (alix/petra) or bonker's separate
`/usr/bin/letta` (an interactive-shell copy, irrelevant to your own
runtime). Those are handled by a weekly cross-host cron documented in the
`update-letta-code` skill in the `simpleDiscordBot` monorepo
(`.agents/skills/update-letta-code/`) — that skill is the operator-facing
counterpart to this one; this one is scoped to what you can safely
trigger on yourself.
