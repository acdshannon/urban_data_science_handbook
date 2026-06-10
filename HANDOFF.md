# Handoff: finishing Chapters 2 & 4 (the data pass)

*Status as of June 2026. Delete this file when the pass is complete.*

Chapters 2 and 4 are fully written — final prose, code cells, exercises,
sidebars — but their code has not yet executed against real data, because the
authoring session's sandbox could not reach the portals. Every place where
executed results must land is marked `TODO:data` (grep for it). Nothing else
is pending.

## The pass, in order

1. **Build snapshots** (network required):
   - `python scripts/fetch_nyc_311.py` — small aggregate queries + rat points
     + NTA geojson. If the NTA dataset id `9nt8-h7nd` or the census table id
     is stale, search the portal catalog and fix the script.
   - `python scripts/fetch_melbourne.py` — downloads the 2009–2022 archive ZIP
     attachment + live export, writes `hourly.parquet`. **Inspect both
     schemas first**; the script's reconcile step has a marked TODO where
     column renames go.
2. **Inspect, then resolve every `TODO:data`** in
   `chapters/02-the-urban-data-toolkit.qmd` and
   `chapters/04-machine-learning.qmd`. Each marker says what it needs (a
   figure built, a number stated in prose, a sensor chosen). Prose claims
   must match what the data actually shows — rewrite the sentence, not the
   data.
3. **Execute and render**: `quarto render` (Quarto ≥ 1.7; binary at
   `/tmp/quarto/bin/quarto` in the original session). Commit the `_freeze/`
   directory — CI renders from it and has no Python.
4. **Quality gates** before pushing: every figure readable at book width;
   no figure contradicted by its caption; chapter runs top-to-bottom from a
   fresh clone offline (snapshots committed); prose pass for stray
   placeholder text.
5. Push to `claude/clever-ptolemy-ekcpck` (PR #2), flip it from draft when
   green.

## Style contract for any prose edits

Follow the voice doc (Google Doc "Alex's Writing Voice"): instance before
concept, colon-definitions for load-bearing terms (italicized once), triads,
em-dash parentheticals, short punchy paragraphs after long ones, dry asides,
no throat-clearing transitions, no "honestly/crucially/delve", no closing
benedictions. Russell-ish willingness to judge. The existing chapter text is
the calibration sample.
