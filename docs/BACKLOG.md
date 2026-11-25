# Backlog

Ordered by expected effect on a real solve rate.

1. **BLOCKED — Accept Kaggle rules and download the dataset.** Need `HARNESS_README.md`, `sample_submission/`, and `tasks.jsonl`. Deadline to enter: 2026-11-25 23:59 UTC. The user must do the acceptance. Do not paste the API token into chat.
2. Re-read `eval_config.yaml` keys against `HARNESS_README.md` and fix or delete the file.
3. Run the official starter on a handful of development tasks. Record B0. Status today: `NOT_RUN`.
4. Run this submission through the same harness on the same tasks. Record B2. Do not compare against a different sample.
5. If localization is the dominant failure, extend the skill with graph-tool hints using the real graph JSON. Do not guess node ids.
6. If repairs are wrong while files are right, change the edit section of the prompt and re-measure.
7. If the right patch is produced and not selected, change `diff_guard` and the verifier rubric.
8. If timeouts dominate, lower `max_output_tokens` further or shorten the prompt, then re-measure.
9. Small-model package (`gemma-4-e2b-it-qat-w4a16-ct` or `e4b`) only after the 31B package runs. It is a second final submission, not a replacement, and only if the official model list confirms eligibility.
10. LoRA only after a real training run on permitted data. Do not add dummy weights.

## Done in this iteration

- Environment discovery
- Private-repo check
- Skill scripts, prompt, packager, unit tests, synthetic localization probe
