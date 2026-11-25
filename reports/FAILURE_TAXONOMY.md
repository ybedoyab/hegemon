# Failure taxonomy

Source: private notebook `ybedoyab/hegemon-dev-eval` version 3, trace `trace_fastapi_15661.json`. One task. Not a leaderboard category distribution.

| Observed failure | Count | Evidence |
| --- | --- | --- |
| Time budget exhausted with no patch | 1 | HEGEMON ran 307.2s, 11 tool calls, 0 patch characters, `resolved=false`. Harness: timed out, no `submit_patch`, no working-tree edits. |
| Localization query was a paraphrase | 1 | `localize.py` received `problem` of 28 characters: "Automate release preparation". It returned `confidence=0.0`, `files=[]`, `next_action=graph_expand`. |
| Graph action was not taken | 1 | After that result the model did not call `search_similar_code` or `get_code_neighbors`. |
| Repeated search of the same script | 4 | `run_command` output for `scripts/add_latest_release_date.py` appears on four later steps. `read_file` opened that script, `pyproject.toml`, and two `.github/workflows` files. No `edit_file`. |
| One turn hit the output cap with no tool | 1 | Step 5 completion tokens were 16384, equal to `max_output_tokens`, and the step had no tool call. |

Tokens for the HEGEMON attempt: 105,738 prompt, 18,527 completion, 124,265 total, 0 cached. `vLLM` started with `tp=4`.

The official sample on version 2 of the same notebook also timed out on this task, at its own 1-minute cap, with 10 tool calls and no patch. That row is a budget timeout, not the same localization failure.

## Version 4 versus version 5

Same task, same 12B checkpoint, same 5-minute and 24-call budget.

| | Version 4 | Version 5 |
| --- | --- | --- |
| Resolved | no | no |
| Tool calls | 19 | 16 |
| Duration | 72.3s | 307.6s |
| Edits | 0 | 0 |
| Localize query | 28 characters, no code token | 245 characters, no path, snake_case, CamelCase, or traceback |
| Title gate | not in that build | did not fire |
| Ranked files | none, confidence 0 | five skill scripts, confidence 0.664, strategy direct_repair |
| Search after that | grep and ls for release | grep and ls for release, including two full reads of 39-line and 40-line files |

The gate did not improve retrieval. It also did not block a valid symbol query on this task, because the accepted query contained no symbol. The confidence increase is a scan of `skills/hegemon-repair`, which the skill process used when `/workspace` was not the checkout. The subprocess sandbox keeps the checkout under `/tmp/swegemma_sandbox_*/workspace`.

## Notebook version 7, four tasks, matched budget

Model `gemma-4-12b-it-qat-w4a16-ct`. Five minutes, 24 tool calls. Official sample and V7A. No compaction event appears in any of the eight traces. Cached tokens are 0. No observation contains `TimeoutExceeded`. Tool clock deltas stay under 2 seconds. A 301-second ending is the agent time budget. A gap after the last recorded step is an unfinished model generation, not a tool timeout.

| Task | Sample | V7A |
| --- | --- | --- |
| fastapi_15661 | 0 patch, 24 calls, 120.7s, tool budget, no edit | 0 patch, 20 calls, 301.7s, agent timeout, no edit |
| fastapi_13537 | edit of `fastapi/dependencies/utils.py` returned an error, then the 16,384-token output reservation overflowed the 32,768 window. 0 patch | five reads of that same file, no edit, agent timeout. Last recorded step at 121s |
| requests_6629 | three new scripts, 1,991 patch characters, tests failed (`exit_code` 1). No `edit_file` | 20 commands, including shell redirects into `test_*.py`, 0 patch because those files are stripped. Tool budget |
| rich_2725 | `edit_file` on `rich/table.py` succeeded, no `submit_patch`, agent timeout at 306.8s, harness kept the patch, tests passed | `edit_file` on `rich/table.py` succeeded at 116.8s, `submit_patch` succeeded, tests passed, 153.1s |

Solve rate on this set: sample 1/4, V7A 1/4. V7A is not promoted.

## Version 6

Same task and budget. `resolved=false`, 10 tool calls, 307.1s, 0 patch characters, 94,237 tokens. The trace contains no `run_skill_script` call, so the sandbox discovery did not run. The model listed `scripts/`, grepped for `release`, and fully read `scripts/add_latest_release_date.py` (40 lines, not truncated) without calling `edit_file`. Failure class: timeout with no edit. The skill-tree bug remains unmeasured on this run.
