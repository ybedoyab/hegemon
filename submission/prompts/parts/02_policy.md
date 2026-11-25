## Decision policy

Keep all scratch files in `/tmp/hegemon`. A file written inside the repository becomes part of the patch.

Start with `run_skill_script` on skill `hegemon_repair`, script `scripts/localize.py`. Pass `problem`: the issue title, exception names, file paths, and the specific failing behavior. Omit long logs.

Then obey `next_action`:

- `read_top_file`: `read_file` the first ranked file. Use the returned `start_line` and `end_line`. Do not read more than 80 lines. Then `state_update.py` with `event=read_done`.
- `graph_expand`: `get_code_neighbors` or `search_similar_code` once, using a symbol name from the localize result, not a sentence. Then read the new file.
- `edit`: `edit_file` once. `old_string` must be copied from the file you just read. Change the smallest span that fixes the cause. Then `state_update.py` with `event=edit_done` and `fingerprint` set to a short hash or unique snippet of that edit.
- `reproduce`: write `/tmp/hegemon/repro.py` with `run_command`. Expectations come only from the issue and the behavior you observed. Then `summarize_pytest.py` with that target.
- `rerun`: `summarize_pytest.py` on one related test file from the localize result, or on `/tmp/hegemon/repro.py`. Do not run the whole suite.
- `revise`: read `category`. If it is `env_error`, do not treat the failure as a wrong patch. If it is `assertion`, call `state_update.py` with `event=failure` and the tail. If `repeated` is true, choose a different file or a different hypothesis. Do not apply the same edit again.
- `submit`: `diff_guard.py`. If it returns `submit`, call `submit_patch`. If it returns `revise`, remove test-file edits and unrelated files first.
- `stop`: call `submit_patch` only when `diff_guard.py` says the diff is non-empty and does not touch tests. Otherwise make no further edits.

A simple defect is localize, one read, one edit, one targeted test, diff_guard, submit. Do not explore the rest of the repository when confidence is high.

When two files have similar scores, inspect the second file before editing. When the issue names a compatibility or serialization boundary, read the function that crosses that boundary, not only the line in the traceback.
