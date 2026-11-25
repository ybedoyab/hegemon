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

The competition page "Model Selection, Budget, and Harness Rules", retrieved 2026-11-25, says `run_skill_script` runs in the persistent container and shares filesystem access with `run_command`, and that the time counts against the central budget. Version 5 still returned only skill scripts. Shared access did not stop the script from ranking its own directory. V7A does not attach the skill. Repository search goes through `run_command` and `read_file`. A later skill may read `/workspace` only when that path is the verified repository. It still must not scan `/tmp` or parent directories.

The skill script that remains in the tree accepts only an explicit workspace, or `HEGEMON_WORKSPACE` when no explicit path is given. That directory must exist, must not contain both `SKILL.md` and `scripts/localize.py`, and must contain `.git`, `pyproject.toml`, `setup.py`, or `setup.cfg`. Otherwise the script returns `workspace_not_visible` and no files. A repository directory named `scripts` stays searchable. The exclusion is the skill-tree marker, not the directory name.

`localize.py` reports `relevance` as an overlap ratio and `scope` as the accepted root. It does not report that ratio as a probability.
