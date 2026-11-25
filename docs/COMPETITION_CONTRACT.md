# Competition contract

Read date: 2026-11-25.

The live pages `overview`, `rules`, and the competitions API did not return usable official text (SPA error and HTTP 401). Nothing below that depends on those pages is marked `VERIFIED_*`. Working assumptions used in `submission/` are the intersection of the secondary sources listed in `docs/OFFICIAL_SOURCES.md`.

## Scoring

Secondary sources agree on a SWE-bench style score: a patch is applied to a fresh tree, the task's tests run, and the score is the fraction of tasks that pass. Public and private halves of about 120 hidden tasks. Private rank decides prizes. Ties go to the earlier submission.

This project has not run that grader.

## Time and hardware

Secondary sources: 12 hours for all tasks, including sandbox setup and vLLM startup, excluding patch validation. One submission per day. Hardware described as 4x L4 (96 GB), internet off, `max_model_len` 32768.

Per-task arithmetic used here: `python -m hegemon budget` returns 305 seconds after a 20-minute reserve and 45 seconds of setup on 120 tasks. `submission/eval_config.yaml` asks for 4 minutes, which is inside that envelope. Both the task count and the YAML keys are `UNKNOWN` against the official file.

## Models

| ID | Small-model bonus | Status |
| --- | --- | --- |
| `gemma-4-31b-it-qat-w4a16-ct` | no | Working default. Every secondary source names it. |
| `gemma-4-12b-it-qat-w4a16-ct` | no | Named by October 2026 sources. September digest said 31B only. `UNKNOWN`. |
| `gemma-4-e4b-it-qat-w4a16-ct` | yes, if sources are right | `UNKNOWN` |
| `gemma-4-e2b-it-qat-w4a16-ct` | yes, if sources are right | `UNKNOWN` |

All agents in one submission must share one base model. Different LoRA adapters per agent are described as allowed. This zip ships no adapter.

## Submission shape

`submission.zip` at `/kaggle/working/submission.zip`, `agent.yaml` at the zip root, under 3 GiB, no symlinks, no `..`. Optional `configs/`, `prompts/`, `skills/`, `sub_agents/`, `adapters/`, `eval_config.yaml`.

Our packer enforces that shape for the local tree. It is not the official notebook validator.

## Data

Development set described as 129 tasks from fastapi, rich, requests, and httpx, about 22.42 GB, Apache-2.0, with snapshots, graphs, embeddings, wheels, and a sample submission. Not downloaded. Do not redistribute it.

Hidden tasks are described as coming from private repositories, so memorizing the four public libraries is a weak strategy.

## Disabled until verified

- Cross-task memory
- Online weight updates
- Sub-agents
- LoRA
- Any eval_config key that `HARNESS_README.md` does not list
- Network access inside the sandbox
- A second base model in the same zip

## Deadlines from secondary sources

- Entry and team merger: 2026-11-25 23:59 UTC
- Final submission: 2026-12-02 23:59 UTC
- Paper track: closed 2026-11-12

Confirm these on the Kaggle timeline before relying on them. The entry gate is today relative to this session.
