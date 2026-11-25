# Official validation

Date: 2026-11-25. Notebook https://www.kaggle.com/code/ybedoyab/hegemon-dev-eval version 2. Status: COMPLETE.

Accelerator flag: `NvidiaL4`. The session started vLLM with `tp=4`, so at least four CUDA devices were visible. GPU product names were not printed.

Internet: disabled. Checked-in model remains `gemma-4-31b-it-qat-w4a16-ct`. The notebook rewrote the in-session copy to `gemma-4-12b-it-qat-w4a16-ct` before validation, matching the official starter's single-session model choice.

## Directory validator

`adk_submission.validate_directory` printed:

`HEGEMON_OFFICIAL_VALIDATE_OK files 10 model_override gemma-4-12b-it-qat-w4a16-ct`

That check did not load the skill. The runtime compiler did.

## Runtime compiler

HEGEMON did not start. `compile_submission` rejected the skill frontmatter:

`name must be lowercase kebab-case ... input_value='hegemon_repair'`

`validate_directory` is not sufficient. The skill name is now `hegemon-repair` in the tree that will be sent as version 3. Version 2 did not run that name.

## Official sample on the same boot

Task `fastapi_15661`, repo `fastapi/fastapi`, model `gemma-4-12b-it-qat-w4a16-ct`.

`resolved=False, exit_code=-1, patch_chars=0, tool_calls=10, duration=67.2s`

The harness logged `agent timed out` and `completed without explicit submit_patch call and no working tree modifications`. The sample `eval_config.yaml` caps the task at 1 minute and 10 tool calls. This is one timed-out task, not a solve rate.

## HEGEMON on that task in version 2

`resolved=false, exit_code=-1, patch_chars=0, tool_calls=0, duration_seconds=1.60`

The failure is the skill-name rejection above. No repair was attempted.

## Version 3

`validate_directory` again printed `HEGEMON_OFFICIAL_VALIDATE_OK`. The compiler accepted `hegemon-repair`. vLLM started with `tp=4`.

HEGEMON on `fastapi_15661`: `resolved=false`, 11 tool calls, 307.2 seconds, 0 patch characters. The harness timed the agent out. See `reports/FAILURE_TAXONOMY.md`.

## Versions 4 and 5

Both completed `HEGEMON_OFFICIAL_VALIDATE_OK` and started vLLM with `tp=4`. Neither solved `fastapi_15661`. Version 5's localize confidence of 0.664 ranked the skill scripts. That is not a successful localization.
