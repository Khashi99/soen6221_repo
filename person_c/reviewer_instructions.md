# Independent human review

Reviewer 1 receives reviewer_1.csv (100 comments). Reviewer 2 receives only
reviewer_2_overlap.csv (30 comments) and these instructions. Do not share
sampling_admin.csv, detector predictions, proposed labels, or the other
reviewer’s decisions before both independent sheets are complete.

Read each raw comment and its code context. Pinned GitHub links identify the
exact source snapshot. Expand context if the excerpt is insufficient. Keep
comment IDs, source metadata and row membership unchanged.

Use exactly one label: SATD, non-SATD or uncertain. SATD is a developer’s
acknowledgement of an existing compromise, deficiency, shortcut or deferred
corrective work. Imperfect code by itself is not an admission. Ordinary
documentation, resolved issues and optional enhancements are non-SATD when
context supports that interpretation. Use uncertain when the evidence is
insufficient. Add a short reason for every decision.

Examine markers in quotations, negations, identifiers such as write_todos and
todo_list, expected test failures, routine deprecation documentation and
optional feature requests. An identifier mentioning a todo tool is not
inherently debt, but a genuine debt admission involving that tool may qualify.
Do not infer the label from detector group or the presence of a keyword alone.

Each reviewer labels independently as a human. LLM or Codex suggestions may
help calibration separately but cannot be reported as human ground truth or
an independent human reviewer. Retain reviewer identities and completion dates
in your team’s review record without fabricating names or independence.

After independent review, compare the 30 overlap comments and record final
resolved decisions in adjudication.csv, retaining the original independent
labels and reasons. Reviewer 1’s other 70 comments also need final decisions.
Retain unresolved uncertainty rather than silently forcing a binary label.

Run review_statistics.py only with these retained sheets. The report uses
actual paired binary N and excludes uncertain/blank pairs from kappa, reporting
those exclusions. Expected agreement of 1 makes kappa undefined. Precision is
population-weighted across strict and loose-only groups. Do not claim
per-framework precision from these small framework subsamples or absolute
recall from candidates alone. Precision >60% and kappa >0.7 are team targets;
do not repeatedly tune patterns to pass them. Any post-calibration revision
requires a fresh held-out sample.
