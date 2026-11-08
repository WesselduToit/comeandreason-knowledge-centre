"""Generic merge of authored/verified JSON parts into data/pages/<page>.json with sanity checks.

Usage: python tools/merge_parts.py <page> <parts-dir> <part> [<part> ...]
- drops bookkeeping keys (part, conventions, sections_covered, notes, unverified, _meta)
- relocates any source file that lives in the session scratchpad into data/sources/
- checks Remedy quotations against docs/remedy_verses.json and that source.file paths exist
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DROP = ("part", "conventions", "sections_covered", "notes", "unverified", "_meta")


def norm(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace("…", "...")
    return re.sub(r"\s+", " ", s).strip().lower()


def walk(obj, path="$"):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk(v, f"{path}[{i}]")
    else:
        yield path, obj


def main(page: str, parts_dir: pathlib.Path, parts: list[str]):
    merged = {}
    for p in parts:
        f = parts_dir / f"{p}.json"
        if not f.exists():
            print(f"MISSING part {f}")
            continue
        data = json.loads(f.read_text(encoding="utf-8"))
        for k, v in data.items():
            if k in DROP:
                continue
            if k in merged:
                print(f"WARN duplicate top-level key {k} from {p}")
            merged[k] = v
        print(f"{p}: keys {[k for k in data if k not in DROP]}")

    scratch_root = parts_dir.parent.parent
    scratch = str(scratch_root).lower()
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
                dest = ROOT / "data" / "sources" / src.relative_to(scratch_root)
                dest.parent.mkdir(parents=True, exist_ok=True)
                if not dest.exists():
                    dest.write_bytes(src.read_bytes())
                relocated[obj] = str(dest)
                return str(dest)
        return obj

    merged = relocate(merged)
    print(f"relocated {len(relocated)} scratchpad source paths into data/sources")

    verses = json.loads((ROOT / "docs" / "remedy_verses.json").read_text(encoding="utf-8"))
    blob = " ".join(norm(v["text"]) for v in verses)
    bad_remedy, bad_paths, checked = [], [], 0
    for path, val in walk(merged):
        if not isinstance(val, str):
            continue
        if path.endswith(".file") and ("\\" in val or "/" in val) and not pathlib.Path(val).exists():
            bad_paths.append((path, val))
        if ".remedy" in path and (path.endswith(".text") or path.endswith(".remedy")) and len(val) > 20:
            checked += 1
            n = norm(val)
            windows = [n[i:i + 60] for i in range(0, max(1, len(n) - 60), 40)]
            if not all(w in blob for w in windows):
                bad_remedy.append((path, val[:80]))

    out = ROOT / "data" / "pages" / f"{page}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(merged, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nwrote {out} ({out.stat().st_size:,} bytes); keys: {sorted(merged)}")
    print(f"remedy quotations checked: {checked}, with a 60-char window not found: {len(bad_remedy)}")
    for p, v in bad_remedy[:40]:
        print("  REMEDY?", p, "::", v)
    print(f"source paths missing: {len(bad_paths)}")
    for p, v in bad_paths[:40]:
        print("  PATH?", p, "::", v)


if __name__ == "__main__":
    main(sys.argv[1], pathlib.Path(sys.argv[2]), sys.argv[3:])
