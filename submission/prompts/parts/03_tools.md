## Tools

Harness tools: `run_command`, `read_file`, `edit_file`, `write_file`, `get_status`, `submit_patch`, `get_code_neighbors`, `search_similar_code`, `get_code_subgraph`.

Skill tools: `run_skill_script` and `load_skill_resource` for skill `hegemon_repair`. If the runtime requires `load_skill` before a script, call it once and then follow this policy.

`search_similar_code` takes a symbol name that exists in the repository graph. `read_file` is 1-indexed and returns at most 150 lines; ask for a window, not a whole module. `edit_file` fails when `old_string` matches zero or several places; include the surrounding lines that make it unique. `get_status` does not spend the tool budget; call it before a second edit if time may be short.

`submit_patch` ends the task. The grader also scores `git diff HEAD` if you never submit, and it resets test files, so leave tests unchanged.
