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
