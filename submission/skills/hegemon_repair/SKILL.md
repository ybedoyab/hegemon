---
name: hegemon_repair
description: Localize a Python bug from the issue text, record evidence, summarize one targeted test, and check the patch before submit_patch.
---

# HEGEMON repair skill

Use these scripts with `run_skill_script`. Arguments are a JSON object of strings. Scratch files stay in `/tmp/hegemon`. Never write scratch files into the repository.

## Scripts

1. `scripts/localize.py` via `file_path`. Args `problem` (short issue text: title, exceptions, paths, the failing behavior) or `problem_file`. Returns ranked files, a symbol, a confidence, and `next_action`.
2. `scripts/state_update.py` args `event` (`read_done`, `edit_done`, `failure`, `success`, `repeated`), `detail` (short evidence), optional `category` and `fingerprint`. Returns the next action from the evidence, and rejects a repeated failing edit.
3. `scripts/summarize_pytest.py` args `target` (one test file or `/tmp/hegemon/repro.py`). Returns a short tail and `pass`, `assertion`, or `env_error`. An import error is an environment failure, not proof the patch is wrong.
4. `scripts/diff_guard.py` no required args. Returns whether the current diff is empty, touches tests, or is safe to submit.

Follow `next_action` from the script. Do not repeat a fingerprint that the state script has rejected.
