## Work

Reply with the next tool call. Do not spend the turn on a long analysis.

1. Extract the requested behavior, identifiers, and expected result.
2. Search with `run_command` for an exact identifier, error string, or API name. If the issue names none, search for the affected behavior and the API it mentions.
3. Read a short window with `read_file`, passing `start_line` and `end_line`. Stay near 80 lines.
4. When the relevant function is visible, call `edit_file`. Copy `old_string` from that read. Change the smallest span that can fix the cause.
5. Run one focused check when a relevant test or snippet can execute. Do not invent test results.
6. Use `get_status` after several calls. Inspect `git diff --stat`, then call `submit_patch` before the time budget ends.

Do not spend the whole task exploring. Do not repeat a search or a read that added no new evidence. Do not read the repository broadly. A reversible edit is appropriate once the relevant function is visible. Do not submit an empty patch.

Search order: exact symbol or error string, then `git grep -n` for that term, then a related test name, then `search_similar_code` or `get_code_neighbors` for a symbol you already found.
