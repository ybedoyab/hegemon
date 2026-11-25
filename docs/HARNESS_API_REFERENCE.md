# Harness API reference

Source: `HARNESS_README.md` downloaded 2026-11-25 with the Kaggle CLI. This note records the signatures our prompt depends on. It is not a copy of the official file.

## Harness tools

| Tool | Arguments | Counts as a tool call | Limit we rely on |
| --- | --- | --- | --- |
| `run_command` | `command` | yes | bash in `/workspace`. stdout and stderr truncated at 5,000 characters. Timeout is the command cap, at least 5 seconds, and does not end the session by itself. |
| `read_file` | `filepath`, `start_line`, `end_line` | yes | 1-indexed. Cap 150 lines and 10,000 characters. `..` is rejected. |
| `edit_file` | `filepath`, `old_string`, `new_string`, `allow_multiple=false` | yes | Exact match, then trimmed-line match, then flexible spacing. Empty file, empty `old_string`, or a non-unique match returns `FileEditError`. |
| `write_file` | `filepath`, `content` | yes | Creates parent directories. A file under `/workspace` enters `git diff`. |
| `get_status` | none | no | Remaining calls, time, turns, patch size. |
| `submit_patch` | none | no | `git add -N .` then `git diff --binary` against `_swegemma_baseline` or `HEAD`. Ends the loop after the current turn. |
| `get_code_neighbors` | `node`, `edge_type`, `max_neighbors=50` | yes | Symbol or suffix. Output cap 5,000 characters. |
| `search_similar_code` | `query`, `k=10` | yes | `query` is a symbol name. Offline lexical fallback. Not a sentence embedding. |
| `get_code_subgraph` | `nodes` | yes | Induced subgraph. Output cap 5,000 characters. |

## Skill tools

Present when `agent.yaml` has `skills:`. The harness coerces a one-element list to a string for `skill_name` and `file_path` on `load_skill`, `load_skill_resource`, and `run_skill_script`.

Our scripts still parse `--key value` from argv. A failed call returns `{"status":"error","error_type":...,"error":...}` instead of aborting the task.

## Patch and scratch

`submit_patch` and the fallback diff both stage untracked files under `/workspace`. Reproduction scripts go in `/tmp/hegemon`. Do not edit `pytest.ini` or `conftest.py`. The harness writes those before the agent starts.

## Budgets in this submission

```yaml
evaluation:
  timeout_seconds: 120
  max_tool_calls: 24
  max_time_minutes: 5
  max_turns: 40
```

`timeout_seconds` is the command timeout. These numbers are a budget choice. They are valid keys. They are not a measured optimum.

## Sampling

`thinking_level` is omitted. `thinking_budget` is 4096 and `max_output_tokens` is 16384, matching the harness note about truncated tool calls. `include_thoughts` is false so thought text is not kept in later turns. The official sample sets it true.
