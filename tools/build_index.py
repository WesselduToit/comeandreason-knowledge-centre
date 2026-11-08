"""Build data/search_index.json: a cross-page index for the hub's global search.

Usage:  python tools/build_index.py
For every generated page (src/pages/<p>.html + data/pages/<p>.json) it records
  - sections   (h2 text  -> #sN)
  - glossary terms (term + meaning -> #sources)
  - scripture references found in the page data (-> the section whose fill() reads that data key)
  - topic titles (title/term/name/label fields inside the data -> owning section)
plus the hand-made seven-levels.html (sections and level names scraped from the file).
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAGES = ["fire", "two-lenses", "dominoes", "seven-reasons", "sin-disease", "wrath", "four-judgments"]
TITLES = {
    "fire": "The Consuming Fire",
    "two-lenses": "Two Lenses: the Biblical Keyword Switcher",
    "dominoes": "The Falling Dominoes",
    "seven-reasons": "Same Act, Seven Reasons",
    "sin-disease": "Sin Is a Disease: symptom or condition?",
    "wrath": "Wrath = Letting Go",
    "four-judgments": "The Four Judgments",
    "seven-levels": "The Seven Levels of Moral Development",
}
BOOKS = (
    "Genesis|Exodus|Leviticus|Numbers|Deuteronomy|Joshua|Judges|Ruth|Samuel|Kings|Chronicles|Ezra|Nehemiah|Esther|Job|"
    "Psalms?|Proverbs|Ecclesiastes|Song of Songs|Song of Solomon|Isaiah|Jeremiah|Lamentations|Ezekiel|Daniel|Hosea|Joel|Amos|"
    "Obadiah|Jonah|Micah|Nahum|Habakkuk|Zephaniah|Haggai|Zechariah|Malachi|Matthew|Mark|Luke|John|Acts|Romans|Corinthians|"
    "Galatians|Ephesians|Philippians|Colossians|Thessalonians|Timothy|Titus|Philemon|Hebrews|James|Peter|Jude|Revelation|"
    "Gen|Ex|Lev|Num|Deut|Ps|Prov|Isa|Jer|Ezek|Dan|Hos|Mal|Matt|Rom|Cor|Gal|Eph|Phil|Col|Thess|Tim|Heb|Pet|Rev"
)
REF_RE = re.compile(rf"\b((?:[123] ?)?(?:{BOOKS})\.? \d{{1,3}}(?::\d{{1,3}}(?:[-–]\d{{1,3}})?)?)")
TITLE_KEYS = {"title", "term", "name", "label", "heading", "short", "objection", "scenario", "act"}
SKIP_TOP = {"meta", "sources", "page_authored_fields", "link_ids"}


def strip_tags(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


def section_map(tpl: str):
    """Return (sections[(id, title)], div->section, datakey->section)."""
    sections, div2sec = [], {}
    for m in re.finditer(r'<section[^>]*id="([^"]+)"[^>]*>(.*?)</section>', tpl, re.S):
        sid, body = m.group(1), m.group(2)
        h = re.search(r"<h2[^>]*>(.*?)</h2>", body, re.S)
        title = strip_tags(re.sub(r'<span class="num">.*?</span>', "", h.group(1))) if h else ""
        sections.append((sid, title))
        for d in re.findall(r'<div[^>]*\bid="([^"]+)"', body):
            div2sec[d] = sid
    key2sec = {}
    fills = list(re.finditer(r"fill\('([A-Za-z0-9_]+)'", tpl))
    for i, f in enumerate(fills):
        end = fills[i + 1].start() if i + 1 < len(fills) else len(tpl)
        body = tpl[f.end():end]
        sec = div2sec.get(f.group(1))
        if not sec:
            continue
        for k in re.findall(r"\bD\.([A-Za-z_][A-Za-z0-9_]*)", body):
            key2sec.setdefault(k, sec)
    return sections, div2sec, key2sec


def walk(obj, path=()):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk(v, path + (k,))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk(v, path + (i,))
    else:
        yield path, obj


def index_page(page: str):
    tpl = (ROOT / "src" / "pages" / f"{page}.html").read_text(encoding="utf-8")
    data = json.loads((ROOT / "data" / "pages" / f"{page}.json").read_text(encoding="utf-8"))
    sections, _, key2sec = section_map(tpl)
    entries, seen = [], set()

    def add(kind, title, anchor, text=""):
        key = (kind, title.lower(), anchor)
        if not title or key in seen:
            return
        seen.add(key)
        entries.append({"page": page, "kind": kind, "title": title, "anchor": anchor, "text": text[:160]})

    for sid, title in sections:
        if title:
            add("section", title, f"#{sid}")
    for g in data.get("glossary") or []:
        if isinstance(g, dict) and g.get("term"):
            add("term", str(g["term"]), "#sources", str(g.get("meaning") or ""))
    for path, val in walk(data):
        if not path or path[0] in SKIP_TOP or path[0] == "glossary":
            continue
        top = path[0]
        anchor = "#" + key2sec.get(top, sections[0][0] if sections else "")
        if isinstance(val, str):
            last = path[-1]
            if last == "ref" or (isinstance(last, str) and last.endswith("_ref")):
                for r in REF_RE.findall(val):
                    add("verse", r.replace("–", "-"), anchor)
            elif last in TITLE_KEYS and 3 <= len(val) <= 90 and not val.endswith("."):
                add("topic", val, anchor)
        # dict keys that are themselves references (e.g. scriptures_remedy["Genesis 3:4"])
        if isinstance(path[-1], str) and REF_RE.fullmatch(path[-1].strip()):
            add("verse", path[-1].strip(), anchor)
    return entries


def index_seven_levels():
    f = ROOT / "dist" / "seven-levels.html"
    if not f.exists():
        return []
    html = f.read_text(encoding="utf-8")
    entries = []
    for m in re.finditer(r'<section[^>]*id="([^"]+)"[^>]*>(.*?)</section>', html, re.S):
        h = re.search(r"<h2[^>]*>(.*?)</h2>", m.group(2), re.S)
        if h:
            entries.append({"page": "seven-levels", "kind": "section", "title": strip_tags(h.group(1)), "anchor": f"#{m.group(1)}", "text": ""})
    # level names: look for objects with a name/title and a numeric level in the inline script
    names = re.findall(r"""(?:name|title)\s*:\s*['"]([^'"]{3,60})['"]""", html)
    for n in dict.fromkeys(names):
        entries.append({"page": "seven-levels", "kind": "topic", "title": n, "anchor": "#levels", "text": ""})
    return entries


def main():
    entries = []
    for p in PAGES:
        if (ROOT / "src" / "pages" / f"{p}.html").exists() and (ROOT / "data" / "pages" / f"{p}.json").exists():
            e = index_page(p)
            print(f"{p}: {len(e)} entries")
            entries += e
    e = index_seven_levels()
    print(f"seven-levels: {len(e)} entries")
    entries += e
    out = {"pages": {p: {"title": TITLES.get(p, p), "file": f"{p}.html"} for p in PAGES + ["seven-levels"]}, "entries": entries}
    path = ROOT / "data" / "search_index.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=0), encoding="utf-8")
    kinds = {}
    for x in entries:
        kinds[x["kind"]] = kinds.get(x["kind"], 0) + 1
    print(f"wrote {path} ({path.stat().st_size:,} bytes): {len(entries)} entries {kinds}")


if __name__ == "__main__":
    main()
