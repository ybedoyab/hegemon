# Baseline comparison

Date: 2026-11-25. One development task. Not a leaderboard score and not a projected public score.

| Agent | Model in the session | Task | Resolved | Tool calls | Duration | Patch chars | Failure |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Official sample | gemma-4-12b-it-qat-w4a16-ct | fastapi_15661 | no | 10 | 67.2s | 0 | 1-minute sample budget timed out before `submit_patch` |
| HEGEMON commit before the kebab-case rename | same session | fastapi_15661 | no | 0 | 1.6s | 0 | skill name `hegemon_repair` rejected by the compiler |

The checked-in submission model is still `gemma-4-31b-it-qat-w4a16-ct`. This session overrode the copy to 12B. vLLM reported `tp=4`.

Solved tasks: 0 of 1 for the sample, 0 of 1 for HEGEMON. The HEGEMON row did not attempt a repair.
