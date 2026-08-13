Audit the files the write agent (`.skills/session-close.md`) just wrote/edited/removed
against every CLAUDE.md rule and the two schema files. You are given that agent's file
list verbatim in your prompt — check those exact files, never re-derive "what changed"
by globbing the whole tree. Research/report only — no file writes, no user contact. No
scripts — every check is `Read`/`Grep`/`Glob` against `.index/`/`.history/`, per
`.index/schema.yml` and `.history/schema.yml`.

## Checks

1. **`.history/` entry.**
   - Filename date matches its own `date:` field; filename slug matches
     `slug_algorithm(title)` exactly.
   - `session`'s fields are exactly `[files, source, status, attempted, explored, tried,
     corrections, bugs_found, completed, not_completed, open_questions, notes]`, all
     present, none extra.
   - Every list field is either the literal scalar `—` or a non-empty YAML list — never
     an empty list `[]`, never `—` mixed with real entries.
   - Spec-study entries: `bugs_found: —` and `files: —`, `source` is non-`—`.
     Implementation entries: `source: —`, `files` is a non-empty list of real paths.
   - No exposition: scan `attempted`/`explored`/`tried`/`corrections`/`completed` for
     full encoding derivations, resolution-algorithm walkthroughs, or complexity
     arguments — a named result is fine, a reproduced derivation is not. No
     `Depends on`/`Unlocks`-shaped field. No personal/psychological content anywhere.
   - No file under `.history/` other than the one just written was modified this
     session, unless the write agent's report states one of the immutability rule's
     explicit exceptions (factual-error correction, formatting fix, filename/date fix,
     genuinely-omitted addition) and gives a real reason.

2. **`.index/sessions/<slug>/` directory.**
   - Exactly 10 files present: `meta.yml`, `summary.txt`, and the 8 relationship lists.
   - `meta.yml` fields in order `[title, kind, files, source, date]`; `kind` is
     `implementation` or `spec-study`; `files`/`source` follow the same — /non-—
     pairing as the `.history/` entry; title matches the `.history/` entry's title
     exactly.
   - `summary.txt` is plain text, one factual sentence, no exposition.
   - Every title referenced in `prerequisites.yml`/`uses_concepts.yml`/
     `derived_from.yml`/`related_to.yml` resolves to an existing
     `sessions/*/meta.yml` title (`grep -l 'title: "<ref>"' .index/sessions/*/meta.yml`
     finds exactly one file).
   - Every title in `unlocks.yml`/`future_targets.yml` resolves to either a session or a
     `.index/future-targets/*.yml` title.
   - Every tag in `concepts.yml`/`capabilities.yml` matches `^[a-z0-9]+(-[a-z0-9]+)*$`.
   - Relationship classification is honest, not just chronological: spot-check one
     `prerequisites.yml` entry against CLAUDE.md's test ("materially harder to follow
     without X") — flag it if it looks like it's there only because it came first.
   - Every path in `meta.yml`'s `files` field exists under `src/i13c/`.

3. **Future targets / branches (only the files in the write agent's report).**
   - Any new `.index/future-targets/<slug>.yml` has `status: not-completed` and
     non-empty `mentioned_by`/`evidence`.
   - No title exists as both a `sessions/*/meta.yml` title and a
     `future-targets/*.yml` title — if the write agent's report claims it removed a
     stale future-target file, confirm it's actually gone.
   - Any touched `branches/<slug>.yml` still has every `sessions`/`frontier` entry
     resolving to a real session title.

4. **Boundary check.** Confirm no file under `src/`, `scripts/`, or `data/` was touched
   this session by anyone acting as Claude (the write agent's report should list only
   `.history/`/`.index/` paths — anything else is a violation of "What Claude must
   never do").

## Report back

List every violation found, each with the exact file/field and what's wrong — specific
enough that the calling conversation can fix it directly without re-investigating. If
nothing is wrong, say so plainly. Never fix anything yourself; never contact the user.
