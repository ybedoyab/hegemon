# Self evolution

Three levels, and what exists today.

## Level 1 — inside one task

Implemented in `submission/skills/hegemon_repair/scripts/state_update.py`.

- A failure increments `attempts` and stores a fingerprint.
- The same fingerprint a second time sets `repeated` and returns `graph_expand`.
- A third failure returns `submit` if a non-test patch exists, otherwise `stop`.
- `env_error` is not treated as proof the patch is wrong (`summarize_pytest.py`).
- A new `localize.py` call replaces state, so a new problem does not keep the previous hypothesis.

This is deterministic. It does not update weights.

## Level 2 — offline, during development

`src/hegemon/evolution/engine.py` can append a bullet and will promote a challenger only when solve rate is measured on the same task count and is higher. No challenger has been measured. The champion solve rate stays null.

`src/hegemon/memory/experience.py` turns failure categories into generic sentences. It drops repository names, instance ids, and patch bodies. Tested.

## Level 3 — across evaluation tasks

Disabled. `configs/features.yaml` sets `cross_task_evaluation_memory: false` and `online_weight_updates: false`.

A persistent container would not change this. `localize.py` overwrites state when it is called. Do not add a file that survives to the next task.
