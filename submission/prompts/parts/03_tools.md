## Tools

Harness tools, attached by name: `run_command`, `read_file`, `edit_file`, `write_file`, `get_status`, `submit_patch`, `get_code_neighbors`, `search_similar_code`, `get_code_subgraph`.

`run_skill_script` arguments are `skill_name`, `file_path`, and `args`. Use `file_path` `scripts/localize.py`, `scripts/state_update.py`, `scripts/summarize_pytest.py`, or `scripts/diff_guard.py`. If a call says the skill is not loaded, call `load_skill` once for `hegemon-repair` and retry.

`read_file` is 1-indexed and returns at most 150 lines and 10,000 characters. `edit_file` matches `old_string` exactly, then by trimmed lines, then by flexible spacing. It does not edit when the snippet is missing or matches several places. `run_command` output is truncated at 5,000 characters. `search_similar_code` and `get_code_neighbors` take a symbol name such as `Class.method`, not a sentence. `get_status` and `submit_patch` do not spend the tool-call budget. `submit_patch` ends the task after the current turn, so call it last, after the guard.
