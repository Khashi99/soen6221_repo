---
name: soen6221-person-c-continuation
description: Continue the SOEN 6221 Person C SATD keyword study in Khashi99/soen6221_repo. Use to explain or revise keyword sensitivity results, review sampled comments with source context, complete human validation statistics, and update the concise Word report while preserving pinned snapshots and distinguishing AI judgments from human labels.
---

# SOEN 6221 Person C continuation

## Purpose and user preferences

Continue the existing SATD keyword study. Inspect the current repository before
starting new work. Complete the user's current request rather than restarting
the analysis. The user prefers a concise keyword list, one sensitivity table,
and a short explanation in a single Word document. Avoid extra reports,
archives, templates or repeated confirmation questions unless they are needed.
Explain results in plain language. Supply a single paragraph when requested.

This file is a self-contained handoff for a new Codex session. Attach it and
ask: "Use this skill to continue my SOEN 6221 Person C project. Inspect the
repository and current report, then [describe the next task]." It may also be
installed as `.agents/skills/soen6221-person-c-continuation/SKILL.md` in a
checkout when the user wants a repository-local Codex skill. It does not
require the old chat, uploaded icon, or openai.yaml to explain project state.

## Locate and preserve the project

- GitHub: https://github.com/Khashi99/soen6221_repo, branch `main`.
- Prior cloud checkout: `/workspace/soen6221_repo`; actual paths may differ in
  a new session. Locate the existing checkout first. If missing, clone the
  repository using existing Git authentication. Do not request a token merely
  because GH_TOKEN is unset. Never print credentials.
- Use the existing checkout. Each cloud task is isolated; do not create an
  additional Git worktree unless requested.
- Read applicable AGENTS.md instructions and run `git status --short` before
  editing. Preserve user changes, human labels, source inputs and historical
  outputs. Do not reset branches, force-push, or silently substitute new HEADs.
- This handoff records work completed before it was written. The GitHub files
  and current user instructions take precedence if the project has advanced.

## Essential project files

| Path relative to repository root | Purpose |
|---|---|
| `SATD_keywords_and_sensitivity.docx` | Current user-facing report, two pages at handoff: exact keyword families, sensitivity table, explanation, and AI-assisted review of two repositories |
| `AI_review_LangChain_LlamaIndex.csv` | 57 AI judgments with reasons, comment IDs, reviewed context, pinned links and separate blank human fields |
| `person_c/patterns.independent.json` | Exact regexes, flags, groups, reasons and provenance; authoritative detector configuration |
| `person_c/results/sensitivity.csv` | Measured per-framework and total counts, added/removed counts and density |
| `person_c/snapshots.json` | Ten exact source commits, cache paths and extraction exclusions |
| `person_c/results/run_manifest.json` | Detector/input/config hashes, seed, scope, designated overlap IDs, reproducibility evidence |
| `person_c/results/matches.jsonl` | Every matched comment/variant with pattern IDs and spans |
| `person_c/results/reviewer_1.csv` | Original 100-comment sample, human labels/reasons still blank at handoff |
| `person_c/results/reviewer_2_overlap.csv` | Designated random 30-comment overlap for a second independent human |
| `person_c/results/adjudication.csv` | Separate final human decisions, blank at handoff |
| `person_c/results/sampling_admin.csv` | Hidden detector groups and sampling probabilities; keep apart from blinded reviewers |
| `person_c/results/sample_framework_coverage.csv` | Framework/group representation in the sample |
| `person_c/results/edge_case_audit.csv` | 23 targeted diagnostics, separate from random validation |
| `person_c/results/review_statistics.json` | Pending human statistics, not the later AI-review totals |
| `person_c/reviewer_instructions.md` | Human labeling rubric and independence instructions |
| `person_c/satd_compare.py` | Extraction and four-variant comparison CLI, detector version 0.2.0 |
| `person_c/acquire_snapshots.py` | Restore or verify pinned source caches |
| `person_c/review_statistics.py` | Statistics from retained human sheets and adjudication |
| `person_c/source_provenance.json` | Original-paper access status and proposed/adapted provenance |
| `person_c/references/` | Exact original supplied context and original SATD skill |
| `person_c/preparation/` | Historical pending templates and unverified pilot counts; not current measured results |
| `person_c_deliverables.zip` | Earlier complete analysis package, including the raw comment corpus |

