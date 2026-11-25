# Compliance matrix

Date: 2026-11-25. `VERIFIED_*` means this workspace opened the official artifact. That did not happen for Kaggle HTML or the dataset. Items we ship are working assumptions, labeled `UNKNOWN` with the source that motivated them.

| Item | Status | Evidence | In this submission |
| --- | --- | --- | --- |
| Score is fraction of tasks whose patch passes hidden tests | UNKNOWN | ReconScribe, ResearchForge, happyc0der digest | n/a |
| `agent.yaml` at zip root | UNKNOWN | Same sources, consistent | yes |
| Zip <= 3 GiB, no symlinks, no `..` | UNKNOWN | Same | packer enforces |
| Model `gemma-4-31b-it-qat-w4a16-ct` allowed | UNKNOWN | All secondary sources | yes, default |
| 12B / E4B / E2B allowed | UNKNOWN | Oct/Nov sources; Sept digest disagrees | not selected |
| Small-model bonus for E2B or E4B | UNKNOWN | ReconScribe, Peoplerepabulic facts | not built |
| Tools `run_command`, `read_file`, `edit_file`, `write_file`, `get_status`, `submit_patch`, graph tools | UNKNOWN | Harness digests | declared |
| `run_skill_script` / `load_skill` argument schema | UNKNOWN | Upstream ADK source, may differ from the harness | declared |
| Skill scripts may use only the sandbox | UNKNOWN | Arubad notes, ADK skill runner | stdlib scripts |
| 12-hour total budget | UNKNOWN | Multiple secondary sources | `eval_config.yaml` hypothesis |
| Internet disabled at score time | UNKNOWN | Secondary sources | scripts do not open sockets |
| One submission per day | UNKNOWN | Secondary sources | we do not submit |
| Private sharing outside the team prohibited | UNKNOWN | Secondary sources | repo is private |
| Competition data redistribution prohibited | UNKNOWN | Secondary sources | dataset not in git |
| Reference patches hidden from the solver | VERIFIED_REQUIRED by project policy | User contract and SWE-bench practice | enforced by absence of data |
| Cross-task memory | UNKNOWN as a platform fact; VERIFIED_PROHIBITED by our policy until an official allowance | User contract | disabled |
| Online weight updates during scoring | VERIFIED_PROHIBITED by our policy | User contract; no official allowance on file | disabled |
| Proprietary-API distillation | UNKNOWN | ReconScribe, open as of 2026-10-17 | not done |
| Submitting to Kaggle from this agent | VERIFIED_PROHIBITED | User contract | not implemented |
| Dummy LoRA weights | VERIFIED_PROHIBITED by our policy | A fake adapter would be a false claim | absent |
| Official baseline solve rate | BLOCKED | No dataset, no model, no running Docker daemon | `NOT_RUN` |
