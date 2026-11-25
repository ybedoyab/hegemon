# Compliance matrix

Date: 2026-11-25. `VERIFIED_HARNESS` means the claim is in the downloaded `HARNESS_README.md`. `VERIFIED_PAGE` means it was visible in the signed-in Kaggle session. `UNKNOWN` is not shipped as if it were confirmed.

| Item | Status | Evidence | In this submission |
| --- | --- | --- | --- |
| Rules accepted for this account | VERIFIED_PAGE | Rules tab banner, 2026-11-25 | n/a |
| `agent.yaml` at zip root, bare tool names, `!include` | VERIFIED_HARNESS | Official sample `agent.yaml` | yes |
| Skills attached with `skills:` directory list | VERIFIED_HARNESS | Harness skills section and sample shape | V7A omits `skills:`. Directory `skills/hegemon-repair` is not loaded. |
| Zip unpacked size < 3 GiB, no symlinks, no `..` | VERIFIED_HARNESS | `build_submission_limits` | packer enforces size class and paths |
| Model `gemma-4-31b-it-qat-w4a16-ct` | VERIFIED_HARNESS | Allowed model list | selected |
| 12B, E4B, E2B QAT checkpoints allowed | VERIFIED_HARNESS | Same list | not selected |
| Nine harness tools and their arguments | VERIFIED_HARNESS | Tools reference | declared by name |
| Skill args `skill_name` and `file_path` | VERIFIED_HARNESS | Skill coercion note | prompt uses those names |
| `evaluation:` keys for budgets | VERIFIED_HARNESS | Section 7.1 and sample `eval_config.yaml` | yes |
| `thinking_level` omitted for vLLM | VERIFIED_HARNESS | Sampling note | omitted |
| Sandbox network off | VERIFIED_HARNESS | `network_mode=none` | scripts do not open sockets |
| 4x L4, context 32768 | VERIFIED_HARNESS | Serving section | not runnable on the local 4 GB GPU |
| Score is the percentage of issues whose patch passes validation tests | VERIFIED_PAGE | Evaluation page, retrieved with the Kaggle API on 2026-11-25 | no score claimed |
| 12-hour total budget | UNKNOWN | Not in the rules pages read on 2026-11-25 | 5 minute per-task cap is a hypothesis |
| One submission per day | VERIFIED_PAGE | Competition-specific rules section 2.2.a, retrieved 2026-11-25 | the agent does not call the submit API |
| Private sharing of competition code outside the team | VERIFIED_PAGE | Foundational rules section 5.d and 6.a, retrieved 2026-11-25 | not done |
| Public sharing of competition code | VERIFIED_PAGE | Foundational rules section 6.b: public sharing must be on the competition forum or notebooks, and is treated as an OSI license that allows commercial use | The GitHub repo is public by the user's choice. Visibility was not changed. No further agent implementation will be pushed while it stays public. Competition data is not in git. |
| Competition data must not be given to non-participants | VERIFIED_PAGE | Competition-specific rules section 2.4.b.1, retrieved 2026-11-25 | `tasks.jsonl` and snapshots stay outside git |
| Development `tasks.jsonl` has 129 lines and includes reference patches | VERIFIED_FILE | Line count only. Patch text was not copied into the repo. | absent from git |
| Cross-task memory during scoring | disabled by policy | No official allowance found | disabled |
| Online weight updates | disabled by policy | No official allowance found | disabled |
| Automatic Kaggle submission | VERIFIED_PROHIBITED | User contract | not implemented |
| Official baseline solve rate | MEASURED on one task at the sample's own 1-minute cap: 0/1 | Notebook version 2 | A matched 5-minute run is in notebook version 7, still running |
| Skill scripts share the container filesystem with `run_command` | VERIFIED_PAGE | "Model Selection, Budget, and Harness Rules" page, retrieved 2026-11-25. The page also says skill time counts against the central budget | Version 5 still ranked the skill directory. V7A does not attach the skill |