**Version distinction:** the ZIP predates the root concise Word report, the
57-comment AI-review CSV, and this handoff. It is useful for corpus recovery,
but is not the latest complete project. Its internal
`person_c/results/person_c_keyword_validation.docx` is an older, longer
technical report. `person_c/build_report.py` builds that older report; do not
use it to replace the current root Word document. The three-page render status
in the original run manifest refers to that older technical report, not the
current two-page document.

## Study identity and extraction

The pilot script, exact pilot dictionary, corpus and commit SHAs were
unavailable. The user explicitly authorized a **fresh independent study**.
Do not call the results pilot reproduction. Do not invent or claim to use the
Potdar-Shihab canonical 62-pattern dictionary.

Analyze framework repositories, not outside applications or agent-authored
pull requests. Scope is all tracked Python `.py` files in the ten snapshots,
including tests and Python examples. Python tokenize extracts actual # comment
tokens. Exclude docstrings and # inside ordinary strings. Merge consecutive
standalone comment lines only at identical indentation, without crossing
blank lines or code. Inline comments stay separate. Preserve raw tokens;
for matching, remove the first # and leading whitespace on each constituent
line, then join the lines with newline. Regex flags ignore case.

Repeated text at distinct locations remains distinct. Comment IDs incorporate
repository, commit, path and line range. Count a block only once per variant,
even if multiple patterns match. Store all spans in the matching-copy coordinate
system. Use all extracted blocks as the consistent density denominator.

The extraction exclusions are listed in snapshots.json. Do not blanket-exclude
source packages called build or dist. At the recorded snapshots, all 12,653
tracked Python files were eligible and none matched excluded directory names.
There were 66,754 blocks and zero tokenization failures. Log extraction failures;
do not silently publish an incomplete corpus.

## Exact keyword configuration

All regexes below use Python `re.IGNORECASE`. Word boundaries are part of the
regex and are separate from the experimental start-of-line anchoring.

| ID | Group | Exact Python regex |
|---|---|---|
| S01 | strict | `\bTODO\b` |
| S02 | strict | `\bFIXME\b` |
| S03 | strict | `\bXXX\b` |
| S04 | strict | `\bHACK\b` |
| P01 | loose_only | `\bwork(?:[ -]?around)\b` |
| P02 | loose_only | `\bhard[ -]?cod(?:e|ed|ing)\b` |
| P03 | loose_only | `\btemporary\s+solution\b` |
| P04 | loose_only | `\bkludge\b` |
| P05 | loose_only | `\bugly\b` |
| D01 | deprecated | `\bDEPRECATED\b` |

Strict markers are TODO, FIXME, XXX and HACK. Loose phrases cover workaround /
work around / work-around; hardcode / hardcoded / hardcoding and their spaced
or hyphenated variants; temporary solution; kludge; ugly. P03 permits whitespace
between its words, including a newline inside a merged block. P01/P02 permit
zero or one literal space or hyphen at the shown position, not arbitrary
whitespace. An underscore is a word character, so `todo_list`, `write_todos`
and `hardcoding_tool` do not match their corresponding standalone marker/term.

Standalone DEPRECATED is diagnostic only. Removing D01 does not remove a block
that also matches a retained strict/loose pattern. No negation, quotation,
identifier or expected-failure classifier was silently added to the baseline;
those cases require contextual review.

Strict marker names were adapted from the supplied context's MAT lead; these
exact regexes are this study's adaptation, not MAT fuzzy matching. Loose
patterns are proposals motivated by the supplied context's Vidoni lead. The
original papers were not yet verified. Quick fix, failure phrases, brittle,
magic number, missing validation and needs refactoring are not in this run.
Do not expand or tune the dictionary silently.

