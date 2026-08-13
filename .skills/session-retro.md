Every 10 completed sessions, audit CLAUDE.md's and `.skills/*.md`'s calibration against
recent real evidence. Research/report only — never edit CLAUDE.md or any `.skills/*.md`
file, never talk to the user, never pick a winner among your own suggestions. No
scripts — every lookup is `Read`/`Grep`/`Glob` against `.index/`/`.history/`.

## Steps

1. **Gather evidence.** `ls .history/*/*.yml | sort | tail -10` for the 10 most recent
   sessions. `Read` each entry in full. Cross-reference each session's
   `.index/sessions/<slug>/` directory for how it was classified.

2. **Check the hint ladder in practice.** CLAUDE.md's "Illustrative snippets" section
   permits a narrow escalation path: pointer → named concept → narrowing question →
   snippet. Scan the 10 sessions' `corrections`/`not_completed`/`open_questions` for
   signs the ladder was skipped (a session where the first hint was already a snippet)
   or under-used (a session stuck for many turns where a snippet was never reached).
   Cite the specific session/field, never a vague impression.

3. **Check prerequisite calibration.** Did any of the 10 sessions' `corrections` reveal
   a prerequisite that CLAUDE.md/the select or plan agent should have flagged but
   didn't (a concept treated as background that wasn't actually covered)? Cite the
   specific session.

4. **Check breadth.** Run `.index/schema.yml`'s `concept_frequency` query. Did the last
   10 sessions concentrate heavily on one pipeline stage despite `.index/` showing
   others are barely touched? If so, that's a signal the select agent's breadth rule
   isn't landing — cite the actual counts.

5. **Check session-unit sizing.** CLAUDE.md's "Session units" expects one coherent
   design decision per session. Scan for sessions whose `files` list or `attempted`
   field suggests several unrelated decisions got bundled into one closing entry, or
   conversely a decision that got split across many oddly-narrow sessions.

6. **Check the closing ritual's discipline.** Spot-check 2–3 `.history/` entries against
   "Never in a history entry" — any exposition (an encoding derivation, a resolution
   walkthrough) that should have stayed in the dialogue/code comments only.

7. **Propose concrete wording changes, not vague impressions.** For each finding, quote
   the exact CLAUDE.md or `.skills/*.md` line(s) implicated and suggest a specific
   replacement. If a rule seems fine and nothing in the evidence contradicts it, say so
   — don't manufacture a finding to fill space.

8. **Report back** every finding with its citation (session/field) and proposed wording
   change, for the calling conversation to present in chat for accept/reject. Never
   apply anything yourself.
