#!/usr/bin/env python3
"""Make the public copies of the travel dashboard data for this site.

Usage:
    python3 scripts/export_public.py SRC_DIR [OUT_DIR]

SRC_DIR holds items.json, pick.json, budget.json and digest.json from the
private dashboard. Public-safe copies are written to OUT_DIR (default: the
repo's data/ folder). Keep SRC_DIR outside the repo so the private copies are
never committed.

What is left out of the public copies:
- news rows about the owner's own trip (section "trip"),
- any sentence that mentions the owner's status or trip plans
  (see PRIVATE_WORDS), in every text field.
"""
import json
import re
import sys
from pathlib import Path

PRIVATE_SECTIONS = {"trip"}
PRIVATE_WORDS = ("플래티넘", "리우", "레베이용", "코파카바나", "Réveillon", "Copacabana")

ITEM_KEYS = {"id", "section", "program", "title", "summary", "tip", "source", "url", "date",
             "dateLabel", "due", "dueLabel", "dueKind", "priority", "added"}
PICK_KEYS = {"id", "date", "dateLabel", "place", "headline", "why", "stay", "getThere",
             "bestTime", "source", "url"}
DIGEST_KEYS = {"runDate", "updatedAt", "updatedLabel", "newCount", "headline"}


def is_private(text):
    return any(w in (text or "") for w in PRIVATE_WORDS)


def scrub(text):
    """Drop the sentences that mention anything private; keep the rest."""
    if not isinstance(text, str) or not is_private(text):
        return text
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return " ".join(s for s in sentences if not is_private(s)).strip()


def load(src, name):
    with open(src / name, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise SystemExit(f"{name}: expected a JSON array")
    return data


def check_keys(rows, keys, name):
    for r in rows:
        missing = keys - set(r)
        if missing:
            raise SystemExit(f"{name}: row {r.get('id', '?')} is missing {sorted(missing)}")


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    src = Path(sys.argv[1])
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).resolve().parent.parent / "data"
    out.mkdir(parents=True, exist_ok=True)

    items = load(src, "items.json")
    check_keys(items, ITEM_KEYS, "items.json")
    public_items = []
    for r in items:
        if r["section"] in PRIVATE_SECTIONS or is_private(r["title"]):
            continue
        r = dict(r, summary=scrub(r["summary"]), tip=scrub(r["tip"]))
        if r["summary"]:
            public_items.append(r)

    picks = load(src, "pick.json")
    check_keys(picks, PICK_KEYS, "pick.json")
    public_picks = []
    for r in picks:
        if is_private(r["place"]) or is_private(r["headline"]):
            continue
        public_picks.append(dict(r, why=scrub(r["why"]), stay=scrub(r["stay"]), getThere=scrub(r["getThere"])))

    budget = load(src, "budget.json")
    public_budget = [dict(r, why=scrub(r.get("why", "")), priceNote=scrub(r.get("priceNote", "")))
                     for r in budget if not is_private(r.get("place", ""))]

    digest = load(src, "digest.json")
    check_keys(digest, DIGEST_KEYS, "digest.json")
    public_digest = []
    for r in digest[:1]:
        run_date = r["runDate"]
        public_digest.append(dict(
            r,
            headline=scrub(r["headline"]),
            newCount=sum(1 for i in public_items if i.get("added") == run_date),
        ))

    for name, rows in (("items.json", public_items), ("pick.json", public_picks),
                       ("budget.json", public_budget), ("digest.json", public_digest)):
        with open(out / name, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=1)
            f.write("\n")
        print(f"{name}: {len(rows)} rows")


if __name__ == "__main__":
    main()
