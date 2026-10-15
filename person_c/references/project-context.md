# SOEN 6221 Person C context

## Repositories

Analyze frameworks, not applications or agent-authored pull requests. Use Python source only, retaining tests. Obtain pilot commit SHAs; none are provided here.

| Framework | GitHub repository |
|---|---|
| LlamaIndex | run-llama/llama_index |
| LangChain | langchain-ai/langchain |
| AutoGen | microsoft/autogen |
| OpenAI Agents SDK | openai/openai-agents-python |
| LangGraph | langchain-ai/langgraph |
| MetaGPT | FoundationAgents/MetaGPT |
| Semantic Kernel | microsoft/semantic-kernel |
| CrewAI | crewAIInc/crewAI |
| Haystack | deepset-ai/haystack |
| smolagents | huggingface/smolagents |

## Reported pilot values

Treat these as team-reported baseline values, not verified findings:
- 62,905 comment blocks; 640 strict candidates; 1,206 loose-only; 1,846 full-pool candidates.
- Full-pool counts: LlamaIndex 459, LangChain 403, AutoGen 207, OpenAI Agents SDK 182, LangGraph 144, MetaGPT 121, Semantic Kernel 110, CrewAI 98, Haystack 71, smolagents 51.
- Earlier strict comparison: LangChain 975/89/77; AutoGen 114/100/87; CrewAI 30/17/12, respectively strict + DEPRECATED / strict without it / anchored strict. Verify compatible snapshots and extraction before comparing.
- Team preference is sampling the full pool. Person B’s document also retains provisional wording; flag the inconsistency rather than silently resolving it.
- 600 candidates is the later taxonomy study target, separate from Person C’s 100-candidate detector evaluation.
- Person B proposes four people labelling the same 30 taxonomy examples and Fleiss’ kappa. This differs from Person C’s binary SATD validation and two-person Cohen’s kappa.

## Source provenance

Use original texts and exact locations; do not imply these sources validate our Python agentic detector.

1. Potdar and Shihab (2014), An Exploratory Study on Self-Admitted Technical Debt, ICSME. DOI 10.1109/ICSME.2014.31. The team asks to start from its 62-pattern set. Obtain the actual published dictionary/replication artifact and compare it with the pilot. Do not reconstruct the list from memory.
2. Guo et al. (2019), MAT: A simple yet strong baseline for identifying self-admitted technical debt, arXiv:1910.13238. https://arxiv.org/abs/1910.13238 — abstract explicitly names TODO, FIXME, XXX and HACK. MAT uses fuzzy matching; our exact whole-word rules are an adaptation.
3. Vidoni (2021), Self-Admitted Technical Debt in R Packages: An Exploratory Study, MSR pp. 179–189. DOI 10.1109/MSR52588.2021.00030. https://melvidoni.rbind.io/publication/2021-rsatd-msr.pdf — Section IV-C, printed p. 185 lists workaround/work around/work-around, hard coded variants, temporary solution, kludge and ugly. Quick fix and failure phrases appear in an additional list explicitly requiring further validation. These are R results.
4. Watts and Debts of Agentic Frameworks, arXiv:2606.10702v1, is a registered report; do not report planned work as completed empirical findings.
5. Bhatia et al., arXiv:2311.12019, and Selvanayagam et al., arXiv:2601.06266v1, use trained classifiers. Verify revisions and evaluation details before citing benchmark values.

The previously drafted N01–N10 dictionary is a proposal, not necessarily the pilot’s loose set or Potdar–Shihab’s canonical dictionary. Broad phrases such as missing validation, needs refactoring, brittle and magic number require explicit provenance or a proposed-pattern label. DEPRECATED remains an empirical diagnostic comparison, not inherently SATD.
