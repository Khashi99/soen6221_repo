---
name: satd-keyword-validation
description: Complete SOEN 6221 Person C SATD keyword selection and validation for ten Python agentic frameworks. Use to inspect a pilot detector, compare strict and loose patterns, generate sensitivity tables, prepare manual review samples, calculate precision and reviewer agreement, and produce a concise referenced Word report.
---

# SATD keyword validation

Complete the Person C deliverable: decide which comment patterns flag SATD candidates and justify the choice with measured counts and manual validation. Read [project context](references/project-context.md) before starting.

## Establish inputs

1. Inspect the supplied pilot script, pattern files, extracted comments, repository manifest and existing reports. Use rg for file discovery. Preserve originals.
2. Record the exact strict and loose definitions, extraction rules, pattern provenance, and pinned commits. Do not assume “strict” means only four markers; establish what the pilot actually used.
3. Reuse pilot inputs and snapshots. If unavailable, request the script, exact patterns, corpus and commit SHAs in one concise question. Continue independent work: source verification, implementation scaffolding and review templates. Do not invent the 62 Potdar–Shihab patterns or attribute a newly assembled dictionary to the pilot.
4. If the user authorizes a fresh independent run without the pilot, pin and record new commits and explicitly distinguish new results from pilot reproduction. Do not silently substitute current HEAD.
5. Keep a run manifest with seed 6221, detector version, configuration hash, input hash, Python version, scope and exclusions.

## Extract and compare

Prefer the existing extraction script. If implementing extraction, use Python tokenize for actual # comments, include inline comments and tests, and merge adjacent standalone comment lines at the same indentation without crossing blank lines or code. Document docstring inclusion/exclusion; match the pilot scope for reproduction. Log tokenization failures rather than silently skipping files. Exclude vendored dependencies, environments, caches and build artifacts consistently; avoid blanket exclusions of source packages named build or dist.

Preserve raw text, normalize only a separate matching copy, and record repository, commit SHA, file path, line range, stable comment ID, pattern IDs and matched spans. Count each block once per variant. Keep repeated text at different locations as distinct records.

Implement a versioned, configurable comparison script and run these variants on one corpus:
- Pilot strict plus DEPRECATED.
- Pilot strict without DEPRECATED.
- Pilot strict without DEPRECATED with its marker detection anchored at the start of the comment after removal of comment delimiters and leading whitespace. Document treatment of consecutive comment lines.
- Pilot full set: strict plus loose-only patterns, without standalone DEPRECATED.
- Optional revised patterns, kept separate from the baseline.

Treat anchoring and whole-word boundaries as separate experimental choices. Examine write_todos, todo_list, quoted markers, negations, optional feature requests, expected test failures and routine deprecation documentation. An identifier mentioning a todo tool is not automatically debt. Do not discard a genuine debt admission just because it mentions that tool.

Generate per-framework and total candidate counts, added/removed counts, and candidate density using one consistent denominator. Save all match records to CSV or JSONL. Investigate mismatches against pilot numbers; never force counts to match.

Test the script with constructed comments covering inline and multiline extraction, strings containing #, multiple matches, identifier collisions, negation and all variant definitions. Mark fixtures as synthetic.

## Manual validation

Define SATD as a developer acknowledgement of an existing compromise, deficiency, shortcut or deferred corrective work. Do not infer an admission from imperfect code alone. Label ordinary documentation, resolved issues and optional enhancements as non-SATD when context supports this. Retain uncertain cases.

Randomly sample 100 candidates without replacement for initial validation. By default select 50 strict and 50 loose-only, uniformly within each disjoint pool, to estimate both groups. If a pool is smaller, review it entirely and allocate remaining places to the other pool. Record sampling probabilities and framework coverage; do not claim per-framework precision from inadequate samples.

Export a reviewer sheet with comment ID, raw text, code context/link and blank SATD/non-SATD/uncertain and reason fields. Keep detector group and proposed labels hidden from reviewers where practical. Have a human second reviewer independently label a randomly selected 30-comment overlap before adjudication. LLM or Codex suggestions may assist calibration but must not be reported as human ground truth or an independent human reviewer.

Compute:
- Group precision after labels are resolved: confirmed SATD / reviewed.
- Unresolved uncertainty counts and confirmed-fraction bounds if uncertainty remains.
- Wilson 95% intervals for resolved group proportions.
- Overall precision weighted by strict and loose-only population sizes, not a simple average of equally sized samples.
- Raw agreement and Cohen’s kappa from independent binary labels on the overlap; report uncertain handling and actual paired N. If expected agreement is 1, report kappa undefined. Preserve pre-adjudication labels.

Treat precision above 60% and kappa above 0.7 as team targets, not universal validity thresholds. Do not tune repeatedly until a target is passed. After changing patterns from calibration, evaluate a fresh held-out sample and distinguish calibration from validation.

## Coverage and limitations

Report strict candidate coverage = strict count / full candidate count when sets are nested. Do not call this SATD recall: candidates include false positives. Compute relative recall only against a clearly defined, manually confirmed wider-set reference, with appropriate sampling weights. Do not estimate absolute recall from flagged comments alone.

Optionally search unflagged comments with an LLM and manually confirm suggested misses to discover new phrase classes. Label this targeted exploration, not a random recall estimate. Report absolute recall as not estimated unless a suitable labelled matched/unmatched evaluation is actually completed.

Verify benchmark figures from original papers before using them. Do not equate F1 with precision or claim superiority across different datasets. Do not claim no prior study reports sensitivity analysis without a documented literature search.

## Finalize deliverables

Produce:
1. Final exact pattern configuration, with one-line inclusion/exclusion reasons and source locations distinguishing adopted, adapted and proposed patterns.
2. Sensitivity CSV/table across all ten frameworks and variants.
3. Review sample and retained independent labels, precision statistics and kappa.
4. Reproducibility manifest and executable scripts.
5. A straightforward Word document: referenced keyword table, sensitivity table, short validation summary and one brief limitations paragraph. Avoid heavy prose and repeated “I” phrasing. Use the documents skill and render/inspect the DOCX if available.

Keep results pending until measured. Freeze the set after validation and flag any resulting change to Person B’s sampling pool. Do not send messages to teammates without explicit authorization. Save outputs in the user’s chosen project; in Work Mode follow available artifact persistence instructions.

State exactly what is completed and what needs human input. If manual labels are missing, finish the automated deliverables and review sheet, then explain that human validation remains outstanding.
