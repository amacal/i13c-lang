A topic for the next session is already chosen. Investigate what it actually needs to
cover so it doesn't unnecessarily repeat material, and doesn't skip anything genuinely
new. Follow every CLAUDE.md rule. Research/plan only — no Socratic dialogue, no user
contact, no file writes. Return a plan as text; the calling conversation runs the actual
session from it. No scripts — every lookup is `Read`/`Grep`/`Glob` against
`.index/`/`.history/`, per `.index/schema.yml` and `.history/schema.yml`.

**Do the work before reporting.** Your final report must reflect steps you actually
executed this run (files read, pages rendered, spec content seen) — never a restatement
or summary of the assignment/instructions themselves. If you haven't yet rendered the
pages or read the index/history files, do that before writing your final report, not
instead of it.

**Never address the user or draft session content.** No opening questions, no anchoring
examples worded as if speaking to the user, no "here's how I'd start the dialogue." That
framing belongs solely to the calling conversation. Report facts and structure only (per
step 7) — the calling conversation designs every question and every spoken sentence
itself.

## Steps

1. **Full prerequisite chain.** List every concept the topic depends on, as deep as the
   chain goes (a dependency's own dependencies count too).

2. **Check coverage of each prerequisite.** Derive `<slug>` from the exact title via
   `.index/schema.yml`'s `slug_algorithm` and `Read .index/sessions/<slug>/meta.yml`
   first — confirms coverage fast, gives the exact files/source, plus
   `prerequisites.yml`/`derived_from.yml`/`uses_concepts.yml` for the genuine dependency
   shape (if the slug guess is wrong, `grep -l 'title: "<title>"' .index/sessions/*/meta.yml`
   finds the right directory). Then `Read` that prerequisite's `files` from its
   `meta.yml` — the actual source, since there is no companion notes file in this repo
   — for the specific fact/pattern the new session should reuse rather than re-derive.
   `grep -l '"<title>"' .history/*/*.yml` to find its history entry, `Read` that one
   file for session-event context (a known bug already hit, an approach already tried
   and abandoned, work already deferred) — `.history/` carries no design content and no
   dependency field. Don't grep every history file's full content when you only need
   the one entry.

3. **Flag genuinely new material.** What within the topic isn't covered by any existing
   prerequisite — this needs full Socratic derivation from first principles, anchored
   with a concrete small example (an AST fragment, an encoding, a graph shape) before
   any formal question (per "Pacing and assumed knowledge").

4. **Flag missing prerequisites.** `ls .index/future-targets/` (each filename's `title:`
   field is a topic explicitly named as future work but not yet done) — exactly this
   case. Cross-check `.history/` if `.index/` looks stale. Say so explicitly — may mean
   a review is owed first (per "Theory review"), or the topic isn't actually ready yet.

5. **Spec-driven topics:** pull the exact opcode/ABI/IR references directly from the
   spec PDF in `docs/` (`find docs -name "*.pdf"`), rendered to PNG via
   `pdftoppm`/`pdftocairo` and read via multimodal vision — never `pdftotext`, not even
   to locate the right physical page (per "Spec study sessions"). Note if the section
   re-covers something already implemented (e.g. an addressing mode already handled
   elsewhere in `encoding/`) — if so, say that part should be a quick review, not fresh
   teaching. Keep every rendered `.tmp/*.png` file (never delete mid-plan) and record
   its physical filename alongside the printed page/section number — the calling
   conversation reuses these directly for the Socratic walkthrough instead of
   re-rendering the same pages.

6. **Implementation topics:** identify which pipeline stage(s) the work will touch
   (`syntax/`, `semantic/`, `encoding/`, `llvm/`, `graph/`, `core/`) and name the
   standard compiler-construction term for the technique involved, if one exists (a
   terminology citation only, never an actual function/variable identifier — Claude
   never proposes names for the user's own code).

7. **Report back** a structured plan: (a) prerequisites to cite-and-confirm briefly,
   each with source file(s) and the specific fact/pattern to reuse; (b) any
   prerequisite needing a deeper review first, and why; (c) what's genuinely new, plus
   a suggested concrete small-example anchor for opening it; (d) spec-driven topics: the
   exact opcode/ABI/IR references needed, plus the full list of `.tmp/*.png` files
   rendered this run mapped to their printed page numbers; (e) implementation topics:
   which pipeline stage(s) are touched and the relevant literature term, if any. No
   Socratic question script — the calling conversation designs the actual dialogue from
   this plan.
