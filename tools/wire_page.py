"""Wire a built page into the hub, the search index, the sibling credit lines and the README.

Usage:
  python tools/wire_page.py <slug> --title "..." --short "..." --pitch "..." --pillar "..." --nodes wrath,law [--planned "Wrath = Letting Go"] [--credit-text "..."]

Does, idempotently:
  1. tools/build_index.py: adds the slug to PAGES and TITLES
  2. src/pages/index.html: adds 'cr-<slug>-' to the hub's PREFIX map (saved-answers panel)
  3. data/pages/index.json: appends a pages.built entry and drops the matching planned entry
  4. src/pages/*.html (other generated pages): appends a link to the credit line
  5. README.md: adds a row to the page table
Then rebuild: python tools/build_index.py && python tools/build_page.py index <siblings...>
"""
import argparse
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--title", required=True)
    ap.add_argument("--short", required=True)
    ap.add_argument("--pitch", required=True)
    ap.add_argument("--pillar", required=True)
    ap.add_argument("--nodes", required=True, help="comma-separated hub node ids: lie,trust,fear,law,wrath,remedy,healing,growing")
    ap.add_argument("--planned", default=None, help="substring of the roadmap title to remove from the hub's planned list")
    ap.add_argument("--credit-text", default=None, help="link text in sibling credit lines (default: --short)")
    a = ap.parse_args()
    slug, credit_text = a.slug, a.credit_text or a.short

    # 1. build_index.py
    p = ROOT / "tools" / "build_index.py"
    s = p.read_text(encoding="utf-8")
    if f'"{slug}"' not in s:
        s = re.sub(r'PAGES = \[(.*?)\]', lambda m: f'PAGES = [{m.group(1)}, "{slug}"]', s, count=1)
        s = s.replace('    "seven-levels": "The Seven Levels of Moral Development",\n', f'    "{slug}": {json.dumps(a.title, ensure_ascii=False)},\n    "seven-levels": "The Seven Levels of Moral Development",\n')
        p.write_text(s, encoding="utf-8"); print("build_index.py: added", slug)
    else:
        print("build_index.py: already has", slug)

    # 2. hub PREFIX map
    p = ROOT / "src" / "pages" / "index.html"
    s = p.read_text(encoding="utf-8")
    if f"'cr-{slug}-'" not in s:
        s = s.replace("hub: 'cr-hub-' }", f"'{slug}': 'cr-{slug}-', hub: 'cr-hub-' }}", 1)
        p.write_text(s, encoding="utf-8"); print("index.html: PREFIX has", slug)

    # 3. hub data
    p = ROOT / "data" / "pages" / "index.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    if not any(b["slug"] == slug for b in d["pages"]["built"]):
        d["pages"]["built"].append({"slug": slug, "title": a.title, "short": a.short, "pitch": a.pitch, "pillar": a.pillar,
                                    "nodes": [n.strip() for n in a.nodes.split(",") if n.strip()], "status": "built", "page_authored": True})
        if a.planned:
            before = len(d["pages"]["planned"])
            d["pages"]["planned"] = [x for x in d["pages"]["planned"] if a.planned.lower() not in x["title"].lower()]
            print(f"index.json: planned {before} -> {len(d['pages']['planned'])}")
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8"); print("index.json: built +=", slug)

    # 4. sibling credit lines
    link = f'<a href="{slug}.html">{credit_text}</a>'
    for f in sorted((ROOT / "src" / "pages").glob("*.html")):
        if f.stem in (slug, "index"):
            continue
        s = f.read_text(encoding="utf-8")
        if f'href="{slug}.html"' in s:
            continue
        m = re.search(r'<p class="credit">.*?</p>', s, re.S)
        if not m:
            print(f.stem, ": no credit line"); continue
        credit = m.group(0)
        s = s.replace(credit, credit[:-4].rstrip() + " and " + link + "</p>", 1)
        f.write_text(s, encoding="utf-8"); print(f.stem, "linked")

    # 5. README row
    r = ROOT / "README.md"
    s = r.read_text(encoding="utf-8")
    if f"dist/{slug}.html" not in s:
        lines = s.split("\n")
        i = max(idx for idx, l in enumerate(lines) if l.startswith("| ") and "dist/" in l)
        lines.insert(i + 1, f"| {a.title} | `dist/{slug}.html` | built from `src/pages/{slug}.html` + `data/pages/{slug}.json` |")
        r.write_text("\n".join(lines), encoding="utf-8"); print("README row added")
    print("now run: python tools/build_index.py && python tools/build_page.py index", slug, "<siblings>")


if __name__ == "__main__":
    main()
