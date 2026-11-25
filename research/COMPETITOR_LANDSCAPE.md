# Competitor landscape

Read 2026-11-25. None of these repositories were treated as a leaderboard leader. No code was copied. Reported scores were not re-run.

| Repository | What was inspected | Takeaway | Compliance note |
| --- | --- | --- | --- |
| https://github.com/happyc0der/gemma-swe-agent `docs/competition.md` | Harness digest | Context grows; keep tool outputs small; scratch must stay out of the worktree; starter budget of 1 minute is too small to be a serious agent | Their reimplementation is theirs. We used the digest as a secondary source only. |
| https://github.com/Peoplerepabulic/kaggle-gemma4-developer-agent `docs/competition-facts.md` | Fact table dated 2026-10-22 | Four QAT model ids, 3 GiB zip, 12-hour cap, small-model bonus | Facts, not code. |
| https://github.com/ennydev-2026/gemma-4-developer-agent | `agent.yaml`, `eval_config.yaml`, `sampling.yaml` | Tool names declared as a YAML list. Their eval keys differ from happyc0der. Their 45-minute task cap would not fit 120 serial tasks. | Not copied. We did not adopt their timeout. |
| https://github.com/nicknnamsa/gemma4-swe-agent | Search snippet of `submission/agent.yaml` | Same tool list, 31B default, sub-agent commented out | Not copied. |
| https://www.researchforgehq.com/kaggle/gemma-4-developer-agent | Narrative | Claims a public leader of 0.29 on 2026-11-15 and a 0.05 swing on a byte-identical resubmit (0.12 then 0.17). Unverified. | Do not tune to one public score. |
| https://github.com/johnsonhk88/kaggle-Google-The-Gemma-4-Developer-Agent-Competition | Not fetched this session | No claim | |
| https://github.com/MadeNavaneeth/Gemma-4-Developer-Agent-Kaggle | Not fetched this session | No claim | |
| https://github.com/8kta/kaggle-gemma4 | Not fetched this session | No claim | |

Reusable idea we did adopt as our own design: a deterministic localizer and a diff check, so the model spends generations on the edit rather than on search.

Not adopted: dummy LoRA files, a 45-minute per-task timeout, and any prompt text from those repos.
