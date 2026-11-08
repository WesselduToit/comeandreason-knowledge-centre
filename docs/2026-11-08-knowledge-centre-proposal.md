# Come and Reason Knowledge Centre: proposal

Synthesis of five corpus slices (blog, Remedy, tracts, books, lessons), three independent judge passes and the Fire deep-dive. Everything below is grounded in files on this laptop; paths are absolute.

**Status of the misplaced Seven Levels HTML page:** not found. Searches of `C:\Personal`, `C:\Claude`, OneDrive, Documents, Downloads and Desktop for `*.html` containing "moral development" / "seven levels" only hit blog-cache files and an unrelated "Virtuous Path" codex. Its source document is confirmed: `C:\Personal\Religion\SevenLevelsOfMoralDevelopment.pdf` (also `C:\Personal\Downloads\Religion\ComeAndReason\Documents To Print\SevenLevels_Complete.pdf`), the 3-page handout mapping L1 Reward & punishment = Satisfaction theory ... L7 Understanding friend of God = Healing Substitution. Before building anything else, run one targeted sweep (see section 5.4); if it does not surface, the page is cheap to rebuild from that PDF plus God-Shaped Heart ch.3 and the shared kit below.

---

## 1. Corpus at a glance

| Slice | Location | Size | Text-ready? | Notes |
|---|---|---|---|---|
| Blog (comeandreason.com) | `C:\Personal\Religion\Blogs\comeandreason_corpus\posts\*.md` (+ `come_and_reason_blog_archive.md`, `manifest.jsonl`) | 611 posts, 2007-11 to 2026-08, ~950k words | Yes | Each post has a `BLOG_POST_METADATA` block (title, url, published, word_count). Title index: `...\scratchpad\blog_titles.txt`. Key posts already in table/list form: Biblical Keywords (13-row table), Design Laws (nested list), Two Covenants (10-row table), Parables (29 bullets), Prophecy table (20 rows), 12 Steps / 7 Steps / 10 Steps (numbered). |
| The Remedy (Jennings' paraphrase: Genesis, Psalms, NT + Preface) | `C:\Personal\Religion\Blogs\remedy_bible_corpus\` (`chapters\`, `books\`, `the_remedy_bible.md`, `manifest.jsonl`, `_cache\*.html`) | 462 chapter files; 10,540 of 11,950 verses in markdown; 316,646 words after re-parse | Partly | **Markdown dropped all red-letter (Jesus' words) spans**: Matthew 71%, Mark 83%, Luke 68%, John 78% (John 3:16, Sermon on the Mount, Matt 10:28, Mark 9:43-48, Luke 16 absent). `_cache\` holds raw HTML for all 461 chapters with red spans intact; `...\scratchpad\reparse.py` already recovers 11,950 verses into `...\scratchpad\remedy_verses.json`. Genesis, Psalms and all epistles are complete now. Official 2022 DOCX/PDF per book at `C:\Personal\Downloads\Religion\ComeAndReason\The Remedy\` (fallback). |
| Remedy audio | `C:\Personal\Downloads\Religion\ComeAndReason\The Remedy\RemedyNT_MP3\` | 262 MP3, 25.5 h, 64 kbps, NT + Preface only | n/a | No chapter markers or transcripts. User's ElevenLabs per-verse experiment for Genesis 2 (59 clips) at `C:\Personal\Religion\ComeAndReason\The Remedy\11 Labs\`. Genesis questionnaire (126 questions) at `...\The Remedy\01_Questionaire.docx`. |
| Tracts, handouts, magazines, study guides | `C:\Personal\Religion\*.pdf` and `C:\Personal\Religion\Blogs\*.pdf`; duplicates under `C:\Personal\Downloads\Religion\ComeAndReason\Documents To Print\` | 32 PDFs: 10 two-page tracts, 8 magazines, 2 thirteen-week study guides, youth workbook (100 pp), CIBTS book (221 pp), 3 one-page sheets | Yes (31 of 32) | Extracted to `...\scratchpad\tracts\<name>.txt`. Only `28 Fundamerntal Beliefs Through the Design Law Lens.pdf` is image-only (and is a 2010 Genesis Road magazine, not Come and Reason; page PNGs at `...\scratchpad\fb28\`). |
| Books (OCR) | `C:\Personal\Books\_ocr_markdown\GodShapedBrain.md` (2,568 lines), `GodShapedHeart.md` (2,123 lines) | 2 full books, ~950 KB | Yes, with OCR noise | Source was per-page screenshots: headings lost, fi/ffi ligatures dropped, Roman numerals garbled, the Heart ch.5 design-vs-imposed table has interleaved columns, WhatsApp overlay artefacts in Heart ch.13. Content is quotable after a clean-up pass. CIBTS PDF text extracts cleanly (`...\scratchpad\cibts.txt`). |
| Sabbath School class notes + quarterlies | `C:\Personal\Downloads\Religion\ComeAndReason\2021 Q4\`, `2022 Q1\`, `2022 Q2\` | 28 Jennings notes PDFs (~175k words), 39 official Easy-Reading quarterlies | Yes | Extracted to `...\scratchpad\text\`. Q1 Hebrews notes cover lessons 1-4 only. Quarterlies are GC copyright; use only as the "what the lesson says" foil. |
| Truth, Love & Freedom study guides | `C:\Personal\Religion\TruthLoveFreedom_StudyGuide_CosmicConflict.pdf` (213 pp, Cole), `..._DomesticViolence.pdf` (185 pp, Lorren); weekly PDFs at `...\ComeAndReason\WeeklyLessons\` | 2 x 13 weeks x 7 days | Yes | Regular headers (LIVING WORDS / BOTTOM LINE / SETTING THE STAGE / THINK ABOUT IT) parse semi-automatically. `Week09.pdf` missing from WeeklyLessons; the complete guide PDF has it. |
| Video / audio needing transcription | `C:\Personal\Downloads\Religion\ComeAndReason\` (Healing The Mind, 2022 Q2 class + Q&A, Journal of the Watcher, human sexuality, LoveCourse, Q3 L11) + `Could it be this Simple\` audiobook | 44 MP4 = 33.1 h; CIBTS 17 MP3 = 5.2 h | No | faster-whisper 1.2.1 + ctranslate2 already in `C:\Personal\Software\WhisperWorkflow\.venv`; RTX 5060 8 GB; ffmpeg 9.0.2. |
| Existing Seven Levels HTML | unknown | 1 file | - | Not located; see 5.4. |

---

## 2. Knowledge-centre architecture

### 2.1 Shape: one hub, many single-file pages, one shared kit

Every page stays a standalone single-file HTML (the user's existing pattern), but is **generated** from a source template plus shared kit so the components stay consistent. A 40-line Python build script inlines `kit/*.css`, `kit/*.js` and the page's data JSON into `dist/<page>.html`. Pages open from disk with no server.

**Hub (`index.html`)**: not a list of links but a routed entry:
1. A 60-second "which lens do you default to?" diagnostic (5 forced-choice items from the lessons Keyword Switchboard idea plus 4 from the Baylor four-God-images / Keith Johnson's Four Questions in God-Shaped Heart ch.6). Result places the reader on the imposed-law / design-law axis and suggests a starting page.
2. A concept map of the pillars in the causal order Jennings himself uses: **Lie believed -> trust broken -> fear & selfishness -> law misread as imposed -> wrath/fire/judgment misread as punishment -> remedy misread as appeasement -> healing model**. Each node is a page.
3. The existing Seven Levels page is the first node of the "Growing up" pillar and is also the lens selector other pages reuse (section 2.4).
4. Global search across all page data (title, glossary, verse refs).

### 2.2 Shared component kit (build once, reuse everywhere)

| Component | What it does | First used by |
|---|---|---|
| `lens-toggle` | Page-wide switch Imposed law / Design law; every element tagged `data-lens` re-renders (colour: red -> gold). Persists in localStorage so the whole centre remembers the reader's lens. | Two Lenses, Fire, Four Judgments, Records, Sanctuary |
| `verse-card` | Reference, translation text (NIV/GNT as Jennings quotes it), Remedy rendering (from `remedy_verses.json`, with "missing locally" badge), red-letter flag, source chip to the comeandreason URL and local file path, copy-with-reference. | Fire, Wrath, Hard Passages, Law as Diagnostic |
| `remedy-reader` | Book/chapter picker, verse list, lens-highlight dictionaries (medical / design-law / trust-fear / let-go / fire), deep-link by `#John.3.16`. | Remedy Verse Explorer; embedded in any page via `<remedy-ref>` |
| `two-column-flip` | Side-by-side pair that animates between readings (courtroom / clinic; script / reality; what God said / what happened). | Two Lenses, Records, Sanctuary, Wrath |
| `timeline` | Horizontal scrubbable timeline with toggleable layers and per-step question/answer. | Fire gallery, Fire end-time sequence, Four Judgments, Preface, Two Covenants |
| `level-stepper` | The 1-7 slider from the Seven Levels page; emits `level` so any text block tagged with `data-level` re-voices itself. | Seven Levels, Same Act Seven Reasons, Fire section 14 |
| `card-grid` + `flip-card` | Filterable grid with reveal/flip and per-card mini-widget slot. | Design Laws Lab, Parables, Object lessons, Six Kinds of Power |
| `sort-bins` | Drag (or tap-to-assign on touch) tokens into bins with instant feedback. | Fire combustion lab, Two Deaths, Perfectionism, Two Covenants practice sorter, Sin Is a Disease |
| `branch-flow` | Decision-tree walker with back button and summary of path. | Forgiveness & Guilt, Knowing God's Will |
| `assessment` | Likert / paired-statement instrument with scoring, radar or gauge, "reflective, not psychometric" label, local-only storage. | Hub diagnostic, Love or Dependency, Which God are you holding, Babylon self-check |
| `glossary-pop` | Inline term popover fed by `data/glossary.json` (design law, imposed law, wrath, thion, first/second death, ...). | All pages |
| `journal` | localStorage text box with export, used for private reflection prompts. | Closing sections, 12 Steps, Study companions |
| `source-chip` | Small chip: post title + date + URL + local path; "show all sources" switch per page. | All pages |

### 2.3 Data pipeline (from the markdown corpora, run once, re-run when corpora update)

```
tools/
  build_remedy_json.py     _cache/*.html  -> data/remedy_verses.json      (11,950 verses; book keys normalised "1John"->"1 John";
                                                                            keep <p></p> as paragraph flag and Psalm <br/><span class=indent> as line breaks;
                                                                            Genesis 24:29 absent on site itself -> patch from 01_Genesis.docx)
  build_keywords_json.py   BIBLICAL KEYWORDS PDF text + blog 2013-05-12 -> data/keywords.json  (13 terms x {design, imposed}, + 5 axioms per paradigm)
  build_design_laws.py     blog 2019-09-04 + THE DESIGN LAWS OF GOD.pdf + Heart Appendix A -> data/design_laws.json (17 laws, examples, consequences, verses)
  build_seven_levels.py    SevenLevelsOfMoralDevelopment.pdf + Heart ch.3 lines 363-379 + ch.4/7/11/14 tables -> data/seven_levels.json
  build_blog_index.py      posts/manifest.jsonl -> data/blog_index.json (title, date, url, path, word_count) for source chips and "read more"
  build_notes_json.py      scratchpad\text\*.txt -> data/class_notes.json (quarter > lesson > day blocks)
  build_studyguide_json.py Cosmic Conflict PDF text -> data/cosmic_conflict.json (13 weeks x 7 days by header regex)
  build_page.py            src/pages/<name>.html + kit + data -> dist/<name>.html (single file)
```

Page-specific curated data (hand-tagged verse lists, objections, timeline steps) lives in `data/pages/<name>.json` and is authored once; the build script embeds it.

### 2.4 Suggested folder layout

```
C:\Personal\Religion\KnowledgeCentre\
  README.md                      how to build; corpus paths; what is derived vs hand-written
  index.html                     hub (built)
  dist\                          built single-file pages (open these)
    seven-levels.html            the recovered/rebuilt page, re-saved here
    fire.html, two-lenses.html, dominoes.html, ...
  src\
    kit\  lens-toggle.js, verse-card.js, timeline.js, level-stepper.js, assessment.js, sort-bins.js, branch-flow.js, glossary-pop.js, kit.css
    pages\ fire.html, two-lenses.html, ...   (templates referencing kit + data)
  data\
    remedy_verses.json, keywords.json, design_laws.json, seven_levels.json, glossary.json, blog_index.json, class_notes.json, cosmic_conflict.json
    pages\ fire.json, wrath.json, hard-passages.json, ...
    crosslinks.json              page -> page links used by the hub map and "related" footers
  tools\  (scripts above)
  media\  (NOT copied; README points to RemedyNT_MP3 and CIBTS MP3 by absolute path; audio pages reference them relatively via a junction if desired)
```

### 2.5 How the existing Seven Levels page slots in

- Move/copy it to `dist\seven-levels.html` and extract its level definitions into `data/seven_levels.json` so the `level-stepper` can be reused (Fire section 14, Same Act Seven Reasons, Six Kinds of Power all key off the same seven labels).
- Add three outbound links from it: "Same act, seven reasons" (companion), "Roads of the Journey" (self-locating map), and "Judgment through the law lens" (Fire page section 14). The handout's atonement-theory column (Satisfaction / Ransom / Governmental / Penal Substitution / Moral Influence / Recapitulation-Christus Victor / Healing Substitution) becomes the bridge to the Healing Model page.
- If the file never surfaces, rebuild it in a half day from `SevenLevelsOfMoralDevelopment.pdf` + `GodShapedHeart.md` lines 363-400 (level definitions with Israel-history correlates: Egypt slaves / Sinai eye-for-eye / Israel wanting kings / Pharisees "we have a law" / Jesus touching lepers / apostles after Pentecost / John 15:15 friends) + blog `2014-12-12--why-did-god-use-law.md`.

---

## 3. Ranked roadmap (22 pages, merged and deduplicated)

Scoring consensus across the three judges; duplicates merged (5 fire candidates -> 1, 4 keyword switchers -> 1, 6 sanctuary/records -> 2, etc.). Effort: S = half day, M = 1-2 days, L = 3+ days or blocked on data work. **BUILD NEXT** marks the top five.

### Pillar A. Foundations and method

**1. Two Lenses: the Biblical Keyword Switcher** — BUILD NEXT (#2)
- Pitch: the master move of the whole system in one toggle: 13 theological terms re-defined under design law vs imposed/imperial law.
- Interaction: `lens-toggle` re-renders the whole page; per-term cards (Justification, Judgment by God, Forgiveness, Salvation, Atonement, Satisfaction, Justice, Vengeance, Wrath, Anger, Heavenly Records, Ransom) with the five axioms of each paradigm as header (protocols vs arbitrary rules; inherent damage vs external punishment; God heals vs inflicts; problem = sin in man vs wrath in God; Christ died to remedy man vs appease God). Tab 2 "Doctrines": 15 doctrine/story cards that flip (robe of righteousness, advocate, intercessor, sins erased, washed in blood, Gen 3 curse, David & Bathsheba, Rev 14:7) from God-Shaped Heart. Tab 3: entry quiz "which lens do you default to?" and exit quiz "spot the lens" using Two Pictures of God statements. Warm-up: the Newton's-laws nine-question quiz (Heart ch.4) proving laws are descriptive.
- Sources: `C:\Personal\Religion\BIBLICAL KEYWORDS COMPARING DEFINITIONS.pdf` (canonical text; identical to The Lie Addendum A pp. 58-59); `posts\2013-05-12--biblical-keywords-comparing-definitions.md`; `GodShapedHeart.md` ~640-663 (contrast table, needs de-interleaving), ~1740-1750 (five doctrines), 562-580 (Newton quiz); `posts\2010-04-28--two-pictures-of-god.md`.
- Readiness: ready now. Effort: **S**.

**2. Why Another Paraphrase? The Preface timeline (front door)**
- Pitch: the Constantine story every other page assumes: design law in the early church -> Constantine 313 -> Eusebius -> "trained Roman lawyers" (Lindsay) -> imposed-law translations -> The Remedy.
- Interaction: `timeline` with hotspots (Justin Martyr, Irenaeus, Constantine, Eusebius, Tertullian/Cyprian/Augustine, Reformation, Remedy); respiration animation (give CO2, receive O2; tie a bag over the loop and it dies); footnote 6's Catholic vs Protestant Decalogue widget; listen-along with `00_Preface\PREFACE_00.mp3` (11 min).
- Sources: `remedy_bible_corpus\chapters\01--preface--000.md` (1,741 words, 6 footnotes); `GodShapedBrain.md` ~972-1006 ("God's Law and How We Have Been Deceived", Dan 7:25 misdirection); `GodShapedHeart.md` Appendix B.
- Readiness: fully ready. Effort: **S**.

**3. Scripture, Science, Experience: the Integrative Evidence Venn (method page)**
- Pitch: click any region of the three circles and see what fails when a leg is missing (science+experience without Scripture = godlessness; Scripture+experience without science = mysticism/fanaticism; Scripture+science without experience = 34,000 denominations).
- Interaction: clickable SVG Venn; "test a claim" worksheet (tick which legs a belief rests on, get the diagnosis); case studies (Galileo, flat earth, eastern meditation, consensus statements); Learn-to-Discern steps and 8 steps for Bible study as drawers.
- Sources: `C:\Personal\Religion\IntegrativeEvidence.pdf`; `posts\2019-11-05--the-integrative-evidence-based-approach-to-finding-truth.md`; `2020-07-14--learn-to-discern...md`; `2023-04-13--evidence-and-history-or-claims-and-wonders.md`; `2010-09-13--8-steps-for-successful-bible-study.md`; `2020-05-20--flat-earthers...md`.
- Readiness: ready. Effort: **S**.

**4. God's Design Laws Lab**
- Pitch: 17 design laws as cards you can "break" and watch the inherent consequence.
- Interaction: `card-grid` (love/giving, liberty, worship, exertion, physics, maths, health, restoration, sowing & reaping, love overcoming fear, fear damaging love, forgiveness vs resentment, truth, revelation, happiness, brokenness, sin & death). Per-law mini-widget: liberty = control slider revealing the three consequences (love destroyed, rebellion instilled, individuality eroded) with Joe/Lynda/Joni presets; love = circle-of-giving animation (water cycle, respiration, blood, economy; break the circle and flow stops: plastic bag, Dead Sea); gravity = 5-inch curb vs 500-ft building degree-of-violation slider; truth = embrace/reject fork; worship = "what you behold" picker. Flagship deep-dive tab: **Survival-of-the-fittest vs the Circle of Giving** (41 Remedy verses: Rom 8:7 "I love myself so much that I will kill you in order that I may live", Eph 2:2-3, Luke 12:23, the four "lose your life to save it" renderings) with a "which principle am I running on?" self-check.
- Sources: `C:\Personal\Religion\THE DESIGN LAWS OF GOD.pdf` (verbatim 17); `posts\2019-09-04--the-design-laws-of-god.md`; `GodShapedHeart.md` 1933-2042 (Appendix A), 389-400 (exertion), 906-935 (worship); `GodShapedBrain.md` 426-447 (liberty "test it on your spouse"); `CIBTS_English+Cover.pdf` ch.5; Remedy `09--romans--008.md`, `13--ephesians--002.md`, `23--james--004.md`, `02--genesis--006.md`.
- Readiness: text ready; 17 small widgets are the cost. Effort: **M**.

### Pillar B. The problem: the lie, broken trust, fear and selfishness

**5. The Falling Dominoes and the Healing Cascade** — BUILD NEXT (#3)
- Pitch: the causal model of the entire teaching, stated in Jennings' own first-person captions: lie believed -> broken love/trust -> fear & selfishness -> acts of sin -> damage and death; and its mirror: truth believed -> trust -> love poured in (Rom 5:5) -> acts of love -> growth.
- Interaction: press "believe the lie" and the dominoes fall with captions; press "believe the truth" and the chain reverses. Case picker highlights which link each story illustrates (Vince, Laura "God took your mommy", Fran "no questions", Savannah, John White/Daniel Cicciaro, the reader's divorce email, Rwanda 1994). The spouse-affair-lie thought experiment runs as a 4-step branching script. Names the lie explicitly (Gen 3:4-5 "you will not surely die" + "God is withholding") so the page also covers the missing "What was the original lie?" topic, pulling from The Lie magazine ch. 2 and Cosmic Conflict weeks 1-2.
- Sources: `GodShapedBrain.md` ~255-287 (Origin of Fear), 572-586 (Romans 7 neuro-paraphrase); `GodShapedHeart.md` ~1423-1452, ~1765-1775; `C:\Personal\Religion\The_Lie_Magazine_Web.pdf` (chapters "The Lie", "The Church Corrupted"); `posts\2011-08-18--the-never-ending-lie-you-will-not-surely-die.md`; `2019-01-10--the-lie-that-led-to-penal-substitution-theology.md`; Cosmic Conflict guide Weeks 1-2.
- Readiness: both cascades are explicit bullet lists. Effort: **S-M**.

**6. Genesis 3: What Changed in Eden**
- Pitch: verse-by-verse walkthrough of the Fall in the Remedy's telling with live Trust / Fear / Selfishness / Shame meters.
- Interaction: step through 24 verses; meters update per verse; hover glosses on interpretive additions ("a beautiful flying creature", "not wanting to frighten them, called out gently", "fiery radiance", "to limit the suffering of sin"); blame-chain animation for 3:12-13; final card ties 3:15 to Heb 2:14 and 3:22-24 to Rev 22. Embedded quiz: the Genesis-chapter-3 questions from the Questionaire. Grows later into the full Genesis Origins track (Creation, Cain, Flood, Babel, Abraham, Jacob, Joseph) using the 2022 Q2 notes.
- Sources: Remedy `02--genesis--003.md`, `02--genesis--002.md`; `...\The Remedy\01_Questionaire.docx`; Remedy `26--1-john--004.md` (4:18 "Fear is part of the infection of selfishness"); later: `2022 Q2\2022_Q2_L02_notes.pdf` etc.
- Readiness: fully ready. Effort: **S**.

**7. Fear vs Love: Interactive Brain Map**
- Pitch: Jennings' psychiatry: the fire-alarm circuit (amygdala = alarm, hypothalamus = 911 operator, pituitary = radio tower, adrenal glucocorticoids = responders, hippocampus = fire chief, DLPFC = principal) vs the prefrontal/ACC love and reason circuits, with a God-concept toggle.
- Interaction: SVG brain with hotspots; scenario slider (rubber hose vs snake); master toggle "God-concept: punishing / loving" re-colours regions and lists downstream effects (cytokines IL-1/IL-6/TNF -> insulin resistance, CVD, bone loss vs ACC growth, lower BP, memory +30%); proBDNF -> BDNF mini-sim (fire a circuit and it thickens; idle and it prunes); Newberg 12-minute protocol as a 30-day simulator; media self-check (TV, music, porn). Companion tab: the 17 Steps / brain-health habit tracker merged from blog and Addendum, with a 15-minute meditation timer.
- Sources: `GodShapedBrain.md` 99-115 (diagram labels), 246-312 (ch.2), 339-466 (ch.3-4), 863-868 (Records and the Brain), 1332-1388 (Addendum), 2212-2240 (glossary); `posts\2014-03-16--fear-the-medium-of-death...md`; `2018-05-10--the-power-of-truth-to-change-the-brain.md`; `2010-05-31--how-tv-and-an-angry-wrathful-god-damage-your-brain.md`; `2018-06-13--7-steps...md`; `2012-04-02--10-simple-steps...md`. Later: Healing The Mind seminar transcripts.
- Readiness: text ready; SVG artwork is the cost. Effort: **M-L**.

**8. Six Kinds of Power: what breaks each one**
- Pitch: coercive, inducing, deceiving, love, love+truth, restraining: definitions, which moral level each appeals to, and the verbatim "broken by..." lists; why God can only use truth and love in freedom.
- Interaction: six columns with reveal cards; scenario mini-games (the Godfather offer, the cult member, the spouse-affair lie breaking love, de Chergé's testament as unbreakable); restraining-power panel (least restraint, shortest time; parent, quarantine, psychiatric hold, God holding the four winds Rev 7:1-3); closing: sovereignty redefined, Zech 4:6. Cross-link (not merge) to blog's **Six Powers of Satan** (lies, imposed law, mammon, accusation, temptation/division, death) as a drawer.
- Sources: `GodShapedHeart.md` 1367-1500, ~1850-1860; `GodShapedBrain.md` ~480-510; `posts\2021-02-18` through `2021-03-25--the-six-powers-of-satan...parts 1-6`.
- Readiness: verbatim lists. Effort: **S**.

### Pillar C. The Remedy: salvation as healing

**9. Sin Is a Disease: symptom or condition? (plus the Atonement Prism)** — BUILD NEXT (#5)
- Pitch: the healing model of salvation in one playable page, built from the Savannah dialogue and the atonement metaphors.
- Interaction: Scene 1 cystic-fibrosis sort (cough/fever vs CF; lust/anger/adultery vs fearful-selfish heart). Scene 2 quick polls ("push your healthy brother in front of the doctor?", "erase the medical records?", "fear the doctor or the disease?"). Scene 3 Trust x Remedy matrix (bin Laden with a cure / loving father-doctor with no cure / both) explaining why Jesus had to both reveal truth and restore the law of love in humanity. Scene 4 cautionary cards: Jesse (insight is not change), Greg (sincerity is not truth). Scene 5 brand-name vs generic penicillin, Aslan and Emeth. Tab 2 **Atonement Prism**: click a colour band (ransom, adoption, reconciliation, sacrifice, substitution, debt, advocate, remission, moral influence) to see its verses, the reality it points to, and the distortion when taken as the reality; "what problem did sin create?" decision tree (did God change? did the law change? did humans change?); myth-buster for the standard allegations against the healing model; Tract 003's "infinite sacrifice" (incarnation permanent) card set.
- Sources: `GodShapedBrain.md` 736-764 (ch.10), 704-733 (ch.9), 918-970 (ch.13 Why Jesus Had to Die); `GodShapedHeart.md` ~470-500, 1140-1180; `posts\2011-04-23--metaphors-of-the-atonement.md`; `2010-06-04--the-healing-substitution-model.md`; `2008-11-21--christ-our-substitute.md`; `2009-04-24--why-did-jesus-have-to-die.md`; `2010-04-16--my-blood-father...md`; `2021-07-29--six-steps-to-dialogue...md`; `C:\Personal\Religion\Tract_003_InfiniteSacrifice.pdf`; `SalvationAndYou_Magazine_LTR_English_web.pdf` (hardware/software/energy analogy; imputed vs imparted).
- Readiness: dialogue adapts nearly verbatim; prism needs ~15 posts distilled. Effort: **M**.

**10. The Law as Diagnostic Instrument (Romans 3 and 7, Galatians 3)**
- Pitch: Romans 7 is where most Christians carry a courtroom; the Remedy reads it as an MRI ("only a diagnostic instrument--and not a Remedy"; "I had unwittingly attempted to use [it] as a cure").
- Interaction: verse reader with `lens-toggle` on every verse; clinic panel (Diagnose -> Prescribe -> Treat -> Heal) lights up as you scroll 7:7-25; card sort "what the law can do" vs "what only the Remedy can do"; kinsman-redeemer quiz from the Q1 Hebrews notes (does Jesus pay Satan, pay God, or heal humanity?).
- Sources: Remedy `09--romans--003.md`, `09--romans--007.md`, `12--galatians--003.md`, `03--psalms--001.md`, `03--psalms--019.md`, `22--hebrews--008.md` (8:10 "restore my law of love in their minds"); Matthew 5 after re-parse; `2022 Q1\2022_Q1_L04_notes.pdf`.
- Readiness: buildable today from epistles. Effort: **S-M**.

**11. The Little Theater: sanctuary walkthrough**
- Pitch: walk camp -> court -> Holy Place -> Most Holy; every furnishing decoded three ways: symbol, the mind (Most Holy Place as model of the healed heart), and the Remedy's "script and stage play" reality.
- Interaction: top-down SVG plan with hotspots (brazen altar wood+bronze+horns+fat+fire, laver mirrors, lampstand 6+1, table 12 loaves, golden altar, curtain, ark: manna -> law -> budding rod, lid, Shekinah); "play the offering" animates the non-priest and priest sin-offering liturgies; penal/healing toggle per symbol; sidebar "saved without acting" (Naaman, Jethro, Esther, thief). Hebrews layer: tap an element to flip from script to reality with the Remedy verse (veil -> "ripped open the veil of lies told by Satan", Heb 10:20).
- Sources: `GodShapedHeart.md` 1239-1365 (ch.10), 1096-1115; `posts\2021-12-16--the-most-holy-place-a-metaphor-for-our-minds.md`; `2026-07-16--the-ark-of-the-covenant...md`; `2013-10-20--what-does-the-veil-represent...md`; Remedy `22--hebrews--009.md`, `--010.md`, `--012.md`, `03--psalms--051.md`.
- Readiness: text complete; plan drawing is the cost. Effort: **M-L**.

**12. Heavenly Records: rap sheet or medical chart?**
- Pitch: the same verses about books, judgment and blotting out, read as prosecution evidence vs the physician's chart that defends God (Rom 3:4).
- Interaction: split screen courtroom / hospital; drag each verse (Rev 20:12, Isa 43:25, Heb 8:10-12, 1 Cor 13:5, 2 Cor 5:19, Rom 3:4 in three versions, Mal 3:2-3, Hos 4:17, Rev 22:11) onto a side and see which reading harmonises all; the Jehovah's Witness helicopter-crash ER case; "where is sin blotted out, books or hearts?"; 1844 / cloud-server backup / body-soul-spirit drawers from the sanctuary booklet.
- Sources: `GodShapedBrain.md` 813-868 (ch.12); `GodShapedHeart.md` ~1619-1632, 1840-1905; `C:\Personal\Religion\HeavenlySanctuary_web.pdf`; `Wedding_of_Christ_Magazine_Web.pdf`.
- Readiness: ready. Effort: **S-M**.

### Pillar D. God's character: wrath, fire, judgment, the hard passages

**13. The Consuming Fire: who can dwell with everlasting burning?** — BUILD NEXT (#1, the user's requested topic)
- Full architecture in section 4.
- Effort: **M** (1-2 days; verse list and Jennings' readings are explicit).

**14. Wrath = Letting Go**
- Pitch: the mechanism underneath Fire, plagues and the cross: God's wrath is withdrawal of restraint (Rom 1:24, 26, 28 "gave them over"), Satan's wrath is the active use of power to harm; "exact opposites".
- Interaction: Romans 1 with the three paradidomi clauses as hotspots (Remedy + cause + effect); flip cards "what God SAID / what actually HAPPENED" (Deut 32:22 vs 32:30; Deut 31:17; Ps 78:58-61; Ezek 21:31; Ezek 24 vs Babylon; Hos 4:6); four-winds animation (Rev 7:1-3) with a seven-step "bowls" slider captioned by Remedy Rev 15:7 "heartbreaking disengagement" and 16:8-9; Remedy verse wall of the ~55 genuine let-go verses (after pruning the regex hits); "acting or withdrawing?" quiz; Egypt plagues vs seven last plagues contrast. Shares one data file with Fire.
- Sources: `posts\2011-10-21--god-s-wrath-what-does-it-mean.md`; `2024-01-25--god-s-wrath-versus-satan-s-wrath...md`; `2010-07-20--seven-last-plagues-why.md`; `2024-08-15--the-plagues-of-egypt-and-the-seven-last-plagues...md`; `2024-02-15--death-a-punishment-inflicted-by-god-or-a-natural-consequence-of-sin.md`; `2009-11-27--why-does-the-bible-use-the-word-punish.md`; `GodShapedBrain.md` ~889-902; Remedy `09--romans--001.md`, `09--romans--012.md`, `30--revelation--015.md`, `--016.md`, `--014.md`, `22--hebrews--010.md`, `03--psalms--022.md`, `05--mark--015.md` (15:34 after re-parse).
- Readiness: arguments explicit; 30-minute prune of verse hits. Effort: **M**.

**15. The Four Judgments Timeline**
- Pitch: Eden to the Great White Throne as four non-judicial events: (1) our judgment of God (Carmel: is He trustworthy?), (2) God's therapeutic diagnosis of each heart (the High Priest enters the heart, Heb 8:10; refiner's fire Mal 3), (3) the righteous review the record in the millennium (Rev 20:4; 1 Cor 6:3), (4) the Great White Throne = revelation of each character's actual condition.
- Interaction: `timeline` with four stations; courtroom-vs-clinic flip per station; station 1 includes a "your judgment of God" reflection; station 3 "open the books" (medical record vs legal tally); Daniel 7 overlay (royal court, not judicial); first angel's "the hour of his judgment has come" tie-in.
- Sources: `posts\2021-07-22--the-four-judgments.md`; `2022-03-31--safe-to-save...md`; `2009-01-02--the-court-in-daniel-7-royal-or-judicial.md`; `2023-08-10--imperial-versus-design-law-judgment...daniel-7.md`; `C:\Personal\Religion\3Angels_Magazine_web.pdf` first-angel section; Remedy `30--revelation--020.md` ("diagnosed according to the reality of their condition").
- Readiness: ready. Effort: **S-M**.

**16. Hard Passages hub: did God kill? (narratives) and Remedy vs traditional (renderings)**
- Pitch: the stories and verses where learners stall, each solved with the design-law reading and a named interpretive move.
- Interaction: Tab 1 detective dossiers (Flood, Sodom, Uzzah, David's baby, she-bears, Korah, Canaanite wars, Abraham and Isaac, Psalm 137, Pharaoh's heart, Nadab and Abihu, OT death penalty, Genesis 3 curse): the charge, the text, imposed-law verdict, design-law verdict, the clue, reader confidence slider. Tab 2 ~40 verse pairs Remedy-beside-traditional with "move" tags (penal -> consequence; appeasement -> revelation of character; judge -> diagnose; torment -> non-existence) that filter the list; export selected pairs as a study sheet. Includes the **first-death vs second-death** distinction and a short "Death, sleep and resurrection" module (first death as grace; why the wicked are resurrected; who destroys the soul) which the Fire page links to.
- Sources: one blog post per case (`2011-02-04--she-bears...`, `2011-06-03--did-god-kill-david-s-baby`, `2019-12-11` + `2020-01-15` Flood parts 1-2, `2023-12-07--the-death-penalty-in-old-testament-times`, `2017-12-18--...abraham-to-kill-isaac`, `2024-03-07--...psalm-137`, `2009-06-05--...pharaoh-s-heart`, `2018-01-02--david-and-the-showbread-vs-uzzah`, `2025-01-09--the-first-death-a-manifestation-of-god-s-grace`, `2010-03-25--why-resurrect-the-wicked`, `2009-05-07--who-destroys-the-soul`, `2008-08-08--did-christ-die-the-second-death`); Remedy `02--genesis--006/019/022.md`, `09--romans--001/003/005/012.md`, `26--1-john--002/004.md`, `30--revelation--006/014/016/019/020/021.md`, `03--psalms--002/007/090.md`. Traditional column: needs a public-domain translation JSON (WEB or KJV), not on disk.
- Readiness: posts ready; 14 dossiers + 40 annotations to write. Effort: **L**.

### Pillar E. Growing up: the Seven Levels and the long story

**17. Same Act, Seven Reasons (Seven Levels companion)** — BUILD NEXT (#4)
- Pitch: extends the existing page with Jennings' four worked tables: why brush your teeth, why wife-beating is wrong, why Jesus had to die (Satisfaction / Ransom / Governmental / Penal Substitution / Moral Influence / Recapitulation-Christus Victor / at-one-ment), and which power persuades whom; plus Eric driving his stroke-victim wife through red lights and Sandi's conference as level-revealing dilemmas.
- Interaction: scenario tabs; `level-stepper` 1-7 rewrites the "why it is right or wrong" panel live; divider at 4|5 shows the imposed -> design shift; scripture correlate per level in the side rail; "can't skip levels / law of exertion" warning with the talents parable; "where would you land?" reflection. Tab 2: **Roads of the Journey** (eight walks: ignorance, illiteracy, infancy, the line, confusion, alone, rebellion, with God) as a self-locating map, labelled as the blog's own frame rather than a Jennings mapping to the seven levels.
- Sources: `GodShapedHeart.md` 363-400, 435-440, 880-905, 1376-1466, 1870-1900; `C:\Personal\Religion\SevenLevelsOfMoralDevelopment.pdf`; `posts\2019-05-29` + `2019-06-05--the-journey-of-life...parts 1-2`; `2008-05-30--fear-is-for-children.md`; `2024-07-11--servants-and-friends-of-god.md`.
- Readiness: all four tables verbatim. Effort: **S-M** (reuses the existing page's framework).

**18. Parables as Design Law: what kind of law is this?**
- Pitch: trains the lens on material readers already know: for 20+ parables, "is there a judge, jury or decree here?" then Jennings' answer.
- Interaction: `card-grid` per parable (lamp, speck and log, new wine, divided kingdom, sower, weeds, mustard seed, leaven, treasure, net, mouth, lost sheep, unforgiving servant "legally right but terminally selfish", labourers, two sons...); reveal and tally "design law spotted"; extras: the seed that dies, rich young ruler, Lazarus and the rich man.
- Sources: `posts\2020-08-25--parables-of-jesus-the-overarching-theme.md` (29 bullets with references); `2019-02-20--new-wine-in-old-skins.md`; `2022-10-20--dying-to-live-lesson-from-the-seed.md`; `2023-08-03--the-rich-young-ruler...md`; `2023-01-12--lazarus-and-the-rich-man.md`.
- Readiness: very ready. Effort: **S**.

**19. Two Covenants, Two Laws (with Sabbath by design)**
- Pitch: the eternal covenant of grace (design law, written on hearts, all humanity) vs the temporary Sinai arrangement (stone, regional), one covenant from Adam onward, not successive contracts.
- Interaction: animated two-column table; timeline Adam -> Noah -> Abraham -> Sinai -> Cross -> end of the 1000 years; "drop a practice here" sorter (circumcision, feast days, Sabbath, tithe, dietary laws, Ten Commandments) with Jennings' placement; a dedicated Sabbath tab (why Saturday, what makes it holy, Sabbath as brain rest from 2022 Q2 L01) since Sabbath otherwise has no home; Hebrews' Seven Better Things as the payoff.
- Sources: `posts\2025-09-18--two-covenants-upon-two-laws.md` (10-row table); `2019-01-01--sabbath-imposed-rule-or-design-for-life.md`; `2025-01-02--what-makes-the-sabbath-holy.md`; `2010-08-27--circumcision-feast-days...md`; `2015-12-07--...ot-feast-days.md`; `2025-06-26/07-03/07-10--seven-better-things...`; `2021 Q4\2021_Q4_L03_notes.pdf` (everlasting covenant); `2022 Q2\2022_Q2_L01_notes.pdf`.
- Readiness: very ready. Effort: **S-M**.

### Pillar F. Living it: the clinic pages

**20. Forgiveness and Guilt walkthrough**
- Pitch: what forgiveness is and is not, starting from the pregnant-14-year-old scenario ("what is she asking for?"), with the guilt decision tree as a branch.
- Interaction: `branch-flow`: I hurt someone / someone hurt me / I can't forgive myself / should I apologise? Each branch pulls Jennings' guidance (boundaries with abusers, when apologising is wrong, confessing to others, assurance). Guilt branch: "did I actually wrong someone?" -> legitimate (repent = heart change; restore) vs illegitimate (find the lie; apply truth; repenting reinforces the lie), the dying-sister case playable both ways, type your own guilt statement and tag the lie. Keith Johnson's Four Questions and "forgiveness is not restored trust" from God-Shaped Brain ch.14 as the justice bridge.
- Sources: `posts\2013-09-24--forgiveness-in-the-non-penal-view.md`; `2009-05-22`, `2009-03-13`, `2012-12-02`, `2011-02-11--guilt-how-to-resolve-it.md`, `2020-08-18--when-apologizing-is-wrong.md`, `2025-02-27`, `2012-05-15--abuse-christian-reconciliation-and-boundaries.md`, `2008-11-08--love-and-boundaries.md`; `C:\Personal\Religion\Tract_002_HowToResolveGuilt.pdf`; `GodShapedBrain.md` 1011-1142 + Study Guide ch.14 (~2008-2060); `GodShapedHeart.md` ~809-900.
- Readiness: ready. Effort: **M**.

**21. Justice: deliver the oppressed, not punish the oppressor**
- Pitch: biblical justice as rescue (Ps 82:3, Isa 1:16-17, Isa 30:18, Jer 21:12, Luke 4:18), Satan's two-step trap (false standard, then fight injustice with coercion), and the Four Questions.
- Interaction: verse wall highlighting what justice *does* (defend, rescue, help); the Four Questions one-at-a-time reveal tracking the reader's mercy/justice flip; drag cases (Cain, the Flood, Joseph's brothers, Israel's exile, the cross) onto the legal or design bench; two-step trap scenarios with the politically loaded ones (CRT, police killing) replaced by the biblical and Charleston/Amish examples; retributivism vs utilitarianism (law-student email); eye-for-eye as restraint (Iraqi shepherd boy).
- Sources: `GodShapedBrain.md` 1011-1142; `GodShapedHeart.md` ~809-900 ("suicide rope" justice); `C:\Personal\Religion\Tract_008_InjusticeOfHumanJustice.pdf`; `Tract_004_InsidiousnessOfSin.pdf` section 3; `Tract_006_Babylon.pdf`; `posts\2017-11-16--what-is-biblical-justice.md`; `2012-09-03--retribution-or-rehabilitation.md`; Cosmic Conflict guide Week 8; `2022 Q2\2022_Q2_L12_notes.pdf`.
- Readiness: ready. Effort: **M**.

**22. Clinic self-checks (one page, four tools)**
- Pitch: Jennings' psychiatric instruments as scored interactives: Love or Dependency (10 paired statements -> 8 steps, navy-diver air-line analogy); Mistake or Sin perfectionism sorter (bounced cheque by arithmetic vs fraud; alabaster-jar woman; the six fears loop you break by swapping the motive); Which Kind of Meditation (5-question Eastern-vs-biblical test, brain-wave table, 15-30 min guided session on Isa 55:7-9); Scriptural 12 Steps with verses (Mark 2:17, John 3:17, Matt 11:28-30, Ps 139:23-24, James 5:16, Ezek 36:25-27...) and the "imagined behaviour fires the same circuits" rewire meter. Knowing God's Will (David runs ahead / Jonah away / Martha around / Elijah is still) as a fifth mini-module.
- Sources: `C:\Personal\Religion\Codependency_Web.pdf`; `TrapofPerfectionism_Pamphlet_English_Web.pdf`; `Meditation_Guide_8x11_web.pdf`; `Tract_005_OvercomingAddiction.pdf`; `Tract_009_KnowingGodsWill.pdf`; `Tract_010_Loneliness.pdf`; `posts\2020-04-29--a-scriptural-healing-plan-for-overcoming-addiction.md`; `2024-04-18--codependency...md`; `CIBTS_English+Cover.pdf` ch.8 Love's Counterfeits.
- Readiness: all verbatim. Effort: **M** (four small builds). Later additions: Seven Steps Through Grief stepper; the Abuse Cycle and first-responder guide (with hotline notice).

### Pillar G. Cosmic conflict and prophecy

**23. The Cosmic Conflict in 13 Weeks**
- Pitch: the one narrative spine from Lucifer's lie to Revelation, from the Come and Reason study guide, with a "Satan's charge vs Jesus' evidence" board that fills in week by week.
- Interaction: week selector with Living Words, Bottom Line, the clinical vignette as a case file, daily readings as collapsibles, the two-column evidence board; Revelation weeks link to the symbol decoder.
- Sources: `C:\Personal\Religion\TruthLoveFreedom_StudyGuide_CosmicConflict.pdf` (57k words; parse by headers); `C:\Personal\Religion\Job_Magazine_English_Print.pdf` (seven truths as flip cards for weeks 4-5).
- Readiness: semi-automatic parse. Effort: **M-L**.

**24. Revelation Decoded: symbols, Babylon, the three angels**
- Pitch: the Remedy's inline glossary ("Babylon the Great--a symbolic description of religions that misrepresent God"; mark of the beast in heart/deed; sickle = bring his followers home; 1000 years = chain of circumstances; sword = spoken truth) plus the Rev 13/17 magazine's symbol rules and the 7 Lamb powers vs 10 beastly powers, plus the Babylon self-check (method, not denomination: does the system enforce conscience, accuse, threaten, equate loyalty to institution with loyalty to God?).
- Interaction: symbol index linking to defining verses; three-angels concentric rings aligned with design-law terms (law of worship / Babylon / law of liberty); Lamb-vs-dragon powers duel; 12-item Babylon checklist scored toward "methods of Babylon" vs "methods of God's kingdom"; Rev 20 millennium timeline shared with the Fire page. Prophecy table ("every row collapses to Messiah is coming to save") and the Eight Signs as a drawer.
- Sources: Remedy `30--revelation--013/014/016/017/019/020/021.md`; `C:\Personal\Religion\Revelation13_Magazine_Print.pdf` pp. 6-20 (pp. 20-60 still unread); `3Angels_Magazine_web.pdf`; `posts\2023-10-12--babylon-popery-and-your-church...md`; `2021-02-11--babylon-the-mother-of-harlots...md`; `2025-07-24--the-seal-of-god.md`; `2020-07-07--bible-prophecy-the-overarching-theme.md`; `2020-12-24--eight-signs...md`.
- Readiness: Revelation 98% in markdown; ~60 symbols to curate. Effort: **M**.

### Infrastructure (not learner pages, but everything above deep-links into them)

**25. Remedy Verse Explorer (data layer + reader)**: `remedy-reader` component with lens highlighting, red-letter toggle, concordance tab (trust 659 vs faith 75; remedy 964 vs salvation 20; design 376 vs imposed 7), themed reading plans with localStorage progress, phase-1 chapter-level audio player mapped to the 262 MP3s (filename quirks: `PHILEMON.mp3`, `PHILLIPIANS_04.mp3`, `REVELATION_00.mp3` intro). Blocked only on re-running `reparse.py` into the corpus folder. Effort: **M**.

**26. Corpus browsers**: blog search-first browser (612 posts, keyword heat strip) and class-notes browser (quarter > lesson > day) from `blog_index.json` and `class_notes.json`; later, the chapter-by-chapter study companion for the two books with CIBTS MP3 per chapter (chapter 12 audio missing). Effort: **M** each, no editorial work.

### Build order summary

| Order | Page | Why now |
|---|---|---|
| 0 | Seven Levels page recovery + `seven_levels.json` + kit skeleton (lens-toggle, verse-card, timeline, level-stepper, glossary-pop) | prerequisite for everything |
| 1 | **The Consuming Fire** | user's stated next topic; fully specified below |
| 2 | **Two Lenses Keyword Switcher** | every other page links to it; half a day |
| 3 | **Falling Dominoes and Healing Cascade** | the causal model; cheap |
| 4 | **Same Act, Seven Reasons** | extends the page that already exists |
| 5 | **Sin Is a Disease + Atonement Prism** | the positive healing-model pillar |
| 6-8 | Preface timeline, Venn, Genesis 3 | each half a day, fully ready; together they make a usable hub |
| 9-12 | Wrath, Four Judgments, Design Laws Lab, Six Kinds of Power | complete the character-of-God and design-law pillars |
| then | Remedy Verse Explorer (after re-parse), Law as Diagnostic, Records, Sanctuary, Parables, Two Covenants, Forgiveness, Justice, Clinic, Revelation, Cosmic Conflict, Hard Passages, Brain Map, browsers | |

Pages dropped or deferred after judging: Fundamental Focus 28-traits browser (image-only, not Come and Reason); How Good People Do Evil ladder (COVID framing; keep only the semantic-drift word game inside Two Lenses); Object Lessons gallery (becomes a feed in the blog browser); Deuteronomy Covenant Explorer (85k words to distil; its one-covenant diagram goes into Two Covenants); Biblical Concepts Made Easy port (becomes the kids' track once adult pages exist, reusing their components); Healing The Mind brain map (after transcription, merges into page 7).

Topics no candidate covered that should be scheduled after the above: **the cross itself as a narrative walkthrough** (Gethsemane, Mark 15:34 / Psalm 22 in the Remedy, "What Angels Saw at the Cross", Did Christ Die the Second Death); **faith = trust** (how trust is established by evidence; Righteousness/Justification/Sanctification by Faith posts); **prayer under design law** (what prayer changes if God does not change); **Holy Spirit and the humanity of Christ**; **marriage, sexuality and parenting by design** (Parents Represent God, Top 10 marriage posts, human-sexuality MP4, LoveCourse); **how to talk about this with your church** (Tract 007 How to Disagree + Six Steps to Dialogue); **why God allows suffering / 2022 Q3 In the Crucible** (unmined folder).

---

## 4. The Fire page: content architecture ready to build

Working title: **The Consuming Fire: who can dwell with everlasting burning?**  File: `dist\fire.html`. Data: `data\pages\fire.json` (verses[], remedy[], quotes[], objections[], glossary[], timelineSteps[], gallery[]).

### 4.1 Thesis the page teaches (Jennings' own framing, assembled from Eternal Fire 2010, Question of Punishment I-III 2008, Truth About Hell 2021, God-Shaped Brain ch.16, The Remedy, 3 Angels magazine pp. 36-41)

1. **The fire is God Himself.** "Our God is a consuming fire" (Deut 4:24; Heb 12:29; Remedy: "a consuming fire of love, holiness, purity, righteousness, goodness, and truth"). Isaiah 33:14-15 is the hinge: the one who dwells with everlasting burning is the righteous. Jennings calls the opposite assumption "the lie Satan has foisted upon us".
2. **Sin is made of lies and selfishness, so the fire that consumes sin is truth and love.** "What is a book made of? What is sin made of?" Combustion burns molecules and cannot destroy an idea. Hence "baptize you with the Holy Spirit and with fire" (Remedy Matt 3:11: "the cleansing fire of God's love and truth").
3. **The wicked suffer and die from their own condition, not an inflicted penalty.** "They perish because they refused to love the truth" (2 Thess 2:10). Torment is "of mind, anguish of heart" in the presence of the Lamb (Rev 14:10). Nadab and Abihu "consumed" yet carried out "still in their tunics" (Lev 10:1-5). Only after all are dead do "the fires of combustion commence" (2 Pet 3:10-13). "Smoke" = what is left: the universe's permanent memory, not ongoing torment.
4. **Brimstone = divine fire** (Jennings reads *theion* as a form of *theios*, "divine"); present as his reading with a caveat.
5. **Wrath = God letting go** (Rom 1:24, 26, 28; Deut 32:22 explained by 32:30; the cross: "forsaken", not "killed"). God's wrath is cessation of protective power; Satan's wrath is power used to harm; "exact opposites".
6. **Two deaths.** First death = sleep, an "artificial state of grace" God controls and has used therapeutically (Flood, Sodom, Uzzah, Elijah's captains). Second death = the wages of sin, annihilation, the devil's power (Heb 2:14), never inflicted by God. Christ did not die the second death.
7. **Judgment = diagnosis.** The books of Rev 20:12 are "like medical records". The wicked are resurrected so that with the gates open (Rev 21:25) "their exclusion is voluntary with themselves" (GC 543).
8. **Why it matters neurologically.** Angry-god concepts activate the amygdala and impair the prefrontal cortex/ACC; Newberg's 12-min/day meditation on a God of love grew the ACC; "love does not flow where lies about God are retained."

### 4.2 Sections and interactions

| # | Section | Content | Interaction (kit component) |
|---|---|---|---|
| 0 | Opening: "Who of us can dwell with everlasting burning?" | Isa 33:14 alone in the ominous register, then v.15 revealed; Jennings' "I did a double take, then a triple take" (GSB ch.16); the three colour-coded voices (Scripture / Remedy / Jennings, plus muted EGW). | Tap-to-reveal: flame turns from red to gold when v.15 appears. One-question poll "who did you think lives in the fire?" stored locally and echoed at the end. |
| 1 | Same fire, two experiences | One fire; the only variable is the heart. Moses' radiant face vs Israel's veil (Ex 34); Remedy Heb 12:19-20 (voice "so pure that those... still preferring selfishness... begged not to hear"; God "put up a barrier... to protect them"); Remedy 2 Thess 1:7-9; Remedy 1 Cor 3:13-15 (same fire burns misconceptions out of the saved); DA 108; GC 543. | Slider "state of the heart" healed -> unhealed; the flame never changes, the figure does (radiant -> shielding face -> fleeing to the rocks, Rev 6:15-16); counter "Fire: 0 changes. Heart: 1 change." |
| 2 | What is sin made of? The combustion test | Book / table / sin; lies (John 8:44) + selfishness; truth consumes a lie, love consumes selfishness; Spirit of truth and love = fire (Remedy Matt 3:11-12; Luke 3:16-17; Acts 2:3 "two separate streams of fire -- the fires of truth and love"); altar fire = Holy Spirit (GSH ~1273); Luke 24:32; Isa 6. | `sort-bins` lab with two burners (combustion / truth+love) and tokens: book, chair, body, a lie about God, selfishness, guilt, a Christlike character. Results table fills in; final prompt: which fire cleanses the earth of *sin*? |
| 3 | The fire gallery | Canonical timeline: Eden's fiery radiance (Remedy Gen 3:24); burning bush (Ex 3 / Remedy Acts 7:30); Sinai (Ex 24:17); Nadab & Abihu (Lev 10); Solomon's temple (2 Chr 5:14; 7:1-3); Elijah's chariot and Carmel/the captains (flagged first-death acts); Isaiah's coal (Isa 6:6-7); fiery stones and "fire from within you" (Ezek 28:14-18); river of fire with billions standing in it (Dan 7:9-10); refiner and rising Sun (Mal 3:2-3; 4:1-3); Transfiguration (Matt 17:2); Pentecost (Acts 2:3); sea of glass mingled with fire (Remedy Rev 15:2 "crystal plane reflecting the fiery presence"); city lit by God (Rev 21:23; 22:5); captions Isa 33:14-15, Song 8:6-7. | `timeline` of cards; each asks "What burned?" and "Who was harmed?" before revealing Jennings' comment; filter chip "only events where someone was hurt" isolates the hard cases and links to section 10. |
| 4 | Case file: Nadab and Abihu | "Fire came out from the presence of the LORD and consumed them... carried them, still in their tunics." Jennings: the fire consumed sin/the inner condition, not matter; "this is what happens to the wicked in the end". Honest footnote: GSB ~487 also lists them among times God "used his power to put people to rest in the grave". | Document viewer with highlighter: swipe "consumed" (red) then "still in their tunics" (gold); prompt "what kind of fire leaves the tunics intact?" (combustion / electrocution / a fire that consumes what sin is made of); toggle "first death or second death?" opens the caveat. |
| 5 | Verse explorer: every fire text, two readings | ~45 passages (list in 4.3), each with translation text, Remedy rendering or "missing locally" badge, imposed-law reading, design-law reading, source post. | `lens-toggle` re-renders all cards at once (table shifts red -> gold); filters: book, Remedy available, Jennings wrote a post, hard case; "random verse" self-quiz where the reader guesses the design-law reading before reveal. |
| 6 | Wrath explorer: "gave them over" | Rom 1:18-32 with the three paradidomi clauses; Hard Sayings of the Bible p.543 quote; Satan's wrath vs God's wrath; "what He said vs what happened" pairs (Deut 32:22-23 vs 29-30; Deut 31:17; Ps 78:58-61; Ezek 21:31; Ezek 24 vs the Babylonians; Hos 4:6); the cross; plagues as stepwise release (Rev 7:1-3; Remedy 15:7; 16:8-9); SDA Bible Commentary vol. 6 pp. 477-478 definition quoted in the Prewitt response. | (a) hotspots on the three "gave them over" phrases; (b) flip cards said/happened; (c) animated hand that strikes (Satan) vs releases a rope holding back a flood (God), with a seven-step bowls slider. |
| 7 | Why does the Bible shout? | "The condition of the people is the determining factor in the way God communicates"; Hos 4:16 "stubborn as mules"; parent shouting at the child near the cliff; Korah's survivors grumbling next day (Num 16:41); Micaiah's lying spirit for Ahab; declarative vs evidentiary passages, Jesus as the lens (John 3:17; 5:22; 8:15; 12:47-48); Ezekiel 24 pot scene. | "Tune the message to the listener" dial: one truth ("leaving Me will destroy you") at three settings (friend Ex 33:11 / wavering Hosea / hardened Ezek 24, Deut 32); two-pane reader where the Jesus-lens is dragged over the declarative verse. |
| 8 | Brimstone, smoke and "for ever" | *thion/theios*; "in the presence of the holy angels and of the Lamb"; smoke = memory (Remedy 14:11 "never be forgotten"); Remedy 20:10 "day and night for the conclusion of their existence"; Isa 34:9-11 Edom parallel (Cole study guide); Remedy 21:8 includes "those who worship gods that must punish or be appeased"; Remedy 19:20, 20:14-15 definitions of the lake. | `glossary-pop` on brimstone / tormented / smoke / for ever and ever / in the presence of the Lamb inside the live verse text, each with Greek, Jennings' gloss, Remedy rendering and caveat badge; "where?" button highlights every locative phrase in Rev 14, 19, 20, 21. |
| 9 | End-time timeline: where exactly is the lake of fire? | (1) Second coming: righteous transformed, wicked die of their condition at the brightness (2 Thess 1:7-9; 2:8). (2) 1000 years: earth an abyss, Satan "bound by circumstances", saints review (third judgment). (3) Wicked resurrected; New Jerusalem descends; gates open; exclusion voluntary. (4) They march; "God unveils his full glory... rivers of fire" (Remedy 20:9); books = diagnosis; second death. (5) Bodies remain; then combustion: "the elements melt" (2 Pet 3:10-12), "a boiling cauldron, a great lake of fire" (GSB). (6) New earth, God its light. | Scrubbable `timeline` with toggleable layers: what is burning (presence-fire vs combustion), who is alive, where is Satan, which of the four judgments; persistent question "is this the lake of fire yet?"; note that the same presence-fire is applied to both unveilings (step 1 and step 4). |
| 10 | Two deaths: sleep and the wages of sin | First death = sleep (John 11:11-14; 1 Thess 4:13-17), God controls it (Deut 32:39; 1 Sam 2:6), used therapeutically (Flood, Sodom: Remedy Gen 19:24 "fiery burning streams of magma... cauterized this lesion", "vaporization... painless"; Elijah's captains; Uzzah); Jennings rejects both "punishment for sin" and "Satan did it". Second death = annihilation of body and psyche, "the devil's power" (Heb 2:14); "God doesn't kill (second death) anyone." Christ-vs-wicked five-row contrast (trusting vs distrusting; longing to see vs hiding; Father hidden vs revealed; under 72 h vs eternal; love overcame selfishness vs overcome by it). | `sort-bins`: drag Bible deaths (Flood, Sodom, Nadab & Abihu, Uzzah, Elijah's captains, Korah, Lazarus of Bethany, the thief, Jesus, the wicked at Rev 20) into first death / second death with "who caused it?" sub-answer; then the contrast as a flip table. |
| 11 | The angel in charge of the fire (Rev 14:18) and the three angels | The 2023 quarterly clipped v.18; the angel comes "from the altar" (Isa 6:6-7 "your guilt is gone"); he calls the harvest because "there is no one left for me to heal"; Remedy 14:18 "with the authority of the fire of truth"; 14:19-20 winepress = "pressed down under the destructive force of unremedied sin when God no longer shielded them"; three angels as law of worship / Babylon's wine ("God coerces and must inflict punishment if not properly appeased", Remedy 14:8) / law of liberty ("poured out full strength... God lets them go completely"). | "Clipped verse" widget: drag the right edge to extend v.18 to its full text and v.19, a second drag pulls in Isa 6:6-7; three concentric rings rotate to align each angel with its design-law term and Remedy verse. |
| 12 | Two fires in Revelation: the Lamb's and the dragon's | Fire from God's presence (1:14; 4:5; 14:10; 15:2; 19:12; 20:9) vs fire from the dragon/beast/human agents (9:17-18; 13:13 the lamb-like beast calls fire from heaven; 17:16 the ten horns burn the prostitute); Remedy 18:8; the rider's weapons are truth (sword from the mouth) and love (Remedy 19:15). From Cole study guide Week 12 Day 5 + Jennings' Sword of God. | Colour-coded concordance of every "fire" in Revelation; tap to assign a source (Lamb / dragon / human agents / symbolic) and compare with the guide's assignment; dim one source to see what remains. |
| 13 | What an angry-God picture does to your brain | Amygdala alarm vs PFC/ACC; fear shunts blood, impairs growth ("fear is the medium of death"); theatrical entertainment and wrathful-god concepts both overdevelop limbic circuits; Newberg 2009 p.49: 12 min/day x 30 days on a God of love grew the ACC, lowered BP/HR/stress hormones, memory +30%, while "an angry, wrathful, distant, or punishing god did not"; Rom 1:21 "futile... darkened"; GSB endnote Shariff & Rhemtulla 2012; Jennings' abused patients as a window into the torment of truth. | Pick a God-concept card; simplified brain lights ACC-PFC glow vs amygdala flare with a running effects list; "12 minutes" timer starts a guided reflection on Remedy Heb 12:29; citations drawer. |
| 14 | Judgment through the law lens (bridge to Seven Levels) | GSH ~1855: "It really depends on which law lens (stage of moral development) you are looking through." Levels 1-4 hear a courtroom and "My blood, my blood, Father!"; levels 5-7 hear "the accurate diagnosis of the condition of each person's heart" (Hos 4:17). GSH ~1742 level-four definition; QoP I's three misunderstandings (law, sin, cross) and the leukemia/bone-marrow parable; "just get him some anger management classes". | `level-stepper` from the Seven Levels page re-voices Rev 14:10, Rev 20:12, Heb 12:29 at each level and shows the question that level asks ("Will I be punished?" -> "Is it fair?" -> "What does this reveal about God?"); deep link to seven-levels.html and the four-judgments cards. |
| 15 | Objections desk | The 15 objections in 4.4. | Accordion: objection text, "How would you answer?" journal box, then "Show Jennings' reply"; per-item "strength of local evidence" meter (strong / moderate / thin). |
| 16 | Closing: "We can never avoid the truth, only delay the day we deal with it" | Deal with it "here and now, under God's grace" vs "in front of the entire universe"; Isa 33:15's portrait; 1 John 2:28; 3:2; 2 Cor 3:18; Rom 12:20; St Simeon's prayer from the study guide ("burn Thou the thorns of all my transgressions"); GSB "What a day that will be when the fire of God's presence burns free!" | Private five-prompt self-check (GSB study questions: "what do these texts teach about the source of consuming fire?"; "love me or I will burn you -- what is the problem with this position?"); replay the opening poll answer beside Isa 33:15; buttons "Return to the slider" / "Open the Seven Levels page". |
| A | Sources and data | Every quote carries a `source-chip`; "copy verse table as CSV"; "missing Remedy verses" list so the page refreshes after the re-parse. | "show sources" switch. |

### 4.3 Key texts (with Remedy file paths where the Remedy covers them)

Remedy root: `C:\Personal\Religion\Blogs\remedy_bible_corpus\chapters\`

| Reference | Use on the page | Remedy file / status |
|---|---|---|
| Isaiah 33:14-15 (+ v.11 "set on fire by your very own breath") | the hinge; opening and closing | OT not in Remedy; quote from Truth About Hell / 3Angels pp. 36-37 / QoP III |
| Deut 4:24; Heb 12:18-29 | thesis; same fire two experiences; "remove the lies that have misrepresented him" (12:27) | `22--hebrews--012.md` |
| Ex 3:2-4 / Acts 7:30-36 | burning bush | `08--acts--007.md` |
| Ex 24:17; 34:29-35 | Sinai; Moses' face vs the veil | OT; quote from blog/GSB |
| Lev 10:1-5 | Nadab and Abihu case file | OT; quote from Eternal_Fire / GSB ch.16; caveat GSB ~487 |
| 2 Chr 5:14; 7:1-3; Ezek 28:14,16,18; Dan 7:9-10; Matt 17:2; 2 Kgs 2:11; Rev 15:2; 21:23; 22:5; Song 8:6-7 | fire gallery | Rev: `30--revelation--015.md`, `--021.md`, `--022.md`; Matt 17 after re-parse; rest OT |
| Matt 3:10-12; Luke 3:9,16-17; Acts 2:3 | baptism with fire; the positive fire | `04--matthew--003.md`; `06--luke--003.md`; `08--acts--002.md` |
| Matt 25:41,46 | "eternal fire prepared to consume evil... pass away for all eternity" | `04--matthew--025.md` line 50 (unnumbered text, verse_count 0) |
| Matt 10:28; 13:40-50; 18:8-9; Mark 9:43-48; Luke 12:49; 16:19-31 | hell texts | **missing in markdown** (red-letter); available after re-parse from `_cache` |
| John 3:19, 36 | why the fire hurts; "God, sadly, grants them their free choice" | `07--john--003.md` (3:36 present; 3:19 after re-parse) |
| Rom 1:18-32 | wrath = gave them over | `09--romans--001.md` |
| Rom 2:5-9; 12:19-21; Eph 5:6; Col 3:6; Heb 10:26-31; 1 Thess 5:9 | secondary wrath texts; "I will decide when to let them go"; "God did not make us to let us go" | `09--romans--002.md`, `--012.md`; `13--ephesians--005.md`; `15--colossians--003.md`; `22--hebrews--010.md`; `16--1-thessalonians--005.md` |
| Deut 31:17; 32:22-23,29-30,39; Ps 78:58-61; Ezek 21:31; 24:9-14; Hos 4:6,16; 1 Sam 2:6 | said vs happened; first death God controls | OT; Ps 78 in `03--psalms--078.md`; rest from God's Wrath (2011), QoP II, GSB |
| 1 Cor 3:12-15 | same fire burns error out of the saved | `10--1-corinthians--003.md` |
| 2 Thess 1:5-10; 2:8-12 | second-coming destruction; "they perish because they refused to love the truth" | `17--2-thessalonians--001.md`, `--002.md` |
| 2 Pet 3:7-13 | combustion phase after the wicked are dead | `25--2-peter--003.md` |
| James 1:15; 3:6; Gal 6:8; Rom 6:23; Ps 34:21 | death comes from sin | `23--james--001.md`, `--003.md`; `03--psalms--034.md` |
| Jude 6-7, 23; Gen 19:24-25 | Sodom "exposed to eternal fire"; "magma... cauterized" | `29--jude--001.md`; `02--genesis--019.md` |
| Gen 3:22-24 | first veiling of glory as grace | `02--genesis--003.md` |
| Ps 11:6; 18:7-8,13; 21:9; 50:3; 97:3; 89:46 | Remedy OT fire bonus ("it will be to them like burning coals of torment"; "fires of truth and love flow from him like mighty rivers") | `03--psalms--011.md`, `--018.md`, `--021.md`, `--050.md`, `--097.md`, `--089.md` |
| Rev 6:12-17 | "Hide us from the truth!... the day when he lets us go has come" | `30--revelation--006.md` |
| Rev 14:6-20 | three angels; brimstone; smoke; altar angel; winepress | `30--revelation--014.md` |
| Rev 15:1-8; 16:1-21 | plagues as stepwise disengagement | `30--revelation--015.md`, `--016.md` |
| Rev 17:16; 18:8 | two fires; Babylon's end | `30--revelation--017.md`, `--018.md` |
| Rev 19:11-21 | sword of truth; lake "emanating from the unveiled presence of God" | `30--revelation--019.md` |
| Rev 20:1-15 | millennium; "rivers of fire come out from him"; "diagnosed according to the reality of their condition"; second death | `30--revelation--020.md` |
| Rev 21:1-8, 23-27 | "those who worship gods that must punish or be appeased"; city lit by God | `30--revelation--021.md` |
| Mal 3:2-3; 4:1-3 | refiner; same Sun heals and reduces to stubble | OT; quote from Four Judgments, Elijah Object Lessons 2025, Bible Prophecy table |
| Isa 6:1-7; 34:9-11; 66:24; Ezek 28:18 (Gehenna, worm) | Cole study guide Week 9 material; attribute to Cole, not Jennings | OT; from `TruthLoveFreedom_StudyGuide_CosmicConflict.pdf` Week 9 |

### 4.4 Objections desk (objection -> Jennings' reply -> source -> evidence strength)

1. "God IS a consuming fire and fire comes down and devours the wicked (Rev 20:9)." -> Yes, God is the fire, and the righteous live in it (Isa 33:14-15; Dan 7; Rev 15:2; 21:23); it consumes lies and selfishness, not matter; "they perish because they refused to love the truth." QoP III; Truth About Hell; GSB ch.16; Remedy Heb 12:29, Rev 20:9. **Strong.**
2. "Rev 14:10-11: tormented with burning sulfur, smoke for ever, no rest." -> Where? "In the presence of the Lamb." *Thion* = divine fire; smoke = what is left; Remedy 14:11 "the memory... will never be forgotten"; Isa 34:9-11 Edom; mortality of the soul (1 Tim 6:16). Eternal Fire; 3Angels pp. 36-41; study guide Week 9 Day 5. **Moderate** (etymology thin).
3. "Rev 20:10: tormented day and night for ever and ever." -> Remedy "for the conclusion of their existence"; 20:14 second death = permanent consumption of all deviation from design; 2 Thess 1:9 "everlasting non-existence". No Jennings post exegetes the phrase directly. **Thin.**
4. "Matt 10:28: fear him who can destroy soul and body in hell." -> Greek names no agent; "Evil shall slay the wicked" (Ps 34:21); fear sinfulness, not the God trying to save you; first vs second death. Who Destroys the Soul? (2009). **Strong.**
5. "Without hell God is not just; heaven is apathetic toward rapists." -> Only follows under imposed law; justice is healing and restoring; the leukemia parable; "just get him some anger management classes"; the abuser faces "the mirror of undiluted truth... in front of the entire universe." GSH Misunderstanding Justice; QoP I-II; First Death. **Strong.**
6. "Rich man and Lazarus shows conscious torment in fire." -> Parable (fingers and tongues on spirits; the saved watching loved ones scream); fixed chasm = character settled; "what do the various interpretations say about God?" Lazarus and the Rich Man (2023). **Strong.**
7. "God really did rain fire on Sodom, strike Elijah's captains, kill Nadab and Abihu, drown the world." -> Conceded as first-death therapeutic acts to keep the Messiah's avenue open; Sodom "vaporization... painless"; rejects both "punishment for sin" and "Satan did it"; all will be resurrected. Flood parts 1-2; First Death; GSB 487, 497; Remedy Gen 19:24-25, Jude 7. **Moderate** (Jennings' own readers push back here; show the tension).
8. "The Bible uses 'punish' 70+ times; 'my anger will flame up like fire' (Deut 32:22)." -> Ask what happened next: "their Rock had sold them" (32:30); Babylon "delivered the destructive punch"; God speaks to "stubborn mules" in the language they can hear; build on evidentiary passages. God's Wrath (2011); Why 'Punish'? (2009); Bible Language and Judgment. **Strong.**
9. "Rev 14:18: the angel with power over fire commands the fires of judgment (2023 quarterly)." -> The lesson clipped the verse; he comes from the altar whose coal cleansed Isaiah; "no one left for me to heal"; Remedy "with the authority of the fire of truth". Fire from the Angel (2023). **Strong.**
10. "Jesus bore the Father's wrath/fire on the cross." -> No fire; darkness; "forsaken", not "killed"; wrath at the cross = letting go exactly as Rom 1; He did not die the second death; appeasement by blood is "modern Baal worship". Did Christ Die the Second Death?; Penal Substitution: Modern Baal Worship; Prewitt response. **Strong.**
11. "2 Thess 1:8 flaming fire taking vengeance." -> Remedy 1:6-9 "give up to reap the torment they have chosen... unfit to tolerate the intensity of absolute truth and pure love... everlasting non-existence"; 2:10-11. **Strong.**
12. "Mark 9 unquenchable fire and the undying worm; Matt 13 furnace." -> Not treated by Jennings; Cole: Gehenna = Valley of Hinnom (Molech, Josiah, the dump, 185,000 corpses behind Isa 66:24); "corpses, not living people" (Fudge); "unquenchable" = no one can put it out, not never finishes; Remedy Luke 3:17 "unquenchable fire of truth and love". Study guide Week 9 Days 2-3. **Moderate; attribute to Cole.**
13. "Isn't this just annihilationism / 'the fires go out' relabelled?" -> Same outcome, different cause: classic annihilationism still has God inflicting combustion as penalty; Jennings has the wicked die of their unhealed condition in the unveiled presence, with literal melting afterwards; cites Fudge, the Anglican 1995 report and EGW (DA 107-108, GC 543) as consistent. Truth About Hell opening; GSB ch.16. **Strong.**
14. "If God merely lets go He is passive, and letting someone die when you could save them is killing them." -> God has been continuously expending power to hold harm at bay; the plagues are a seven-step release; love cannot be forced; "the angriest act Love can take is to let the object of His love go"; the bone-marrow parable; letting go only "when people have rejected God so completely that they are beyond reach". God's Wrath vs Satan's Wrath (2024); Seven Last Plagues; QoP II; Healing Substitution Model. **Strong.**
15. "Why resurrect the wicked only to have them suffer and die again?" -> So the universe sees, with the gates open, that exclusion is voluntary and that "the last lie, that God is the source of death, is fully disproved"; sin never rises again. Why Resurrect the Wicked? (2010); GSB ch.16 endnote; Four Judgments. **Strong.**

### 4.5 Glossary entries (for `glossary-pop`)

Design law; Imposed / Roman (imperial) law; Consuming fire; Fire of combustion; Lies and selfishness; Thion/theion (with caveat: standard lexicons gloss "sulfur"); Wrath of God (orge) = letting go; Satan's wrath = power used to harm; Giving over / God's strange act (Isa 28:21); First death (sleep, "artificial state of grace", "stored on heaven's servers"); Second death (Rev 20:14; 21:8); Lake of fire (two senses: God's fiery presence; then the melting earth); Smoke of their torment = memory; Brightness (epiphaneia) of His coming; Unremedied condition; The Remedy (Christ; the paraphrase); Judgment as diagnosis; The four judgments; Voluntary exclusion (GC 543); Gehenna / Valley of Hinnom (Cole); Fire from the altar (Isa 6; Rev 14:18; = Holy Spirit in GSH); Babylon's wine (Remedy 14:8); Law of worship; Amygdala vs prefrontal cortex / ACC; Great Controversy.

### 4.6 Gaps and tensions the page must handle honestly

1. **Remedy red-letter gap.** Matt 5, 10:28, 13:24-50, 18:8-9, Mark 9:42-50, Luke 12:49, Luke 16:19-31 are absent from the markdown and from `the_remedy_bible.md`. Re-run `reparse.py` against `_cache\` (red spans intact) before the verse explorer ships; until then show the "missing locally" badge.
2. **The Remedy covers only Genesis, Psalms and the NT.** Isaiah 33/6/34/66, Malachi 3-4, Daniel 7, Ezekiel 28, Leviticus 10, Exodus 3/24/34, Deuteronomy 4/31-32, 2 Chronicles 5-7, Hosea 4 must be quoted in NIV/GNT as Jennings quotes them in the posts, GSB and the 3Angels magazine.
3. **Gehenna / the worm / Matt 13's furnace are never treated in Jennings' own writing** (zero blog hits for gehenna, hinnom, sheol, hades, worm). Only Week 9 of the Cole study guide covers them; attribute accordingly.
4. **The *thion/theios* etymology is asserted, not argued**, in every version (2008, 2010, 2021, magazine); present as Jennings' reading with a caveat.
5. **"For ever and ever" in Rev 20:10 and "eternal punishment" in Matt 25:46** are handled only by the Remedy paraphrase and the Isaiah 34 parallel; mark evidence as thin.
6. **Internal tensions**: Nadab and Abihu both prove the fire does not harm matter and appear in GSB's list of God-caused first deaths; "God doesn't kill (second death) anyone" sits beside affirmed first-death acts (Sodom's magma, Elijah's captains, the Flood); the same presence-fire is applied to both the second coming (2 Thess 2:8) and the post-millennial lake (Rev 20), so the timeline must show two unveilings.
7. **Brain panel rests on thin primary data in the corpus**: Newberg 2009 p.49, the Iraqi-children growth study, an undifferentiated reference list in the 2010 TV post, Shariff & Rhemtulla 2012 in a GSB endnote. Keep claims to what Jennings says.
8. **Variant versions of the same essay** (Eternal_Fire 2010 ≈ QoP III 2008 ≈ Truth About Hell 2021 ≈ GSB ch.16 ≈ 3Angels pp. 36-41); later versions add Daniel 7 "rivers of fire", Song 8:6-7, smoke = memory, the explicit bodies-remain-then-combustion sequence. Use Truth About Hell as the base text and credit the earlier ones.
9. **Not yet mined for this page**: 2021 Q4 L04 notes (wrath via Romans 1, "children of wrath"), Revelation 13 magazine pp. 20-60, the Heavenly Sanctuary pamphlet's refiner's-fire section, and the Spectrum "God's Wrath/Anger" PDF linked from the Healing Substitution Model post (`https://comeandreason.com/files/share/Spectrum_Gods_Wrath_Anger.pdf`, not local).

---

## 5. Transcription, extra scraping, and what is missing locally

### 5.1 Data work that unblocks pages (hours, not days)

| Task | Unblocks | How |
|---|---|---|
| Re-run `...\scratchpad\reparse.py` into `remedy_bible_corpus\remedy_verses.json` with book-key normalisation, paragraph flags and Psalm line breaks | Fire verse explorer (Matt 10:28, 13, 18, 25; Mark 9; Luke 12, 16), Remedy Verse Explorer, Law as Diagnostic (Matt 5), Wrath (Mark 15:34), all Gospel renderings | ~1-2 h parser hardening; source is `_cache\*.html` (`<span class="verse">` and `<span class="red">` after `<span class='verseNum'>`); Genesis 24:29 absent on the site itself, patch from `01_Genesis.docx` |
| Download one public-domain translation as JSON (WEB or KJV, ~4 MB) | the "traditional" column in Hard Passages tab 2 and in the Fire verse explorer | one-time fetch; not on disk anywhere |
| De-interleave the God-Shaped Heart ch.5 contrast table (~lines 655-663) and clean OCR ligatures / numerals in quoted passages | Two Lenses tab 2, Study companion | manual, ~1 h; re-OCR specific pages from `.folder-ocr-manifest.json` sources if needed |
| Prune the let-go regex hits (80 -> ~55 genuine) and hand-tag the 83 Remedy fire verses by category | Wrath verse wall, Fire section 5/12 | one evening |
| Extract the 126 Genesis questions from `01_Questionaire.docx` and map chapter 3's to verse ranges | Genesis 3 quiz | 30 min for chapter 3; ~2 h for all 49 |
| Fetch `Spectrum_Gods_Wrath_Anger.pdf` from comeandreason.com/files/share | Wrath page drawer | optional |

### 5.2 Transcription plan (media-only content)

Tooling exists: `C:\Personal\Software\WhisperWorkflow\.venv\Scripts\python.exe` has faster-whisper 1.2.1 + ctranslate2 4.7.1 (only `base` and `small.en` cached; download `large-v3-turbo` or `distil-large-v3`); RTX 5060 Laptop 8 GB; ffmpeg 9.0.2. Write a ~30-line batch script *outside* that repo: `ffmpeg -vn -ac 1 -ar 16000` to WAV, `WhisperModel('large-v3-turbo', device='cuda', compute_type='int8_float16')`, `vad_filter=True`, emit `.txt` plus timestamped segments `.json`; fall back to `device='cpu', compute_type='int8'` with `small`/`medium` if cuDNN 9 DLLs do not load. Expect 10-20x realtime on GPU, so the whole backlog is a few hours of compute.

Priority order:
1. **Healing The Mind** Chattanooga seminar, 8 MP4, 6.1 h (`...\ComeAndReason\Healing The Mind\`): the only neuroscience-and-love seminar not in any text; feeds page 7 (Brain Map).
2. **Could It Be This Simple** audiobook, 17 MP3, 5.2 h (`...\ComeAndReason\Could it be this Simple\`): clean single voice; gives a searchable text of the book even though the PDF exists (chapter 12 MP3 missing).
3. **2022 Q2 Q&A sessions**, 12 MP4, 6.3 h: listener questions that exist nowhere in text; feeds the blog/notes browser and Genesis track.
4. **Journal of the Watcher** (128 min), **human-sexuality-god-s-design.mp4** (97 min), **LoveCourse\Lesson1.mp4** (21 min), **2022 Q3 L11 Waiting in the Crucible** (71 min, no notes): unique material for the missing marriage/sexuality and suffering pages.
5. The Q2/Q1/Q4 class videos (14 h) only if verbatim elaboration beyond the notes is wanted.
6. Skip the Remedy NT MP3s (text exists). Verse-level audio sync would need forced alignment (whisperX/aeneas against the known Remedy text, ~25 h of audio, 2-3 days plus compute); chapter-level sync is a filename map and ships in phase 1.

### 5.3 Missing locally (cannot be fixed by parsing)

- **Old Testament outside Genesis and Psalms** is not in The Remedy: Isaiah 33:14-15, Isaiah 6, Isaiah 34, Isaiah 66:24, Malachi 3-4, Daniel 7, Ezekiel 28, Leviticus 10, Exodus 3/24/34, Deuteronomy 4/31-32, 2 Chronicles 5-7, Hosea 4, 1 Kings 18-19, 2 Kings 1-2. Quote these in the translation Jennings uses in the source post (usually NIV, sometimes GNT) and show no Remedy column.
- **Genesis 24:29** absent from the website itself (use `01_Genesis.docx`).
- **2022 Q1 Hebrews notes** exist only for lessons 1-4 (the quarterlies ERQ122_00-13 give the outline; Remedy Hebrews is complete).
- **WeeklyLessons\Week09.pdf** is missing; use the complete Cosmic Conflict guide PDF.
- **Jennings on Gehenna / Hinnom / the worm / Sheol / Hades**: nothing in 611 posts or the two books; only the Cole study guide.
- **A traditional (penal) reading column**: no public-domain Bible JSON on disk; no critic texts beyond what Jennings quotes (Prewitt paper response, the hell-apologetics quotes in GSH ch.6).
- **Revelation 13 magazine pp. 20-60** and the **CRT magazine's "How to End Racism" plan** were not read in the slices; **The Lie magazine** was read only for Addendum A; **Heavenly Sanctuary pamphlet** (14.7k words) and **Wedding of Christ** were skimmed by TOC; **2022 Q3** folder (50 files) and **The Journal of the Watcher** untouched.
- **`28 Fundamerntal Beliefs Through the Design Law Lens.pdf`** has no text layer and is a Genesis Road publication; body text would need OCR of `...\scratchpad\fb28\p-01..16.png`.
- **CIBTS chapter 12 ("Forgiveness") MP3** is missing from the audiobook set.
- **Newberg / Shariff / Centerwall / Danese primary papers** are cited but not on disk; the pages should cite them as Jennings cites them.

### 5.4 Finding the existing Seven Levels page

The previous sweeps grepped `*.html` for "moral development" and "seven levels" under `C:\Personal`, `C:\Claude`, OneDrive, Documents, Downloads, Desktop. Before rebuilding, run one wider pass: (a) include `*.htm`, `*.html.txt`, `*.md` and files with no extension, and search for distinctive strings from the handout such as "Marketplace exchange", "Healing Substitution", "Satisfaction theory", "Understanding friend of God", not just the title; (b) include `C:\Users\pwess\` (AppData\Local and Roaming, where editors and browsers autosave), `C:\Personal\Writing\`, `C:\Personal\Software\`, any secondary drive, and the Dropbox mirror `C:\Personal\Documents\Dropbox\Personal\Religion\`; (c) sort by modification date near the time the Remedy corpus was scraped (2026-04-29) and the OCR of the books (2026-09-03 screenshots); (d) check whether it was a claude.ai artifact that was never saved to disk (the artifacts connector's `list_artifacts` with query "Seven Levels" would show it) or a Claude Code session transcript (`search_session_transcripts` for "Seven Levels"). If none of these hit, rebuild from `SevenLevelsOfMoralDevelopment.pdf` + `GodShapedHeart.md` 363-400 in half a day using the kit's `level-stepper`; the rebuild is then the first node of the hub.
