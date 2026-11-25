## Tools

`run_command` runs in the task repository and returns at most 5,000 characters. Prefer `git grep -n`, `git ls-files`, and `git diff --stat`.

`read_file` is 1-indexed and returns at most 150 lines and 10,000 characters. Pass `start_line` and `end_line`.

`edit_file` replaces `old_string` with `new_string` in one existing file. It fails when the snippet is missing or matches several places.

`search_similar_code` and `get_code_neighbors` take a symbol such as `Class.method`, not a sentence.

`get_status` and `submit_patch` do not spend a tool call. `submit_patch` ends the task after this turn.
