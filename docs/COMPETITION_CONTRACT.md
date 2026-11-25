# Competition contract

Read date: 2026-11-25. Sources opened in this session:

- Kaggle rules page, signed-in session: banner "You have accepted the rules for this competition."
- `HARNESS_README.md` downloaded with the official CLI to `D:\kaggle-data\gemma-4-developer-agent\` (55,940 bytes, file dated 2026-10-13). Not committed.
- Official `sample_submission/agent.yaml`, `eval_config.yaml`, and `configs/sampling.yaml` from the same dataset.
- `tasks.jsonl`: 129 lines. Contains reference patches. Not committed and not given to the solver.

## Scoring

The downloaded harness describes Phase 2 as applying the agent patch and running pytest. A public leaderboard score has not been produced. Do not treat a unit-test pass as a solve rate.

## Time and hardware

Verified from `HARNESS_README.md`:

- Evaluation serving: 4x NVIDIA L4, 96 GB, vLLM, `tensor_parallel_size=4`, `max_model_len=32768`, tool and reasoning parsers `gemma4`.
- Sandbox network mode `none`.
- Unpacked submission under 3 GiB (3,221,225,472 bytes). No symlinks. No `..`.
- Per-task keys live under `evaluation:` in `eval_config.yaml`: `timeout_seconds` (command timeout), `max_tool_calls`, `max_time_minutes`, `max_turns`.
- Defaults in `inference.py` when unset: 60 minutes, 100 tool calls, 500 turns, 300 second command timeout. The sample submission uses 1 minute, 10 calls, 50 turns, 60 second command timeout.
- Agent time starts after container setup. `get_status` and `submit_patch` do not count as tool calls. `submit_patch` ends the loop after the current turn.
- Context compaction is configured (`token_threshold` 14336, interval 15). This replaces the earlier assumption that compaction does not run.

Not in the harness file: the 12-hour wall clock and the one-submission-per-day rule. Those remain timeline claims from the competition pages, not harness constants. `submission/eval_config.yaml` uses 5 minutes, 24 tool calls, 40 turns, and a 120 second command timeout so a full task set cannot inherit the 60-minute default.

## Models

Verified allowed base checkpoints, exactly one per submission:

| ID | Notes |
| --- | --- |
| `gemma-4-31b-it-qat-w4a16-ct` | Default. This submission. |
| `gemma-4-12b-it-qat-w4a16-ct` | Allowed. Not selected. |
| `gemma-4-e4b-it-qat-w4a16-ct` | Allowed. Small-model prize depends on the rules page, not this file. |
| `gemma-4-e2b-it-qat-w4a16-ct` | Allowed. Same caveat. |

Unquantized Gemma variants are documented as local-CLI only. No LoRA is shipped. `thinking_level` is omitted because the harness says the vLLM OpenAI endpoint should not receive it.

## Submission shape

Official sample `agent.yaml` uses bare tool names, `instruction: !include`, and `generate_content_config: !include`. Skills are a list of relative directories. V7A matches that shape and does not set `skills:`. The repair skill remains in the tree for a later comparison and is not offered to the model. It does not declare `load_skill` as a harness tool. The harness adds skill tools when `skills:` is set.

`agent_class: LlmAgent` is the documented default and is omitted, matching the sample.

## Tools

Nine harness tools: `run_command`, `read_file`, `edit_file`, `write_file`, `get_status`, `submit_patch`, `get_code_neighbors`, `search_similar_code`, `get_code_subgraph`. Signatures are in `docs/HARNESS_API_REFERENCE.md`.

Skill script argument coerced by the harness is `file_path`, together with `skill_name`.

## Data

129 development tasks downloaded. Snapshots, graphs, embeddings, wheels, and the full 22 GB set are not fully downloaded. Reference `patch` fields stay outside git and outside the solving prompt.

## Still disabled

- Cross-task memory during official evaluation
- Online weight updates
- A second base model
- Network inside the sandbox
- Automatic Kaggle submission

## Deadlines seen on the competition timeline

- Entry and team merger: 2026-11-25 23:59 UTC
- Final submission: 2026-12-02 23:59 UTC

Rules acceptance for this account is already recorded. See `docs/REGISTRATION_STATUS.md`.
