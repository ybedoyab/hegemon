## Decision policy

Scratch state lives in `/tmp/hegemon`. A file created inside the repository is part of the submitted diff. Put reproduction scripts in `/tmp/hegemon`, never in `/workspace`.

Emit exactly one tool call per turn.

First call `run_skill_script` with `skill_name` `hegemon-repair` and `file_path` `scripts/localize.py`. Pass `problem` as the issue title, exception names, file paths, and the failing behavior. Then follow `next_action`.

- `read_top_file`: `read_file` the next unread ranked file, using the returned `start_line` and `end_line`, at most 80 lines. Then `state_update.py` with `event=read_done`.
- `graph_expand`: one `get_code_neighbors` or `search_similar_code` using a symbol name from the localize result, then read the new file.
- `edit`: one `edit_file`. Copy `old_string` from a file you read. Change the smallest span that can fix the cause. Then `state_update.py` with `event=edit_done` and a short `fingerprint`.
- `reproduce`: write `/tmp/hegemon/repro.py` with `run_command` from behavior named in the issue, then summarize that file.
- `rerun`: `summarize_pytest.py` on one related test file or `/tmp/hegemon/repro.py`.
- `revise`: if `category` is `env_error`, the patch is not disproven. If it is `assertion`, call `state_update.py` with `event=failure` and the tail. A repeated fingerprint changes strategy. Edit the same file again when the failure names a new line.
- `submit`: `diff_guard.py`. Call `submit_patch` only when it returns `submit`.
- `stop`: call `submit_patch` only when `diff_guard.py` accepts a non-empty diff.

When confidence is high, read one window and edit. When two files score similarly, read the second before editing. When a targeted test fails after the edit, use the failure text before the next edit. When `get_status` shows few calls left, or the same fingerprint has failed twice, submit the best diff the guard accepts.