## Measured sensitivity results

Four variants, using the same corpus:

1. `strict_plus_deprecated`: S01-S04 plus D01, unanchored.
2. `strict_without_deprecated`: S01-S04, unanchored.
3. `anchored_strict_without_deprecated`: S01-S04 at the start of **each**
   constituent comment line after delimiter/whitespace removal.
4. `full_without_deprecated`: S01-S04 plus P01-P05, unanchored.

| Framework | Blocks | Strict plus D | Strict | Anchored strict | Strict plus loose |
|---|---:|---:|---:|---:|---:|
| LlamaIndex | 13345 | 313 | 256 | 244 | 263 |
| LangChain | 11602 | 967 | 89 | 84 | 109 |
| AutoGen | 6816 | 110 | 100 | 98 | 101 |
| OpenAI Agents SDK | 7700 | 13 | 13 | 12 | 15 |
| LangGraph | 6031 | 25 | 10 | 10 | 13 |
| MetaGPT | 2905 | 98 | 97 | 81 | 102 |
| Semantic Kernel | 7818 | 38 | 36 | 35 | 40 |
| CrewAI | 3926 | 24 | 17 | 13 | 26 |
| Haystack | 5238 | 3 | 3 | 2 | 4 |
| smolagents | 1373 | 22 | 20 | 18 | 20 |
| TOTAL | 66754 | 1613 | 641 | 597 | 693 |

Compared with unanchored strict: DEPRECATED adds 972 candidates (878 from
LangChain); anchoring removes 44; loose phrases add 52. Strict/full candidate
coverage is 641/693 = 92.50%. This is not SATD recall. Totals are measured
candidate counts, not human-confirmed debt counts. The unverified team's pilot
values (62,905 blocks, 640 strict, 1,206 loose-only, 1,846 full) must remain
separate; similar strict totals do not establish reproduction.

## Pinned source snapshots

Keep these exact commits for replay; source caches are research inputs, not
additional development projects. Do not replace them with latest default
branches without explicit authorization for a separate new study.

| Framework | GitHub repository | Commit |
|---|---|---|
| LlamaIndex | run-llama/llama_index | `5b7b6e323e1da3edd787a2104a89257c14f026d0` |
| LangChain | langchain-ai/langchain | `8ace87e7a6493d41d4c61bb41a637052367b27f3` |
| AutoGen | microsoft/autogen | `027ecf0a379bcc1d09956d46d12d44a3ad9cee14` |
| OpenAI Agents SDK | openai/openai-agents-python | `1c1a28df92f359dded4eed83976301c2f9850e89` |
| LangGraph | langchain-ai/langgraph | `a6731f436700c7d46a9224ccd3a0e0ce3a5bfdb5` |
| MetaGPT | FoundationAgents/MetaGPT | `11cdf466d042aece04fc6cfd13b28e1a70341b1f` |
| Semantic Kernel | microsoft/semantic-kernel | `5b4a3269a6803f7832568e66313c31d714a1f009` |
| CrewAI | crewAIInc/crewAI | `ba367461691278cf3b49afb68c785ca1935ff448` |
| Haystack | deepset-ai/haystack | `2b8e1d9f8360757dd50e8e4f71f83cb042f97238` |
| smolagents | huggingface/smolagents | `96f33faaf028479119ec8d34507b47694cf14e34` |

## Sampling and validation status

Seed 6221 selected 100 candidates without replacement from disjoint pools:
50/641 unanchored strict and 50/52 loose-only. Inclusion probabilities are
50/641 and 50/52. All ten frameworks are represented. These are stratified,
not 100 uniformly sampled full-pool candidates. Population weighting is
required for an overall precision estimate. Small framework subsamples do not
support reliable per-framework precision claims.

