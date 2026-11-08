"""Merge the four authored/verified parts into data/pages/fire.json and run sanity checks.

Usage: python tools/merge_fire.py <parts-dir>
Parts: texts.json, wrath-endtime.json, angel-brain-levels.json, objections-glossary.json
Checks: every Remedy quotation matches docs/remedy_verses.json (after normalising whitespace/quotes);
        every source.file path exists. Problems are printed, not fatal.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PARTS = ["texts", "wrath-endtime", "angel-brain-levels", "objections-glossary"]


def norm(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace("…", "...")
    return re.sub(r"\s+", " ", s).strip().lower()


def load_remedy():
    verses = json.loads((ROOT / "docs" / "remedy_verses.json").read_text(encoding="utf-8"))
    return "\n".join(norm(v["text"]) for v in verses)


def walk(obj, path="$"):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk(v, f"{path}[{i}]")
    else:
        yield path, obj


def main(parts_dir: pathlib.Path):
    merged = {}
    for p in PARTS:
        f = parts_dir / f"{p}.json"
        if not f.exists():
            print(f"MISSING part {f}")
            continue
        data = json.loads(f.read_text(encoding="utf-8"))
        for k, v in data.items():
            if k in merged:
                print(f"WARN duplicate top-level key {k} from {p}")
            merged[k] = v
        print(f"{p}: keys {list(data.keys())}")

    # drop author/verifier bookkeeping keys that are not page content
    for k in ("part", "conventions", "sections_covered", "notes", "unverified", "_meta"):
        merged.pop(k, None)

    # relocate any source files that live in the session scratchpad into data/sources so citations survive
    scratch = str(parts_dir.parent.parent).lower()
    relocated = {}

    def relocate(obj):
        if isinstance(obj, dict):
            for k, v in list(obj.items()):
                obj[k] = relocate(v)
            return obj
        if isinstance(obj, list):
            return [relocate(v) for v in obj]
        if isinstance(obj, str) and obj.lower().startswith(scratch):
            src = pathlib.Path(obj)
            if src.exists() and src.is_file():
                rel = src.relative_to(parts_dir.parent.parent)
                dest = ROOT / "data" / "sources" / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                if not dest.exists():
                    dest.write_bytes(src.read_bytes())
                relocated[obj] = str(dest)
                return str(dest)
        return obj

    merged = relocate(merged)
    print(f"relocated {len(relocated)} scratchpad source paths into data/sources")

    remedy_blob = load_remedy()
    bad_remedy, bad_paths, checked = [], [], 0
    for path, val in walk(merged):
        if not isinstance(val, str):
            continue
        if path.endswith(".file") and ("\\" in val or "/" in val):
            if not pathlib.Path(val).exists():
                bad_paths.append((path, val))
        if ".remedy" in path and (path.endswith(".text") or path.endswith(".remedy")) and len(val) > 20:
            checked += 1
            snippet = norm(val)[:120]
            if snippet not in remedy_blob:
                bad_remedy.append((path, val[:80]))

    out = ROOT / "data" / "pages" / "fire.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(merged, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nwrote {out} ({out.stat().st_size:,} bytes); top-level keys: {sorted(merged)}")
    print(f"remedy quotations checked: {checked}, not matching verbatim: {len(bad_remedy)}")
    for p, v in bad_remedy[:40]:
        print("  REMEDY?", p, "::", v)
    print(f"source paths missing: {len(bad_paths)}")
    for p, v in bad_paths[:40]:
        print("  PATH?", p, "::", v)
    counts = {k: (len(v) if isinstance(v, (list, dict)) else 1) for k, v in merged.items()}
    print("counts:", counts)


if __name__ == "__main__":
    main(pathlib.Path(sys.argv[1]))
