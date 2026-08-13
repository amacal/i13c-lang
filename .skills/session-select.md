Investigate the repo and propose exactly 3–5 candidate topics for the next session.
Follow every CLAUDE.md rule, especially "Session units" and "Session selection".
Research/report only — no user contact, no AskUserQuestion, no picking a winner. Return
findings as text; the calling conversation presents them. No scripts — every lookup is
`Read`/`Grep`/`Glob` against `.index/`/`.history/`, per `.index/schema.yml` and
`.history/schema.yml`.

## Steps

1. **Sibling repo awareness (informational only — skip entirely if `.other/` doesn't
   exist).** `.other/` may hold sibling learning repos (e.g. `hard-with-llm`,
   `math-with-llm`) checked out purely for reference. `ls .other/` to enumerate them.
   For each subdirectory that has its own `.git`:
   - `git -C .other/<repo> status --porcelain` first. Any output → local changes are
     sitting there uncommitted; skip fetch/pull for that repo this run and just note
     "not refreshed, has local changes" in the report. Never touch its working tree.
   - Otherwise `git -C .other/<repo> fetch`, then check whether the local branch is
     behind its upstream (e.g. `git -C .other/<repo> log HEAD..@{u} --oneline`). If
     behind, `git -C .other/<repo> pull --ff-only` — fast-forward only, never a
     merge/rebase, never `--force`, never a push. If `--ff-only` fails (diverged
     history), leave it alone and note the divergence; never resolve it.
   - Once current, skim its recent session record for date/title/one-line-summary only
     — `ls .history/*/*.yml | sort | tail -6` and a quick `Read` of just the
     `date`/`title` fields (or its `summary.txt` equivalent under `.index/sessions/`).
   - Purpose is situational awareness only: how recently and how intensely the user has
     been working elsewhere, and on what topics — never used to justify or rule out a
     candidate's prerequisites (this repo's scope stays self-contained regardless of
     what's happening in a sibling repo), and never used to infer personal/psychological
     conclusions. Report activity facts (dates, titles, cadence), not assessments of the
     person.
   - Report this as its own clearly labeled section in the final report-back step,
     separate from the candidate list.

2. **Done set.** `ls .index/sessions/` (each directory's `meta.yml` `title:` field is
   the exact Session Title) — this IS the done set. Cross-check against `src/i13c/**`
   for pipeline stages with little/no session coverage. Fall back to reading every
   `.history/*/*.yml` in full only if `.index/` looks stale/incomplete.

3. **Dependency graph.** `grep -rl "<title>" .index/sessions/*/prerequisites.yml` for
   reverse "required-by" lookups; `Read .index/sessions/<slug>/derived_from.yml`/
   `unlocks.yml` for a session's own forward relationships — genuine prerequisites kept
   separate from softer `uses_concepts.yml`/`related_to.yml`. `ls .index/branches/` +
   `Read` each for branch structure, `ls .index/open-gaps/*/` + `Read` each for "what's
   underexplored". `.history/` carries no dependency field by design — if `.index/`
   looks stale, re-derive from the source files directly, never from a `.history/`
   `Depends on`/`Unlocks` field (none exists). Use `grep -l '"<title>"' .history/*/*.yml`
   or `grep -r "<term>" .history/*/*.yml` only for session-event citations (a specific
   bug, a specific abandoned approach) when needed.

4. **Spec-study position.** If any spec-study sessions exist (`grep -l 'kind:
   "spec-study"' .index/sessions/*/meta.yml`), find the most recent by date, identify
   the document/section from its `source` field. Locate the PDF in `docs/`
   (`find docs -name "*.pdf"`), determine the next relevant section by rendering
   candidate TOC/section-heading pages to PNG via `pdftoppm`/`pdftocairo` and reading
   them with multimodal vision — never `pdftotext`, not even for the TOC (per "Spec
   study sessions"'s total ban on text-extraction against these documents). Keep every
   rendered `.tmp/*.png` file (never delete mid-run) and record its physical filename
   alongside the printed page number it shows, for the report-back.

5. **Generate 3–5 candidates.** Per candidate:
   - Confirm not already in the done set.
   - Confirm its full prerequisite chain is already covered — except the
     stepping-stone exception in "Session selection", named explicitly with the larger
     target it unlocks.
   - Classify: harder variant/extension, cross-backend comparison (native vs. LLVM),
     gap-filling, or stepping-stone.
   - 1–2 sentences on why it's interesting given what's done.
   - Its prerequisite chain (existing sessions/files it draws on).

6. **Force genuine breadth.** Don't let all candidates be the next link in the most
   recent chain. Run `.index/schema.yml`'s `concept_frequency` query
   (`grep -h '^- ' .index/sessions/*/concepts.yml | sed 's/^- //' | sort | uniq -c | sort -rn`)
   to see, concretely, which pipeline stages/tags are saturated versus barely touched —
   cite the actual counts (e.g. "x86-encoding: 9 sessions, register-allocation: 1") when
   justifying a candidate, rather than relying on impression. Check whether a
   cross-backend option (native vs. LLVM for the same construct) or an underexplored
   stage (liveness, ELF relocations, optimization) is viable given the done set, include
   at least one if so. This frequency count is a descriptive signal only — it does not
   replace the hand-curated judgment in `.index/selection-context/`, which stays a
   human/agent judgment call, not a formula.

7. **Report back** a plain list of the candidates (title, classification, rationale,
   prerequisite chain), plus — if any PDF pages were rendered — the full list of
   `.tmp/*.png` files produced this run mapped to their printed page numbers, plus — if
   step 1 found anything — the sibling-repo awareness section (which repos exist,
   whether each was refreshed or skipped and why, and the handful of recent session
   facts pulled from each). Not a user-facing menu, no questions asked — structured
   findings for the calling conversation to present interactively.
