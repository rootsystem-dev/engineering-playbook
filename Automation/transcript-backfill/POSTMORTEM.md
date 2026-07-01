# Post-mortem: fake dates from a greedy filename regex

**Date:** 2026-06-30 · **System:** `backfill-transcripts.py` (one-time historical
transcript ETL: Fireflies/Otter/Granola exports → Obsidian vault `Transcripts/`)

## What happened

A one-time backfill (run 2026-06-18, see `backfill.log.2026-06-18`) imported
~800 meeting transcripts. 16 Fireflies transcripts were written with **impossible
dates** — `date: 2071-42-05`, `2096-72-43`, `2055-09-33` (month/day out of
range) — and the same garbage went into the filenames
(`2071-42-05-integrations.md`). The corruption sat unnoticed for 12 days until a
strict YAML parser (a vault-frontmatter linter) choked on them
(`ValueError: month must be in 1..12, not 42`).

## Root cause

Date extraction from the source filename tried patterns in the **wrong order**:

```python
def _date_from_name(name):
    m = re.search(r"(20\d{2})[-_]?(\d{2})[-_]?(\d{2})", name)  # ran FIRST
    if m: return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    m = re.search(r"-(\d{13})\.json$", name)                   # never reached
    if m: return dt.date.fromtimestamp(int(m.group(1)) / 1000).isoformat()
    return None
```

Fireflies files are named `Title-<13-digit-epoch-ms>.json`, e.g.
`Integrations-1720714205993.json`. The loose date regex matched digits **inside
the epoch** — `1720714205993` → `2071`,`42`,`05` — and returned before the
correct epoch branch could run. `2024-07-11` (the real date, from the epoch)
became `2071-42-05`.

Two failures compounded it:
1. **Order:** the general/greedy pattern ran before the specific/unambiguous one.
2. **No validation:** the extracted date was never checked. `dt.date(2071, 42, 5)`
   would have raised at extraction time; instead a syntactically-fine but
   impossible string was written and only failed far downstream.

## The fix

```python
def _date_from_name(name):
    # Specific/unambiguous pattern FIRST.
    m = re.search(r"-(\d{13})\.json$", name)                   # trailing epoch ms
    if m: return dt.date.fromtimestamp(int(m.group(1)) / 1000).isoformat()
    # Guard the loose date regex so it can't match digits inside a longer run.
    m = re.search(r"(?<!\d)(20\d{2})[-_]?(\d{2})[-_]?(\d{2})(?!\d)", name)
    if m: return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    return None
```

Verified: the 16 bad files recovered to correct dates; legit embedded dates
(`otter-export-20230710`, `Meeting 2026-04-16.json`) still parse. The 16 vault
files were repaired (correct `date:` + `datetime:` from the epoch) and renamed.

## Lessons (generalize beyond this script)

1. **Order fallback parsers most-specific first.** When several patterns can
   extract the same field, a greedy/general one placed ahead of a specific one
   will strip-mine data meant for the later rule. Specific → general, always.
2. **Anchor numeric regexes.** A bare `\d{2}` inside free text will match part of
   a longer number. Guard with `(?<!\d)`/`(?!\d)` (or `\b`) so you match a token,
   not a fragment.
3. **Validate at the source and fail loud.** Construct the real type at extraction
   (`dt.date(y, m, d)`) so impossible values raise *there*, not silently persist
   and surface days later in an unrelated component. Silent-but-wrong is worse
   than a crash — the crash is 12 days earlier and 100× cheaper to trace.
4. **A strict parser downstream is a cheap tripwire.** The bug was only caught
   because something eventually applied strict YAML. Consider running that strict
   check *at write time* in the ETL itself.

## Status

One-time script; archived here (not scheduled — live meeting sync runs elsewhere
via the Granola sync hook). Kept for reference and for the lesson above.
