"""Build a single-file page from src/pages/<name>.html + src/kit + data/pages/<name>.json.

Usage:  python tools/build_page.py fire
Markers in the template:
  <!-- @kit.css -->   -> <style>contents of src/kit/kit.css</style>
  <!-- @kit.js -->    -> <script>contents of src/kit/kit.js</script>
  <!-- @data -->      -> <script>window.PAGE_DATA = {...json...}</script>
  <!-- @index -->     -> <script>window.SEARCH_INDEX = {...}</script>  (optional; from data/search_index.json)
Output: dist/<name>.html
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def build(name: str) -> pathlib.Path:
    tpl_path = ROOT / "src" / "pages" / f"{name}.html"
    data_path = ROOT / "data" / "pages" / f"{name}.json"
    css = (ROOT / "src" / "kit" / "kit.css").read_text(encoding="utf-8")
    js = (ROOT / "src" / "kit" / "kit.js").read_text(encoding="utf-8")
    tpl = tpl_path.read_text(encoding="utf-8")
    data = {}
    if data_path.exists():
        data = json.loads(data_path.read_text(encoding="utf-8"))
    # </script> inside JSON strings would terminate the script block early.
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    out = (
        tpl.replace("<!-- @kit.css -->", f"<style>\n{css}\n</style>")
        .replace("<!-- @kit.js -->", f"<script>\n{js}\n</script>")
        .replace("<!-- @data -->", f"<script>window.PAGE_DATA = {payload};</script>")
    )
    # Optional: the hub inlines the cross-page search index built by tools/build_index.py.
    if "<!-- @index -->" in out:
        idx_path = ROOT / "data" / "search_index.json"
        idx = json.loads(idx_path.read_text(encoding="utf-8")) if idx_path.exists() else {}
        idx_payload = json.dumps(idx, ensure_ascii=False).replace("</", "<\\/")
        out = out.replace("<!-- @index -->", f"<script>window.SEARCH_INDEX = {idx_payload};</script>")
    for marker in ("<!-- @kit.css -->", "<!-- @kit.js -->", "<!-- @data -->", "<!-- @index -->"):
        assert marker not in out
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    out_path = dist / f"{name}.html"
    out_path.write_text(out, encoding="utf-8")
    return out_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: build_page.py <page-name>")
    for page in sys.argv[1:]:
        path = build(page)
        print(f"built {path} ({path.stat().st_size:,} bytes)")
