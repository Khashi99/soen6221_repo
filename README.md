# SOEN 6221 Person C deliverables

Fresh independent SATD keyword study across ten pinned Python framework repositories.
The pilot inputs were unavailable; these results do not reproduce the pilot.

- [Download the complete package](person_c_deliverables.zip) using GitHub's **Download raw file** button.
- [Word report](person_c/results/person_c_keyword_validation.docx)
- [Sensitivity table](person_c/results/sensitivity.csv)
- [100-comment reviewer sheet](person_c/results/reviewer_1.csv)
- [30-comment independent reviewer overlap](person_c/results/reviewer_2_overlap.csv)
- [Reviewer instructions](person_c/reviewer_instructions.md)
- [Method, results and reproduction instructions](person_c/README.md)

The ZIP includes the complete extracted corpus. The 64 MB uncompressed corpus
is omitted from Git to avoid duplicating it; extract the ZIP to restore it.
Original package checksums are in `person_c/checksums.sha256` and cover files
inside the package, including the corpus.

Measured totals from 66,754 comment blocks: 1,613 strict plus DEPRECATED,
641 strict without DEPRECATED, 597 anchored strict and 693 with proposed
loose phrases. Fifteen synthetic tests passed and replayed results matched.

Human labels, precision, Cohen's kappa and original-paper verification remain
pending. The proposed pattern configuration is fixed for initial validation,
not finalized as a validated detector.
