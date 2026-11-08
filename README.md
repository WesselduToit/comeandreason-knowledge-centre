# Come and Reason Knowledge Centre

Interactive, single-file HTML explainers of Dr Timothy R. Jennings' (Come and Reason) teaching, built from the local corpus on this laptop.

## Open the pages

Everything in `dist/` opens straight from disk (double-click) or from any static server:

```
python -m http.server 8777 --directory dist
```

| Page | File | Status |
|---|---|---|
| **Hub: start here** (lens diagnostic, the causal chain, page cards, search over every page, saved answers) | `dist/index.html` | built from `src/pages/index.html` + `data/pages/index.json` + `data/search_index.json` |
| The Seven Levels of Moral Development | `dist/seven-levels.html` | hand-made first page (downloaded from a chat artifact, 2026-11-08) |
| The Consuming Fire | `dist/fire.html` | built from `src/pages/fire.html` + `data/pages/fire.json` |
| Two Lenses: the Biblical Keyword Switcher | `dist/two-lenses.html` | built from `src/pages/two-lenses.html` + `data/pages/two-lenses.json` |
| The Falling Dominoes and the Healing Cascade | `dist/dominoes.html` | built from `src/pages/dominoes.html` + `data/pages/dominoes.json` |
| Same Act, Seven Reasons (Seven Levels companion) | `dist/seven-reasons.html` | built from `src/pages/seven-reasons.html` + `data/pages/seven-reasons.json` |
| Sin Is a Disease: symptom or condition? (plus the Atonement Prism) | `dist/sin-disease.html` | built from `src/pages/sin-disease.html` + `data/pages/sin-disease.json` (atonement-by-level ladder reused from seven-reasons.json) |
| Wrath = Letting Go (the mechanism beneath Fire) | `dist/wrath.html` | built from `src/pages/wrath.html` + `data/pages/wrath.json` (reuses the Fire page's verified wrath data) |
| The Four Judgments (who is judging whom?) | `dist/four-judgments.html` | built from `src/pages/four-judgments.html` + `data/pages/four-judgments.json` (reuses the Fire page's end-time sequence and seven-level hearing of Rev 20:12, and the Wrath page's SDA commentary quotation) |
| Heavenly Records: rap sheet or medical chart? | `dist/records.html` | built from `src/pages/records.html` + `data/pages/records.json` (reuses the Four Judgments page's ledger-or-medical-record flip cards and the Fire page's seven-level hearing of Rev 20:12) |
| God's Design Laws Lab | `dist/lab.html` | built from `src/pages/lab.html` + `data/pages/lab.json` |

## Build a page

```
python tools/build_page.py fire
```

To add a finished page to the hub, the search index, the sibling credit lines and this table in one step:

```
python tools/wire_page.py <slug> --title "..." --short "..." --pitch "..." --pillar "..." --nodes law,healing --planned "<roadmap title>"
```

The hub (`index`) also inlines a cross-page search index; regenerate it whenever a page's data changes, then rebuild the hub:

```
python tools/build_index.py
python tools/build_page.py index
```

Content for a page is authored as JSON parts by subagents, fact-checked, then merged with `python tools/merge_parts.py <page> <parts-dir> <part>...` (checks Remedy quotations against `docs/remedy_verses.json`, copies any scratchpad source texts into `data/sources/`).

The build inlines `src/kit/kit.css`, `src/kit/kit.js` and `data/pages/<page>.json` into `src/pages/<page>.html` at the `<!-- @kit.css -->`, `<!-- @kit.js -->` and `<!-- @data -->` markers and writes `dist/<page>.html`. Templates contain no prose; all content lives in the page's JSON.

## Publishing (GitHub Pages)

`dist/` is the whole site. Pushing to `main` runs `.github/workflows/pages.yml`, which uploads `dist/` as the Pages artifact (no build on GitHub; build locally, commit the result). Adding a page is: build it, run `python tools/build_index.py` and `python tools/build_page.py index` so the hub includes it, commit, push.

Kept out of the repository by `.gitignore`: `data/sources/` (copies of tract and book extracts) and `docs/remedy_verses.json` (the full Remedy text). Page data stores source files as `folder/file` only (`tools/strip_paths.py`, applied automatically by `merge_parts.py`), so no local paths are published. `dist/.nojekyll` makes Pages serve the files untouched.

## Layout

```
dist/            built pages (open these)
src/kit/         shared components: lens toggle, verse cards + explorer, timeline, sort bins, flip pairs, accordion, level stepper, glossary popovers, poll, journal boxes
src/pages/       one template per page; a page script maps its JSON onto the kit renderers
data/pages/      one JSON per page, authored and fact-checked against the corpus
docs/            the proposal (roadmap of 22 pages), plans, and remedy_verses.json
tools/           build script and corpus parsers
```

## Corpus (read-only, not copied here)

- Blog, 611 posts as markdown: `C:\Personal\Religion\Blogs\comeandreason_corpus\posts\`
- The Remedy (Jennings' paraphrase, Genesis + Psalms + NT): `C:\Personal\Religion\Blogs\remedy_bible_corpus\` — the markdown chapters are missing Jesus' words (red-letter spans were dropped by the scrape). Use `docs/remedy_verses.json` (11,950 verses, re-parsed from `_cache/*.html` by `docs/remedy_reparse.py`) instead.
- Tracts, magazines, study guides: `C:\Personal\Religion\*.pdf`
- Books (OCR): `C:\Personal\Books\_ocr_markdown\GodShapedBrain.md`, `GodShapedHeart.md`
- Lesson notes and media: `C:\Personal\Downloads\Religion\ComeAndReason\`

## Conventions

- Every quotation carries a source chip (source file as `folder/file`, and the comeandreason.com URL where known).
- Remedy text is copied verbatim from `remedy_verses.json`; verses the Remedy does not cover show a "Not in The Remedy" badge.
- Contested readings carry a ⚠ caveat; material from the Truth, Love & Freedom study guide is attributed to its author (Cole), not Jennings.
- The imposed-law / design-law lens is remembered in `localStorage['cr-lens']` and shared by all pages; page state uses the `cr-<page>-` prefix (the hub lists and clears it per page).
- Every page's credit line links back to the hub (`index.html`); the hub's page cards deep-link to each page's sections via the search index.

## Next pages (from `docs/2026-11-08-knowledge-centre-proposal.md`)

Sanctuary, Design Laws Lab, Parables, Two Covenants, Brain Map, Clinic self-checks, Cosmic Conflict in 13 weeks.
