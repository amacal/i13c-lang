Write the `.history/` entry and the `.index/` session directory for the session that
just ended. Follow every CLAUDE.md rule exactly. No scripts — every write here is a
direct `Write`/`Edit`; every lookup is `Read`/`Grep`/`Glob` against `.index/`/`.history/`,
per `.index/schema.yml` and `.history/schema.yml`. There is no notes file to write in
this repo (see CLAUDE.md's "Session units") — do not create one.

## Steps

1. **Identify the files.** List the primary `src/i13c/**` paths created or primarily
   worked on this session — `git status`/`git diff --stat` against the session's actual
   work is the fastest way to confirm this. Spec-study session (no code) → identify the
   document/section instead.

2. **Write the `.history/` entry.** Determine `date` from today (or from the
   introducing git commit if the session's code was already committed). Derive
   `<slug>` from the exact Session Title via `.index/schema.yml`'s `slug_algorithm`.
   `Write` a single new file at `.history/<YYYY-MM>/<date>-<slug>.yml` (create the month
   directory if it doesn't exist yet — nothing else to set up, no header/chaining
   fields) with exactly the shape in `.history/schema.yml`'s `file_format`:

   ```yaml
   date: "YYYY-MM-DD"
   title: "Exact Session Title"
   session:
     files: [src/i13c/..., src/i13c/...]   # or — for spec-study sessions
     source: —                              # or "Document Name, section/table" for spec-study sessions
     status: completed
     attempted: [...]
     explored: [...]
     tried: [...]
     corrections: [...]
     bugs_found: [...]                      # always — for spec-study sessions
     completed: [...]
     not_completed: [...]
     open_questions: [...]
     notes: [...]
   ```

   Fill every field per CLAUDE.md's field semantics, `—` for empty (never omit a field,
   never an empty list, never mix `—` into a populated list; each list field is either
   the literal `—` or a non-empty list). Observable session events only — no encoding
   derivations/resolution-algorithm descriptions/complexity arguments (there is nowhere
   for this exposition to live in this repo but the dialogue itself and the user's own
   commit messages/comments — a history entry may name a result in passing as
   investigation evidence, never reproduce it), no `Depends on`/`Unlocks` field, no
   personal info/personality/psychological interpretation/subjective judgment. This
   `Write` is the entire operation — never touch any other file under `.history/`.

   **Name results, never restate their derivation.** A recurring mistake: writing
   "Implemented callsite resolution for variadic calls (walks the call's argument list,
   widening each operand to the callee's declared width before binding)" instead of
   just "Implemented callsite resolution for variadic calls." The parenthetical is
   exposition that belongs nowhere but the dialogue/code comments — never restate it
   here, no matter how short it seems. The one exception is a genuinely concrete fact
   used as a correction/test case (e.g. "expected ModRM byte 0x45; observed 0x44 — off
   by one in the displacement-size check" while fixing a specific bug) — that's
   investigation evidence, not exposition, and stays.

3. **Write the `.index/sessions/<slug>/` directory (10 files) — never a full-tree read,
   no script.** Treat every already-completed session's existing files as ground truth;
   do not re-read every old source/`.history/` file to re-derive them from scratch.
   Classify honestly against CLAUDE.md's "Fast index (`.index/`)" tests, using targeted
   lookups only:
   - `grep -l 'title: "<candidate title>"' .index/sessions/*/meta.yml` to confirm a
     candidate prerequisite/related session actually exists and get its directory.
   - `Read` that session's own `.yml`/`.txt` files (not the whole tree) for the specific
     reused fact.

   Then `Write` all 10 files in `.index/sessions/<slug>/`: `meta.yml`
   (`title`/`kind`/`files`/`source`/`date`), `summary.txt` (plain text, one sentence),
   and `prerequisites.yml`/`uses_concepts.yml`/`derived_from.yml`/`related_to.yml`/
   `unlocks.yml`/`future_targets.yml`/`concepts.yml`/`capabilities.yml` (each a YAML
   list of exact titles/tags, or the literal scalar `—`, per `.index/schema.yml`'s
   `empty_field_convention`).

4. **Future targets.** For each title in this session's own `future_targets.yml` that
   isn't already a `.index/future-targets/<slug>.yml` file, `Write` one
   (`title`/`status: not-completed`/`mentioned_by`/`evidence`, per `.index/schema.yml`).
   If this session's own title matches an *existing*
   `.index/future-targets/<slug>.yml`, `rm` that file now — a title cannot be both a
   pending target and a completed session.

5. **Branches.** If this session extends an existing branch, `Edit`
   `.index/branches/<slug>.yml`: append the title to `sessions`, and replace `frontier`
   with whatever the new frontier genuinely is (usually just this session, but say so
   explicitly if a sibling session in the same branch is still also frontier). If this
   session opens a brand-new branch, `Write` a new `.index/branches/<slug>.yml`
   (`title`/`sessions`/`frontier`/`explicit_future_targets`).

6. **Everything else is curated, not mechanical — touch only what genuinely changed.**
   `.index/selection-context/active-branches.yml`, `candidate-signals.yml`, and
   `reusable-recent-capabilities.yml` are hand-curated judgment — don't try to make them
   a formula. `.index/open-gaps/<category>/<slug>.yml` and `.index/edges/<slug>.yml`
   are curated prose, written rarely. Edit only the specific file this session's
   evidence actually changes. Never touch `.index/schema.yml` itself as part of a
   normal close. Nothing needs to be written for `recent_sessions` or
   `explicit_unfinished_targets` — those are computed on demand, never stored.

7. **Retrospective revision of an *older* session's fields is still allowed** (that's
   `.index/`'s whole point of difference from `.history/`), but is a deliberate,
   targeted `Edit` to that one file — only when this new session's evidence
   specifically implicates that older classification (state the reason in your
   report). Never a routine side effect, never a from-scratch re-derivation of an older
   session just to double-check it, never mirrored into that older session's
   `.history/` entry.

8. **Validate before finishing — no script, run these directly with Grep/Glob** (the
   exact checks are in `.index/schema.yml`'s `validation` section):
   - `ls .index/sessions/<slug>/ | wc -l` is exactly 10.
   - Every title in every `prerequisites.yml`/`uses_concepts.yml`/`derived_from.yml`/
     `related_to.yml` you just wrote resolves: `grep -l 'title: "<ref>"' .index/sessions/*/meta.yml`
     finds exactly one file.
   - Every title in `unlocks.yml`/`future_targets.yml` resolves to either a session or a
     `.index/future-targets/*.yml` title.
   - No title exists as both a `.index/sessions/*/meta.yml` title and a
     `.index/future-targets/*.yml` title.
   - Every tag in `concepts.yml`/`capabilities.yml` matches `^[a-z0-9]+(-[a-z0-9]+)*$`.
   - Every path in `files.yml`/`meta.yml`'s `files` field actually exists under
     `src/i13c/`.

9. **Report back** every file you wrote/edited/removed, verbatim, with full paths (the
   new `.history/` entry path, the `.index/sessions/<slug>/` directory and its 10
   files, any future-target/branch files touched, any retrospective edit and its stated
   reason) — the calling conversation passes this into the verify agent's prompt so it
   can check the actual files directly instead of re-deriving "what changed" by
   globbing the whole tree.