A designated random 30-comment overlap is saved for a second independent
human. Human sheets and adjudication were still blank at handoff. The user
asked Codex to review LangChain and LlamaIndex; Codex contextually reviewed
**only their 57 comments in the existing sample**, not their full 372-candidate
pool. Expanded source context was inspected for ambiguous cases. Decisions:

| Repository | Reviewed | AI SATD | AI non-SATD | AI uncertain |
|---|---:|---:|---:|---:|
| LangChain | 27 | 17 | 9 | 1 |
| LlamaIndex | 30 | 13 | 6 | 11 |
| Total | 57 | 30 | 15 | 12 |

The CSV uses ai_label and ai_reason; reviewer_type explicitly identifies
Codex. Preserve it separately from human labels. It has blank human_label and
human_reason fields but does not replace the designated independent human
workflow. Do not relabel these as a human manual review or two reviewers.

Examples: admitted temporary async wrappers and missing validation were AI
SATD; fake test responses and security allowlists were AI non-SATD; ambiguous
or possibly stale TODOs were uncertain. Identical text at different locations
was retained separately. These judgments are provisional, not ground truth.
Do not call 30/57 overall precision or compute human Cohen's kappa from them.

SATD means a developer acknowledgement of an existing compromise, deficiency,
shortcut or deferred corrective work. Imperfect code alone is insufficient.
Distinguish ordinary documentation, resolved workarounds, expected failures
for unsupported upstream APIs, optional enhancements and intentional design.
Retain uncertainty when the comment/context does not settle the distinction.
A genuine admission can mention a todo tool; do not suppress it merely for
mentioning that tool. Never force labels to meet a target.

## Next work and honest reporting

Follow the current user request, using this state to avoid repeated work.
Likely next steps:

1. Obtain actual human labels for the 100 comments and independent 30-comment
   overlap; preserve pre-adjudication labels and reviewer independence. The
   AI CSV may help separate calibration, but sharing its labels with blinded
   reviewers can influence their decisions.
2. Record adjudicated decisions separately. Compute group confirmed fractions,
   uncertainty counts/bounds, Wilson 95% intervals for resolved group
   proportions, and population-weighted overall precision. Disclose handling
   of uncertainty and missing labels. Wilson intervals on resolved cases can
   be biased if uncertainty is selective.
3. Compute raw agreement and Cohen's kappa only from actual independent binary
   human pairs; exclude/report uncertain pairs and report actual paired N.
   If expected agreement is 1, kappa is undefined. An AI or a second pass by
   the same AI is not an independent human reviewer.
4. Verify original sources before making canonical-dictionary, exact-page or
   benchmark claims. MAT: https://arxiv.org/abs/1910.13238. Vidoni 2021 DOI
   10.1109/MSR52588.2021.00030, source lead Section IV-C printed p.185:
   https://melvidoni.rbind.io/publication/2021-rsatd-msr.pdf. Earlier requests
   received HTTPS proxy 403 responses. Additions for arxiv.org and
   melvidoni.rbind.io were saved to the environment configuration draft, but
   runtime application was not established. Recheck actual access after a
   relevant state change; do not assume saving a draft applied it. User-supplied
   PDFs are another source-verification route. Never disable TLS verification.
5. Keep patterns provisional until validation. If calibration leads to changes,
   preserve the baseline and evaluate a new held-out sample. Do not repeatedly
   tune until team targets (precision >60%, kappa >0.7) pass; those are team
   goals, not universal validity thresholds.
6. Update the existing concise Word document with measured changes and a
   brief limitation paragraph. Do not create a new pile of deliverables.

Reviewing flagged comments alone does not estimate absolute recall. Strict
candidate coverage is not SATD recall. Relative recall requires a clearly
specified manually confirmed wider reference and appropriate sample weights.
Person B's sampling wording needs reconciliation before adopting the new
693-candidate pool. The later 600-comment taxonomy study and four-person
Fleiss' kappa are separate from Person C's 100-comment binary validation and
two-person Cohen's kappa. Do not send teammate messages without authorization.

