# Backlog

Ordered by expected effect on a real solve rate.

1. Notebook version 8 reruns the same four tasks after the prompt requires an edit once a file has been read twice, forbids repository test files, and checks `git diff -U3` before submit. Do not add tasks until that no-edit rate moves.
2. Promote nothing from the version 7 tie. Sample and V7A both solved 1/4.
3. If V7A still does not edit, change the native-tool prompt from the trace and re-measure. Do not put the skill back until a trace shows `run_skill_script` executing in the task repository.
4. Run the same smoke on `gemma-4-31b-it-qat-w4a16-ct` after the 12B loop produces a nonempty patch. The checked-in id is unmeasured.
5. Keep `encode/httpx` out of the smoke split. It has one development task.
6. LoRA only after a real training run on permitted data.

## Done

- Rules accepted, CLI authenticated, official harness downloaded
- Versions 2–6 measured on `fastapi_15661` at 0/1. Versions 5 and 6 are not promoted
- V7A packed at `8d537ad`: native tools, output cap 4096, thinking budget 1024
