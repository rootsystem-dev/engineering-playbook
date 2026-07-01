#!/usr/bin/env python3
"""
Backfill historical meeting transcripts -> vault Transcripts/ as QMD-chunkable markdown.

Deterministic, idempotent, stdlib-only — NO model, NO MCP. Safe to run detached
(nohup) and re-run; it skips anything already converted. Mirrors the schema the
live SessionStart Granola sync hook produces (see reference_granola_sync_hook).

Handles three source formats found under the Dropbox transcript archive:
  - Granola .txt   : embedded "Raw Output" JSON (transcript + enhanced_notes + attendees)
  - Fireflies .json: list of {sentence, speaker_name, startTime, ...} segments
  - Otter .txt     : "Speaker Name  MM:SS" blocks (incl. inside .zip exports)

Media (mp3/mp4/m4a/pdf) is ignored. Output: Transcripts/<YYYY-MM-DD>-<slug>.md
Run:  python3 backfill-transcripts.py [--dry-run] [--limit N]
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
import unicodedata
import zipfile

# --- paths -------------------------------------------------------------------
HOME = os.path.expanduser("~")
VAULT = "/Users/robertjacques/Library/CloudStorage/Dropbox-RootSystem/Rob Jacques/RMJ.Obsidian/RobbyRobZettelkasten"
OUT_DIR = os.path.join(VAULT, "Transcripts")
SOURCES = [
    "/Users/robertjacques/Dropbox/Apps/Fathom",
    "/Users/robertjacques/Dropbox/Apps/MeetingTranscripts",
]
STATE_DIR = os.path.join(HOME, ".cache", "granola-sync")
SYNCED_IDS = os.path.join(STATE_DIR, "synced-ids")          # granola meeting ids
MANIFEST = os.path.join(STATE_DIR, "backfill-manifest")     # source paths already processed
LOG = os.path.join(VAULT, "DailyOps-CC", "scripts", "backfill.log")

MEDIA_EXT = {".mp3", ".mp4", ".m4a", ".wav", ".pdf", ".png", ".jpg", ".jpeg", ".zip.part"}


def log(msg):
    line = f"[{dt.datetime.now().strftime('%H:%M:%S')}] {msg}"
    print(line)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def slugify(title):
    """kebab-case ascii slug; strips emoji/punctuation."""
    t = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode()
    t = re.sub(r"[^a-zA-Z0-9]+", "-", t).strip("-").lower()
    return (t or "untitled")[:80]


def fmt_frontmatter(meta):
    """meta: dict with title,date,datetime,source,meeting_id?,granola_url?,participants,tags."""
    lines = ["---", f"title: {meta['title']}", f"date: {meta['date']}"]
    if meta.get("datetime"):
        lines.append(f"datetime: {meta['datetime']}")
    lines.append(f"source: {meta['source']}")
    if meta.get("meeting_id"):
        lines.append(f"meeting_id: {meta['meeting_id']}")
    if meta.get("granola_url"):
        lines.append(f"granola_url: {meta['granola_url']}")
    lines.append("participants:")
    for p in meta["participants"]:
        lines.append(f"  - {p}")
    lines.append(f"tags: [{', '.join(meta['tags'])}]")
    lines.append("---")
    return "\n".join(lines)


def write_doc(meta, body):
    """Write the markdown file. Idempotency is handled by the source-path MANIFEST
    (a source is processed once), so here we never silently drop: on a date+slug
    collision with a DIFFERENT meeting we append a numeric suffix."""
    base = f"{meta['date']}-{slugify(meta['title'])}"
    dest = os.path.join(OUT_DIR, base + ".md")
    n = 2
    while os.path.exists(dest):
        dest = os.path.join(OUT_DIR, f"{base}-{n}.md")
        n += 1
    with open(dest, "w") as f:
        f.write(fmt_frontmatter(meta) + "\n\n" + body + "\n")
    return os.path.basename(dest)


# --- transcript formatters ---------------------------------------------------
def fmt_granola_transcript(text):
    """Granola 'Me:'/'Them:' inline string -> bulleted turns (Me=Rob)."""
    parts = re.split(r"\s+(Me|Them):\s*", " " + text.strip())
    out = []
    i = 1
    while i < len(parts) - 1:
        spk, txt = parts[i], parts[i + 1].strip()
        if txt:
            out.append(f"- **{'Rob' if spk == 'Me' else 'Them'}:** {txt}")
        i += 2
    return "\n".join(out)


def fmt_named_turns(segments):
    """segments: list of (speaker, text). Merge consecutive same-speaker -> bullets."""
    turns, cur_spk, buf = [], None, []
    for spk, txt in segments:
        txt = (txt or "").strip()
        if not txt:
            continue
        if spk == cur_spk:
            buf.append(txt)
        else:
            if cur_spk is not None:
                turns.append(f"- **{cur_spk}:** {' '.join(buf)}")
            cur_spk, buf = spk, [txt]
    if cur_spk is not None:
        turns.append(f"- **{cur_spk}:** {' '.join(buf)}")
    return "\n".join(turns)


# --- per-format parsers ------------------------------------------------------
def parse_granola(path):
    text = open(path, encoding="utf-8", errors="replace").read()
    m = re.search(r"Raw Output:\s*(\{.*\})\s*$", text, re.S)
    if not m:
        raise ValueError("no Raw Output JSON")
    d = json.loads(m.group(1))
    iso = d.get("calendar_event_time", "")
    date = iso[:10] if iso else dt.date.fromtimestamp(os.path.getmtime(path)).isoformat()
    title = d.get("calendar_event_title") or d.get("title") or "Untitled"
    mid = d.get("id", "")
    parts = []
    for a in d.get("attendees", []) or []:
        nm, em = a.get("name", "").strip(), a.get("email", "").strip()
        parts.append(f"{nm} <{em}>" if em else nm)
    if not parts:
        cn, ce = d.get("creator_name", "Rob Jacques"), d.get("creator_email", "rob@rootsystem.com")
        parts = [f"{cn} <{ce}>"]
    meta = {
        "title": title, "date": date, "datetime": iso or None, "source": "granola",
        "meeting_id": mid, "granola_url": f"https://notes.granola.ai/d/{mid}" if mid else None,
        "participants": parts, "tags": ["meeting", "transcript", "granola"],
    }
    body_parts = [f"# {title}", "", "## Participants"]
    body_parts += [f"- {p}" for p in parts]
    if d.get("enhanced_notes"):
        body_parts += ["", "## Summary", "", d["enhanced_notes"].strip()]
    body_parts += ["", "## My Notes", "", d.get("my_notes", "").strip() or "_none_"]
    body_parts += ["", "## Transcript", "",
                   "> Granola diarization: \"Rob\" = note-creator mic, \"Them\" = all other voices.",
                   "", fmt_granola_transcript(d.get("transcript", ""))]
    return meta, "\n".join(body_parts), mid


def _date_from_name(name):
    """Pull a date from common filename patterns; else None."""
    # Check the trailing epoch-ms FIRST: Fireflies names end `-<13 digits>.json`,
    # and the date regex below would otherwise carve a bogus date out of the
    # middle of that epoch (e.g. `...1720714205993...` -> 2071-42-05). The date
    # regex is also guarded with (?<!\d)/(?!\d) so it only matches a standalone
    # date token, never digits embedded in a longer run.
    m = re.search(r"-(\d{13})\.json$", name)                          # trailing epoch ms
    if m:
        return dt.date.fromtimestamp(int(m.group(1)) / 1000).isoformat()
    m = re.search(r"(?<!\d)(20\d{2})[-_]?(\d{2})[-_]?(\d{2})(?!\d)", name)  # 2026-04-16 / 20230710
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    return None


def parse_fireflies(path):
    arr = json.load(open(path, encoding="utf-8", errors="replace"))
    if not isinstance(arr, list) or not arr:
        raise ValueError("empty/non-list fireflies json")
    segs = [(s.get("speaker_name") or "Speaker", s.get("sentence", "")) for s in arr]
    name = os.path.basename(path)
    title = re.sub(r"-\d{10,}\.json$", "", name)
    title = re.sub(r"\.json$", "", title).strip() or "Fireflies Meeting"
    date = _date_from_name(path) or dt.date.fromtimestamp(os.path.getmtime(path)).isoformat()
    speakers = sorted({s for s, _ in segs})
    meta = {
        "title": title, "date": date, "datetime": None, "source": "fireflies",
        "participants": speakers, "tags": ["meeting", "transcript", "fireflies"],
    }
    body = [f"# {title}", "", "## Participants"] + [f"- {s}" for s in speakers]
    body += ["", "## Transcript", "", fmt_named_turns(segs)]
    return meta, "\n".join(body), None


def parse_otter_text(text, name, src_path):
    # Blocks: "Speaker Name  MM:SS\n<text lines>\n\n"
    segs, cur, buf = [], None, []
    for line in text.splitlines():
        h = re.match(r"^(.{1,60}?)\s{2,}\d{1,2}:\d{2}(?::\d{2})?\s*$", line)
        if h:
            if cur is not None:
                segs.append((cur, " ".join(buf)))
            cur, buf = h.group(1).strip(), []
        elif line.strip():
            buf.append(line.strip())
    if cur is not None:
        segs.append((cur, " ".join(buf)))
    if not segs:
        raise ValueError("no otter blocks (empty/stub)")
    title = re.sub(r"\.txt$", "", name)
    title = re.sub(r"\(\d+\)$", "", title).strip() or "Otter Meeting"
    # date: prefer a date in the path (parent folder e.g. otter-export-20230710), else file mtime
    date = _date_from_name(src_path) or dt.date.fromtimestamp(os.path.getmtime(src_path)).isoformat()
    speakers = sorted({s for s, _ in segs})
    meta = {
        "title": title, "date": date, "datetime": None, "source": "otter",
        "participants": speakers, "tags": ["meeting", "transcript", "otter"],
    }
    body = [f"# {title}", "", "## Participants"] + [f"- {s}" for s in speakers]
    body += ["", "## Transcript", "", fmt_named_turns(segs)]
    return meta, "\n".join(body), None


# --- dispatch + walk ---------------------------------------------------------
def classify(path):
    low = path.lower()
    ext = os.path.splitext(low)[1]
    if ext in MEDIA_EXT:
        return None
    if "granola" in low and ext == ".txt":
        return "granola"
    if "fireflies" in low and ext == ".json":
        return "fireflies"
    if ext == ".json" and "fireflies" in path.lower():
        return "fireflies"
    if "otterexport" in low or "otter" in low:
        if ext == ".txt":
            return "otter"
        if ext == ".zip":
            return "otter-zip"
    if ext == ".txt":
        # generic .txt under otter dir
        return "otter" if "otterexport" in low else None
    return None


def load_state():
    done = set()
    if os.path.exists(MANIFEST):
        done = set(l.strip() for l in open(MANIFEST) if l.strip())
    synced = set()
    if os.path.exists(SYNCED_IDS):
        synced = set(l.strip() for l in open(SYNCED_IDS) if l.strip())
    return done, synced


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="parse + report, write nothing")
    ap.add_argument("--limit", type=int, default=0, help="cap files processed (0 = all)")
    args = ap.parse_args()

    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(STATE_DIR, exist_ok=True)
    done, synced = load_state()

    # collect candidate files
    files = []
    for root in SOURCES:
        for dirpath, _, names in os.walk(root):
            for n in names:
                files.append(os.path.join(dirpath, n))
    files.sort()

    written = skipped = failed = 0
    new_ids, new_manifest = [], []
    log(f"backfill start: {len(files)} files scanned, {len(done)} already done"
        f"{' [DRY-RUN]' if args.dry_run else ''}")

    for path in files:
        if args.limit and written >= args.limit:
            break
        if path in done:
            continue
        kind = classify(path)
        if kind is None:
            continue
        try:
            results = []
            if kind == "granola":
                results = [parse_granola(path)]
            elif kind == "fireflies":
                results = [parse_fireflies(path)]
            elif kind == "otter":
                results = [parse_otter_text(open(path, encoding="utf-8", errors="replace").read(),
                                            os.path.basename(path), path)]
            elif kind == "otter-zip":
                with zipfile.ZipFile(path) as z:
                    for inner in z.namelist():
                        if inner.lower().endswith(".txt"):
                            txt = z.read(inner).decode("utf-8", "replace")
                            results.append(parse_otter_text(txt, os.path.basename(inner), path))
            for meta, body, mid in results:
                if mid and mid in synced:
                    skipped += 1
                    continue
                if args.dry_run:
                    log(f"  WOULD write [{meta['source']}] {meta['date']}-{slugify(meta['title'])}.md "
                        f"({len(meta['participants'])} ppl)")
                    written += 1
                    continue
                fn = write_doc(meta, body)
                if fn:
                    written += 1
                    log(f"  wrote [{meta['source']}] {fn}")
                    if mid:
                        new_ids.append(mid)
                        synced.add(mid)
                else:
                    skipped += 1
            new_manifest.append(path)
        except Exception as e:
            failed += 1
            log(f"  FAIL {os.path.basename(path)}: {e}")

    if not args.dry_run:
        if new_ids:
            with open(SYNCED_IDS, "a") as f:
                f.write("\n".join(new_ids) + "\n")
        if new_manifest:
            with open(MANIFEST, "a") as f:
                f.write("\n".join(new_manifest) + "\n")
    log(f"backfill done: wrote {written}, skipped {skipped}, failed {failed}")


if __name__ == "__main__":
    main()