## Replay commands and corpus recovery

The analysis scripts use Python's standard library. Start in `person_c/`
within the actual checkout:

```sh
python -m unittest -v test_satd_compare.py test_review_statistics.py
python acquire_snapshots.py
python satd_compare.py extract --manifest snapshots.json --out extracted_replay
python satd_compare.py compare --corpus extracted_replay/comments.jsonl --config patterns.independent.json --out results_replay
```

Original validation: 15 synthetic tests passed, including extraction, regex
boundaries, variants, sampling, preservation of human labels, Wilson intervals
and kappa edge cases. Corpus, sensitivity tables, matches and review samples
were byte-identical on replay. Recheck only what the current change requires.
Synthetic fixtures are not study data or human labels.

acquire_snapshots.py preserves pins when snapshots.json exists. Its default
cache is `/workspace/satd-source-cache`. For a different filesystem location,
inspect its path handling and prepare a separate local manifest with relocated
checkout paths; do not alter commit pins. Never reset an unexpected or modified
source checkout to force a match.

The raw `person_c/extracted/comments.jsonl` is intentionally Git-ignored. It is
inside `person_c_deliverables.zip`. Restore only that member to avoid overwriting
newer files. From the repository root:

```python
from pathlib import Path
import hashlib
import zipfile

root = Path.cwd()
target = root / "person_c/extracted/comments.jsonl"
with zipfile.ZipFile(root / "person_c_deliverables.zip") as archive:
    data = archive.read("person_c/extracted/comments.jsonl")
expected = "4bb7df1aa624641a09e2c7be55e80cc28e2d9647fac8b2057fa05ac16afa16e7"
assert hashlib.sha256(data).hexdigest() == expected
if target.exists():
    assert target.read_bytes() == data, "Preserve differing local corpus"
else:
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
```

For completed HUMAN sheets, from person_c/:

```sh
python review_statistics.py --directory results
```

This computes the original human workflow, not the root AI-review CSV. Inspect
its inputs before use. Keep pending statistics pending if labels are absent.
Never fill blank human fields with Codex judgments to make it run.

Always use a NEW comparison output directory for replay. The comparator refuses
nonblank review labels/reasons, but preservation requires care beyond that
check. Retain stable IDs and the designated overlap recorded in the manifest.

## Word editing and delivery

Edit `SATD_keywords_and_sensitivity.docx` in place while preserving the user's
concise layout. It currently has two pages: keywords/sensitivity and review
interpretation. It is the document the user expects. If an applicable document
skill is available, use its runtime and rendering instructions. Render and
inspect every page before delivery; text extraction alone does not prove layout.
In the previous environment, the bundled runtime/renderer were:

```sh
"$CODEX_PRIMARY_RUNTIME_PYTHON" /opt/codex/skills/builtins/documents/render_docx.py SATD_keywords_and_sensitivity.docx --output_dir /tmp/satd-report-qa
```

Do not assume these tools exist in a different environment; inspect available
capabilities. Keep QA renders and temporary builder scripts out of Git unless
requested. Do not overwrite the older reproducibility ZIP just to deliver a
new report, and do not claim that ZIP contains later root files.

The user could see sidebar files but could not download chat sandbox links,
even for a tiny text file. Do not repeat unsupported claims that permissions,
environment variables or the Internet domain list will fix file downloads.
The user explicitly requested GitHub publication in this conversation and
previous deliverables were pushed to `main`. In a new session follow its
current authorization and repository instructions for publication. If push is
authorized, add only intended changes, commit normally, push without force,
and verify success before claiming publication. Do not push unrelated work.
Prefer a GitHub download URL for this user, for example:

https://github.com/Khashi99/soen6221_repo/raw/refs/heads/main/SATD_keywords_and_sensitivity.docx

A successful local write or a saved environment configuration is not proof of
GitHub publication, a working download, or a new-task restore. State exactly
what was verified, what remains pending and the one next action needed.
