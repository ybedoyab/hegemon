# Compliance matrix

Date: 2026-11-25. `VERIFIED_HARNESS` means the claim is in the downloaded `HARNESS_README.md`. `VERIFIED_PAGE` means it was visible in the signed-in Kaggle session. `UNKNOWN` is not shipped as if it were confirmed.

| Item | Status | Evidence | In this submission |
| --- | --- | --- | --- |
| Rules accepted for this account | VERIFIED_PAGE | Rules tab banner, 2026-11-25 | n/a |
| `agent.yaml` at zip root, bare tool names, `!include` | VERIFIED_HARNESS | Official sample `agent.yaml` | yes |
| Skills attached with `skills:` directory list | VERIFIED_HARNESS | Harness skills section and sample shape | `skills/hegemon_repair` |
| Zip unpacked size < 3 GiB, no symlinks, no `..` | VERIFIED_HARNESS | `build_submission_limits` | packer enforces size class and paths |
| Model `gemma-4-31b-it-qat-w4a16-ct` | VERIFIED_HARNESS | Allowed model list | selected |
| 12B, E4B, E2B QAT checkpoints allowed | VERIFIED_HARNESS | Same list | not selected |
| Nine harness tools and their arguments | VERIFIED_HARNESS | Tools reference | declared by name |
| Skill args `skill_name` and `file_path` | VERIFIED_HARNESS | Skill coercion note | prompt uses those names |
| `evaluation:` keys for budgets | VERIFIED_HARNESS | Section 7.1 and sample `eval_config.yaml` | yes |
| `thinking_level` omitted for vLLM | VERIFIED_HARNESS | Sampling note | omitted |
| Sandbox network off | VERIFIED_HARNESS | `network_mode=none` | scripts do not open sockets |
| 4x L4, context 32768 | VERIFIED_HARNESS | Serving section | not runnable on the local 4 GB GPU |
| Score is fraction of tasks whose hidden tests pass | UNKNOWN | Harness describes pytest verification. The public formula was not copied from the rules body in this pass. | no score claimed |
| 12-hour total budget | UNKNOWN | Not in the harness file read today | 5 minute per-task cap is a hypothesis |
| One submission per day | UNKNOWN | Not re-read from the rules body | we do not submit |
| Private sharing outside the team prohibited | UNKNOWN | Not re-read from the rules body | repo stays private |
| Development `tasks.jsonl` has 129 lines and includes reference patches | VERIFIED_FILE | Line count only. Patch text was not copied into the repo. | absent from git |
| Cross-task memory during scoring | disabled by policy | No official allowance found | disabled |
| Online weight updates | disabled by policy | No official allowance found | disabled |
| Automatic Kaggle submission | VERIFIED_PROHIBITED | User contract | not implemented |
| Official baseline solve rate | NOT_RUN | No Gemma generation yet | `NOT_RUN` |
