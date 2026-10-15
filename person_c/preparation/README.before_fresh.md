# Person C: pilot reproduction pending

The supplied skill and context define the task, but contain no executable pilot,
exact detector dictionary, comment corpus, or pinned commit SHAs. The selected
GitHub repository has no commits or files. These tools are preparatory work;
no framework analysis or human validation has been completed.

## Inputs required before reproducing the pilot

Supply the pilot script (including version/dependencies), exact strict and
loose-only pattern configuration with regex flags and provenance, extracted
comment corpus, extraction rules, and ten pinned commit SHAs. If extraction
must be repeated, the corresponding source snapshots are also needed.
Specify treatment of docstrings, consecutive comment lines, tests, exclusions,
normalization, case sensitivity, word boundaries and standalone DEPRECATED.
The skill warns that the pilot strict set may contain more than four markers.
No canonical 62-pattern dictionary has been supplied or reconstructed.

The corpus adapter must preserve raw text, distinct source locations, stable
comment IDs, commit SHA, matching copy, source URL and code context. The script
expects UTF-8 JSONL with those fields; see `satd_compare.py` for field names.
Confirm that its extraction and matching rules match the pilot before declaring
reproduction. A newly pinned run requires explicit user authorization and must
be described as an independent analysis.

## Prepared tools and tables

- `satd_compare.py`: standard-library-only extraction, four comparisons,
  match records/spans, per-framework/total counts and density, seeded sampling.
- `test_satd_compare.py`: eight passing tests, entirely synthetic. Its fixture
  patterns and counts are not pilot patterns or empirical findings.
- `patterns.pending.json`: deliberately empty and rejected by the executable.
  Replace only after establishing the actual pilot definitions.
- `sensitivity.pending.csv`: table structure for ten frameworks plus total;
  all measurement cells remain blank and status is pending.
- `pilot_reported_counts.csv`: values transcribed from the supplied context,
  explicitly unverified. They are not computed results.
- `reviewer_template.csv`: header only, not a 100-comment sample.
- `preparation_manifest.json`: input hashes, scope, seed and completion status.

## Run after inputs arrive

Use the existing checkout; no additional Git worktree is needed.
Working directory: `/workspace/soen6221_repo/person_c`.

```sh
python -m unittest -v test_satd_compare.py
python satd_compare.py compare --corpus INPUT_COMMENTS.jsonl --config VERIFIED_PATTERNS.json --out results
```

Optional extraction, only if compatible with the pilot:

```sh
python satd_compare.py extract --manifest VERIFIED_SNAPSHOTS.json --out extracted
```

The extraction manifest must specify `docstrings: "exclude"`,
`excluded_directory_names`, and `repositories` with `framework`, `repository`
(owner/name), `checkout` and exact 40-character `commit`. This extractor uses
tracked Python files only, retains tests, excludes docstrings, uses tokenize,
and merges adjacent standalone # lines only at equal indentation without
crossing blank lines or code. List actual vendor/environment/cache exclusions;
do not blanket-exclude source packages called build or dist. Tokenization
failures are logged and prevent publication of an incomplete corpus.

Every pattern needs `id`, `group` (strict, loose_only or deprecated), `kind`
(marker or phrase), exact `regex`, explicit boolean `case_sensitive`, `source`
and `reason`. Separate standalone DEPRECATED into its diagnostic group;
do not bundle it inside strict/loose regexes. Adopted/adapted/proposed provenance
belongs in `source`. No pattern or regex flags are inferred.

The anchored variant changes only strict marker detection: match at the start
of a matching comment after delimiter/leading-whitespace removal. Configure
`anchoring` as `first_line` or `every_line` and report that choice. Strict phrase
patterns remain unchanged. Regex word boundaries are independent of anchoring.
The input matching copy must be audited against the pilot normalization.

Sensitivity rows use all extracted blocks as the denominator. Added/removed
counts compare with unanchored strict without DEPRECATED. The strict/full
candidate ratio is coverage, not SATD recall. All match records are retained.

## Human review

Sampling uses seed 6221 with disjoint unanchored strict-without-DEPRECATED and
full-set loose-only pools: 50 each, redistributing shortage to the other pool.
If the entire candidate pool has fewer than 100 blocks, all are selected and
the actual N is reported. `sampling_admin.csv` retains group, population size,
sample size and inclusion probability; keep it separate from reviewer sheets.
`reviewer_1.csv` hides groups and leaves labels/reasons blank.
`reviewer_2_overlap.csv` contains a random 30-comment overlap (or actual smaller
N), independently labelled by a second human before adjudication.

Labels: SATD / non-SATD / uncertain. SATD requires a developer acknowledgement
of an existing compromise, deficiency, shortcut or deferred corrective work.
Use source context to distinguish documentation, resolved issues, optional
enhancements, quoted markers, negations and routine deprecation. Do not erase
pre-adjudication labels. Codex-generated suggestions are not human labels.

After labels arrive, compute group precision, unresolved counts and bounds,
Wilson intervals for resolved proportions, population-weighted overall
precision, and raw agreement/Cohen's kappa on independent binary overlap
labels. Record uncertain handling and paired N; kappa is undefined if expected
agreement is 1. These statistics and the final referenced Word report remain
pending. No final detector selection can be justified from synthetic tests.

## Team issues to resolve

The context reports 62,905 blocks, 640 strict, 1,206 loose-only and 1,846 full
candidates. Per-framework full counts sum to 1,846, an arithmetic consistency
check only. Earlier strict comparisons use unspecified snapshots/extraction
and cannot yet be compared. The full-pool sampling preference conflicts with
Person B's provisional wording. Person C's 100-candidate binary validation and
two-person Cohen's kappa are distinct from the later 600-candidate taxonomy
study and four-reviewer Fleiss' kappa. Flag any validated detector changes to
Person B's pool; no teammate messages have been sent.

Paper titles/claims in the supplied context are provenance leads, not verified
source findings. Original papers and exact dictionary locations still require
verification before the final keyword table/report. Precision >60% and kappa
>0.7 are team targets, not general validity thresholds. Absolute recall is
not estimated by reviewing flagged comments alone.
