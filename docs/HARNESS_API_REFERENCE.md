# Harness API reference

This is a working note, not a copy of `HARNESS_README.md`. Confirm every signature against the dataset file before treating a mismatch as a bug in our agent.

## Tools, as described by public digests

| Tool | Arguments described | Budget | Behavior we rely on |
| --- | --- | --- | --- |
| `run_command` | `command` | yes | Shell in the workspace. We use it for `/tmp/hegemon/repro.py` only. Output is truncated in the digest (about 5000 chars). |
| `read_file` | `filepath`, `start_line`, `end_line` | yes | 1-indexed. Digest says 150 lines and 10000 chars. Prompt asks for <= 80. |
| `edit_file` | `filepath`, `old_string`, `new_string`, `allow_multiple=false` | yes | Exact match, then flexible match. Zero or many matches error. |
| `write_file` | `filepath`, `content` | yes | Creates directories. Avoid for scratch. |
| `get_status` | none | no, per digest | Budget and patch status. |
| `submit_patch` | none | no | Ends the turn. Digest: `git add -N . && git diff HEAD`. |
| `get_code_neighbors` | `node`, `edge_type=None`, `max_neighbors=50` | yes | Symbol resolution. Graph files may be absent. |
| `search_similar_code` | `query`, `k=10` | yes | Digest says `query` is a symbol name, not a sentence. |
| `get_code_subgraph` | `nodes` | yes | Induced subgraph. |
| `load_skill` | `name` | unknown | Upstream ADK loads `SKILL.md`. |
| `load_skill_resource` | `skill_name`, `path` | unknown | Reads a skill file. |
| `run_skill_script` | `skill_name`, `script_path`, `args` object | yes, time counts | Upstream ADK passes args as `--key value` and runs the script from a temp copy of the skill. Scripts must use absolute workspace paths. |

## Skill scripts we ship

- `hegemon_repair/scripts/localize.py`
- `hegemon_repair/scripts/state_update.py`
- `hegemon_repair/scripts/summarize_pytest.py`
- `hegemon_repair/scripts/diff_guard.py`

`common.py` is imported by those scripts.

## Session behavior we plan for, still unverified here

- If the agent never calls `submit_patch`, the digest says the harness still grades `git diff HEAD`.
- Test files named by the official test patch are reset, so editing tests is useless.
- Scratch inside the workspace is dangerous because of `git add -N`.
- Context compaction may not save a single long task. The digest argues for staying under roughly 20 large tool results.

## Not confirmed

Exact `eval_config.yaml` schema, whether `load_skill` is required before `run_skill_script`, whether `/tmp` persists across tasks, and whether the harness passes skill args the way upstream ADK does.
