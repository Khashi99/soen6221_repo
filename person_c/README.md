# SOEN 6221 Person C fresh independent study

The user authorized this new study because the pilot inputs are unavailable.
Ten newly pinned framework snapshots produced **66,754 comment blocks**.
These are independent results with proposed patterns, not pilot reproduction
or a verified implementation of the Potdar–Shihab 62-pattern dictionary.
Original attached documents are unchanged and copied to `references/`.
Earlier preparation files and unverified team counts are kept in `preparation/`.

## Measured totals

| Variant | Candidates | Added versus strict | Removed versus strict |
|---|---:|---:|---:|
| Strict plus standalone DEPRECATED | 1,613 | 972 | 0 |
| Strict without DEPRECATED | 641 | 0 | 0 |
| Strict without DEPRECATED anchored on every comment line | 597 | 0 | 44 |
| Strict plus proposed loose patterns without DEPRECATED | 693 | 52 | 0 |

The strict markers are TODO, FIXME, XXX and HACK using case-insensitive whole
words. The five proposed loose families are workaround variants, hardcode
variants, temporary solution, kludge and ugly. Exact regexes and one-line
reasons are in `patterns.independent.json` and `keyword_configuration.csv`.
Standalone DEPRECATED is diagnostic only. It does not enter the main review
pool unless another retained pattern also matches. No pattern was tuned after
sampling. The set is fixed for initial validation, not finalized as validated.

All tracked Python `.py` files are eligible, including tests and Python
examples; docstrings and non-comment strings are excluded. Adjacent standalone
comment lines merge only at identical indentation with no blank line or code
between them. Inline comments remain separate. Raw # tokens and code context
are retained. Leading whitespace and the first # are removed only in the
matching copy. Anchor on each constituent line, independently of word
boundaries. Keep repeated text at different source locations distinct.

Exclusions are explicitly listed in `snapshots.json`. All 12,653 tracked Python
files were eligible; no files matched those excluded directory names in these
snapshots. Source packages called build or dist are retained. There were zero
tokenization failures. Density uses all extracted blocks per framework.
Strict/full candidate coverage is 641/693 = 92.50%; **this is not SATD recall**.

## Main deliverables

- `results/person_c_keyword_validation.docx`: measured Word report, with
  provisional patterns, per-framework sensitivity, validation plan and limitations.
- `results/sensitivity.csv`: all 44 framework/total variant rows, including
  density and added/removed counts relative to strict without DEPRECATED.
- `results/reviewer_1.csv`: 100 real comments, raw text, context, pinned source
  links and blank labels/reasons. Group is hidden.
- `results/reviewer_2_overlap.csv`: designated random 30-comment overlap for
  an independent second human reviewer; labels/reasons are blank.
- `results/adjudication.csv`: separate final decisions, initially blank.
- `results/sampling_admin.csv`: hidden detector groups, inclusion probabilities
  and population/sample sizes. Do not distribute with blinded reviewer sheets.
- `results/sample_framework_coverage.csv`: sample counts by group/framework;
  all ten frameworks are represented, but no per-framework precision is inferred.
- `results/edge_case_audit.csv`: 23 targeted cases, distinct from random validation.
- `results/matches.jsonl`: all matched block/variant records and pattern spans.
- `extracted/comments.jsonl`: complete extracted corpus including unflagged blocks.
- `snapshots.json`, extraction/run manifests: full pinned SHAs, scope,
  normalization, seed 6221, Python/detector versions and input/configuration hashes.
- `review_statistics.py`: group precision, uncertainty bounds, Wilson intervals,
  population-weighted precision and raw agreement/Cohen’s kappa after human labels.

## Human input and source checks still required

No human labels have been supplied. Label all 100 reviewer-1 rows and the
independent 30-row overlap before discussion, then record final decisions in
adjudication.csv without changing the original labels. Use SATD, non-SATD or
uncertain and provide reasons. See `reviewer_instructions.md`.

Sampling is 50/641 strict and 50/52 loose-only without replacement, with seed
6221. The two groups are disjoint. Inclusion probabilities are 7.8003% and
96.1538%. Weight group precision by 641/693 and 52/693, not by equal sample
sizes. Uncertain pairs are excluded from binary kappa and actual paired N is
reported. Expected agreement of 1 produces undefined kappa. Wilson intervals
apply to resolved group proportions; uncertainty bounds retain unresolved
cases. Codex outputs are not human labels or an independent human review.

Original-paper verification is pending: HTTPS requests to arxiv.org and
melvidoni.rbind.io received proxy 403 responses. Both domain additions are
saved in the environment configuration draft; application to this runtime is
not confirmed. Review and save those changes in environment settings, then
publish the environment, or supply the original paper PDFs for source checks.
The source leads are recorded in `source_provenance.json`; no unverified
benchmark or canonical dictionary claims are made. Proposals are distinguished
from adapted marker names in the supplied context.

Reconcile Person B’s provisional sampling wording before adopting the new
693-candidate full pool. This detector evaluation uses 100 comments and
Cohen’s kappa; the later 600-comment taxonomy study and Fleiss’ kappa are
separate. No teammate messages were sent. Any pattern change after calibration
requires a new held-out validation sample. Absolute recall is not estimated.

## Reproduce in this cloud machine

Use the existing checkout; no new Git worktree is needed. Working directory:
`/workspace/soen6221_repo/person_c`. Research snapshots are input caches in
`/workspace/satd-source-cache`, not extra development projects.

```sh
python acquire_snapshots.py
python satd_compare.py extract --manifest snapshots.json --out extracted_replay
python satd_compare.py compare --corpus extracted_replay/comments.jsonl --config patterns.independent.json --out results_replay
python -m unittest -v test_satd_compare.py test_review_statistics.py
```

The acquisition script restores/verifies exact pinned SHAs when snapshots.json
exists, rather than substituting a new HEAD. The corpus and comparison need
only the Python standard library; no framework dependencies are installed.
After human review, run `python review_statistics.py --directory results`.
Do not rerun comparison into a reviewed directory: use a new directory. The
comparison script refuses to overwrite sheets with nonblank labels/reasons.

Build the Word report with the bundled document runtime:

```sh
"$CODEX_PRIMARY_RUNTIME_PYTHON" build_report.py
"$CODEX_PRIMARY_RUNTIME_PYTHON" /opt/codex/skills/builtins/documents/render_docx.py results/person_c_keyword_validation.docx --output_dir /tmp/person-c-report-qa
```

Render and inspect all pages before delivery. The optional report builder uses
python-docx from the bundled runtime; it is not needed for analysis.
