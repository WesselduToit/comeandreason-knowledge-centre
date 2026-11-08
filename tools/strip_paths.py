"""Replace local drive paths in page data with short, machine-independent forms.

Usage:  python tools/strip_paths.py            (rewrites data/pages/*.json in place)
        python tools/strip_paths.py --check    (reports remaining drive paths, exit 1 if any)

"C:\\Personal\\Religion\\Blogs\\comeandreason_corpus\\posts\\2011-10-21--x.md"  ->  "posts/2011-10-21--x.md"
"C:\\Personal\\Books\\_ocr_markdown\\GodShapedHeart.md"                        ->  "_ocr_markdown/GodShapedHeart.md"
The source chips already display only the last two path segments, so built pages look the same;
the full paths simply no longer exist anywhere in the repository or the published site.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
# A Windows drive path: a lone letter, a colon and a backslash (so "https://" never matches).
DRIVE = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:\\(?:[^\\/\s\"'<>|]+\\)*[^\\/\s\"'<>|]*")


def shorten(path: str) -> str:
    parts = [p for p in re.split(r"[\\/]", path) if p]
    return "/".join(parts[-2:]) if len(parts) >= 2 else path


def strip_text(s: str) -> str:
    return DRIVE.sub(lambda m: shorten(m.group(0)), s)


def walk(obj):
    if isinstance(obj, dict):
        return {k: walk(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [walk(v) for v in obj]
    if isinstance(obj, str) and DRIVE.search(obj):
        return strip_text(obj)
    return obj


def main(check: bool) -> int:
    bad = 0
    for f in sorted((ROOT / "data" / "pages").glob("*.json")):
        raw = f.read_text(encoding="utf-8")
        hits = len(DRIVE.findall(raw))
        if check:
            if hits:
                print(f"{f.name}: {hits} drive paths remain")
                bad += hits
            continue
        if not hits:
            print(f"{f.name}: clean")
            continue
        data = walk(json.loads(raw))
        f.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{f.name}: shortened {hits} drive paths")
    if check:
        print("no drive paths remain" if not bad else f"{bad} drive paths remain")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main("--check" in sys.argv))
