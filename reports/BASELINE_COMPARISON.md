# Baseline comparison

Date: 2026-11-25. One development task. Not a leaderboard score and not a projected public score.

| Agent | Model in the session | Task | Resolved | Tool calls | Duration | Patch chars | Failure |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Official sample | gemma-4-12b-it-qat-w4a16-ct | fastapi_15661 | no | 10 | 67.2s | 0 | 1-minute sample budget timed out before `submit_patch` |
| HEGEMON before the kebab-case rename | same version-2 session | fastapi_15661 | no | 0 | 1.6s | 0 | skill name `hegemon_repair` rejected by the compiler |
| HEGEMON after the rename, version 3 | gemma-4-12b-it-qat-w4a16-ct, tp=4 | fastapi_15661 | no | 11 | 307.2s | 0 | 5-minute budget timed out. Localization got a 28-character paraphrase and returned no files. No edit. |
| HEGEMON version 4, localize-first prompt | same | fastapi_15661 | no | 19 | 72.3s | 0 | Localize ran first, still with a 28-character query. No edit. Stopped before the 5-minute cap. 189,962 tokens. |
| HEGEMON version 5, title gate | same | fastapi_15661 | no | 16 | 307.6s | 0 | Gate did not fire. A 245-character prose query was accepted. Confidence 0.664 ranked the skill scripts, not the repository. No edit. Timed out. 155,729 tokens. |

Version 5 is not a champion. Solve rate stayed 0 of 1, time to first edit stayed infinite, and the higher confidence was measured on the wrong tree.

The checked-in submission model is still `gemma-4-31b-it-qat-w4a16-ct`. This session overrode the copy to 12B. vLLM reported `tp=4`.

Solved tasks: 0 of 1 for the sample, 0 of 1 for HEGEMON. The HEGEMON row did not attempt a repair.
