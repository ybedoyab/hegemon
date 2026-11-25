# Decisions

## D001 — Single agent plus skill scripts

- Rationale: the harness compiles YAML into one ADK agent. Extra sub-agents spend the same 12-hour budget on more generations.
- Evidence: public harness notes (happyc0der `docs/competition.md`, read here 2026-11-25) say context grows inside a task and tool outputs are capped. ReconScribe (checked by that author through 2026-11-10) describes a 12-hour cap for about 120 tasks.
- Expected benefit: a simple bug finishes in about six tool calls.
- Cost: no parallel hypotheses in one turn.
- Risk: Gemma may ignore `next_action`. Not measured.
- Validation: unit tests of the scripts. Official harness still `NOT_RUN`.
- Rollback: delete the skill from `agent.yaml` and keep the prompt-only edit loop.

## D002 — Scratch state outside the repository

- Rationale: public harness notes say `submit_patch` runs `git add -N .` and untracked workspace files enter the diff.
- Evidence: happyc0der competition digest, 2026-09-24 dataset copy, fetched 2026-11-25.
- Expected benefit: notes and reproduction scripts are not graded as product code.
- Cost: state disappears if `/tmp` is wiped mid-task.
- Risk: if the sandbox cwd is not allowed to read `/tmp`, scripts fail. Then the prompt still tells the model the policy.
- Validation: `test_localize_does_not_write_into_the_repository`.
- Rollback: stop calling scripts and edit from the prompt alone.

## D003 — Default model is 31B, no adapter

- Rationale: every public source lists `gemma-4-31b-it-qat-w4a16-ct`. Later sources also list 12B, E4B, and E2B. The small-model bonus is a separate final submission, and we have no measurement.
- Evidence: ReconScribe guide and Peoplerepabulic `competition-facts.md`. The live Kaggle page returned an application error on 2026-11-25, so this is not `VERIFIED` against Kaggle HTML.
- Expected benefit: the largest commonly allowed model is the default package.
- Cost: 31B is slower per task than E2B.
- Risk: the local 4 GB GPU cannot load it, so we cannot compare sizes here.
- Validation: packager allow-list. Inference `NOT_RUN`.
- Rollback: change the `model:` line to another id in the allow-list and rebuild the zip.

## D004 — Four-minute per-task cap

- Rationale: 120 tasks times 4 minutes is 8 hours, leaving time for sandbox setup and vLLM startup inside 12 hours.
- Evidence: task count and 12-hour cap are from secondary sources, not a local harness. `hegemon budget` computes 5.08 minutes per task after a 20-minute reserve and 45 seconds of setup.
- Expected benefit: one stuck task cannot consume the run.
- Cost: hard tasks may be cut off.
- Risk: `eval_config.yaml` key names may be wrong. The starter digest uses `max_time_minutes`, `max_tool_calls`, `max_turns`, `timeout_seconds`. Another public repo uses different keys. Unknown keys may be ignored or rejected.
- Validation: budget unit test. Official run `NOT_RUN`.
- Rollback: remove `eval_config.yaml` if the harness rejects it.

## D005 — Offline evolution cannot promote itself

- Rationale: prompt edits without a measured solve rate overfit the author's taste.
- Evidence: `promote()` rejects `NOT_RUN` and regressions. Tested.
- Expected benefit: the champion stays the last measured policy.
- Cost: no automatic prompt improvement until the harness runs.
- Risk: none in the submission. The evolution engine is development-only.
- Validation: `test_evolution_rejects_unmeasured_and_regressions`.
- Rollback: ignore `src/hegemon/evolution`.

## D006 — Do not train on external-model trajectories

- Rationale: as of the 2026-10-17 sources, distillation from proprietary APIs had no public host ruling.
- Evidence: ReconScribe FAQ, fetched 2026-11-25.
- Expected benefit: avoids a compliance reject.
- Cost: slower data collection.
- Risk: we may forgo a legal training signal if the host later allows it.
- Validation: no training run exists, so there is nothing to audit yet.
- Rollback: revisit only after an official forum ruling is saved in `docs/OFFICIAL_SOURCES.md`.

## D007 — V7A uses native tools and a 4096-token output cap

- Rationale: version 4 died at 72.3 seconds because a 16,384-token output reservation plus a 16,385-token prompt exceeded the 32,768 combined window. Versions 5 and 6 then timed out at about 307 seconds without an edit. The skill ranked its own scripts when it ran, and version 6 never called it.
- Evidence: `reports/ITERATION_3_FORENSICS.md` and `reports/FILESYSTEM_CONTRACT.md`, from notebook versions 3–6 on 2026-11-25. Harness text: `max_model_len = 32768` and `read_file` / `run_command` are workspace tools.
- Expected benefit: the prompt can grow past 16,384 tokens, a single generation cannot request 16,384 completion tokens, and search hits the task checkout.
- Cost: a tool call can be cut off if the model spends the 4,096 output tokens on reasoning. `thinking_budget` is 1,024 for this candidate.
- Risk: 1,024 may be too small for a correct edit. That is unmeasured. The checked-in model remains 31B; the notebook still overrides to 12B.
- Validation: unit tests for scope isolation. Notebook smoke on `experiments/splits/smoke_v7.json` is the measurement. Not promoted until that measurement exists.
- Rollback: restore `max_output_tokens: 16384`, `thinking_budget: 4096`, and `skills:` in `agent.yaml` from commit `7e67e08`.
