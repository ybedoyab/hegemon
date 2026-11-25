# Filesystem contract

Read from `HARNESS_README.md` on 2026-11-25, plus the version 5 trace. This is the boundary V7A uses.

| Location | What runs there | What it can see |
| --- | --- | --- |
| Submission package | Files unpacked from the zip for `compile_submission` | `agent.yaml`, prompts, and any skill directory. Not the task repository. |
| Skill script process | `run_skill_script` through the ADK skill tool | The script's own directory unless a path is passed in. Version 5 ranked `scripts/localize.py` and the other skill scripts. `/workspace` was not the tree that got ranked. |
| Task repository | `run_command`, `read_file`, `edit_file`, `write_file`, `submit_patch` | `/workspace` in the agent sandbox. The subprocess sandbox rewrites `/workspace` to `/tmp/swegemma_sandbox_<id>_.../workspace`. Paths are resolved relative to that checkout. `..` is rejected. |
| Evaluator | Phase 2 verification | A fresh checkout plus the submitted patch. The agent does not run there. |
| Scratch | Skill state, only if a skill is invoked | `HEGEMON_STATE_DIR`, default `/tmp/hegemon`. Not inside the repository, because `submit_patch` stages untracked files. |

`run_command` is documented to execute `/bin/bash -c` inside `/workspace`. `read_file` slices a file under that same checkout and accepts `start_line` and `end_line`.

The skill and the task checkout are not the same filesystem view. Inferring the repository from the skill script path, the skill process current directory, or a scan of `/tmp/swegemma_sandbox_*` is not a documented skill input. V7A does not attach the skill. Repository search goes through `run_command` and `read_file`.

The skill script that remains in the tree accepts only an explicit workspace, or `HEGEMON_WORKSPACE` when no explicit path is given. That directory must exist, must not contain both `SKILL.md` and `scripts/localize.py`, and must contain `.git`, `pyproject.toml`, `setup.py`, or `setup.cfg`. Otherwise the script returns `workspace_not_visible` and no files. A repository directory named `scripts` stays searchable. The exclusion is the skill-tree marker, not the directory name.

`localize.py` reports `relevance` as an overlap ratio and `scope` as the accepted root. It does not report that ratio as a probability.
