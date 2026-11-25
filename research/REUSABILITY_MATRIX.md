# Reusability matrix

| Idea | Source | Use | License barrier |
| --- | --- | --- | --- |
| Localize then patch then test | Agentless | Our control flow | Paper is public; we did not copy their code |
| Keep a short memory of failed edits | Reflexion | Fingerprints in `/tmp/hegemon/state.json` | No code copied |
| Refuse unmeasured prompt promotions | GEPA, simplified | `promote()` | No GEPA code vendored |
| Graph neighbor lookup | Competition harness | Prompt tells the model to call it once when confidence is low | Harness-provided |
| Skill script for test summaries | Competition skill mechanism | `summarize_pytest.py` | Original |
| Competitor prompts or dummy adapters | Public GitHub repos | Not used | Not audited as reusable, so excluded |
| SWE-bench dumps, issue-to-patch maps | Public datasets | Not downloaded | Would be a contamination risk even if the license allowed training |

Original code in this repository is under Apache-2.0. See `research/LICENSE_AUDIT.md`.
