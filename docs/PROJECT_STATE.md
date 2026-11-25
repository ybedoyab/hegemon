# Project state

Updated: 2026-11-25

## Phase

`IMPLEMENTING`. Rules are accepted. Kaggle CLI is logged in as `ybedoyab`. Real 12B inference has run on one development task. Solve rate on that task is 0/1 for the official sample and for HEGEMON versions 2 through 6. Nothing has been submitted to the leaderboard.

## Champion

No champion. `configs/champion.json` is not promoted. Versions 5 and 6 stay rejected: same 0/1 solve rate, no edit.

## What is measured

- Official validator accepts the package (`HEGEMON_OFFICIAL_VALIDATE_OK`).
- Notebook `ybedoyab/hegemon-dev-eval` versions 2–6 completed on Nvidia L4 with vLLM `tp=4` and `gemma-4-12b-it-qat-w4a16-ct`.
- Version 4 stopped at 72.3 seconds on `ContextWindowExceededError` (32,768 combined limit, 16,384 reserved output tokens).
- Versions 5 and 6 timed out at about 307 seconds with no patch. Version 5 ranked skill scripts. Version 6 never called the skill.
- Checked-in model id remains `gemma-4-31b-it-qat-w4a16-ct`. That id has not been executed.

## Current candidate

V7A: native harness tools, no attached skill, `max_output_tokens` 4096, `thinking_budget` 1024. Smoke ids are in `experiments/splits/smoke_v7.json`. Measurement is not back yet.

## Review

`REQUEST_CHANGES` on `7e67e08`. Approval is null.
