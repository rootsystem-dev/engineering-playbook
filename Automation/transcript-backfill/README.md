# transcript-backfill

One-time ETL that imported historical meeting transcripts (Fireflies `.json`,
Otter `.txt`, Granola) from the Dropbox archive into the Obsidian vault
`Transcripts/` as QMD-chunkable markdown. Run once on 2026-06-18.

**Not scheduled.** Ongoing meeting capture runs elsewhere (Granola sync hook →
vault). This is kept for reference, not reuse.

## Files
- `backfill-transcripts.py` — the ETL (with the `_date_from_name` fix applied).
- `backfill.log.2026-06-18` — the actual run log.
- `POSTMORTEM.md` — **read this.** A greedy filename date-regex carved fake dates
  (`2071-42-05`) out of Fireflies epoch-ms, silently, caught 12 days later. The
  generalizable lessons (parser ordering, anchored numeric regexes, validate-and-
  fail-loud at the source) are the reason this lives in the playbook.

## If ever re-run
Sources are hardcoded (`SOURCES` in the script). It walks `/Users/.../Dropbox/
Apps/{Fathom,MeetingTranscripts}`, dedupes by date+slug, writes to the vault
`Transcripts/` dir. Review paths before running.
