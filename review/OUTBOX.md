Iteration 3 evidence. This is not a request for approval.

Commit: 7e67e08 and the measurement commit that follows it on feat/hegemon-core.
PR: https://github.com/ybedoyab/hegemon/pull/1
Notebook: https://www.kaggle.com/code/ybedoyab/hegemon-dev-eval
Model in the notebook: gemma-4-12b-it-qat-w4a16-ct, vLLM tp=4.
Checked-in submission model remains gemma-4-31b-it-qat-w4a16-ct.
Task: fastapi_15661 only. Budget: 5 minutes, 24 tool calls. No leaderboard submission.

Results, solved/attempted:

- Official sample: 0/1. 10 calls, 67.2s, no patch. Its 1-minute cap timed out.
- HEGEMON v4: 0/1. 19 calls, 72.3s, 189,962 tokens, no edit. Localize received a 28-character title.
- HEGEMON v5: 0/1. 16 calls, 307.6s, 155,729 tokens, no edit. The title gate did not fire. A 245-character prose query with no code token was accepted. Reported confidence 0.664 ranked the skill scripts, not the repository.
- HEGEMON v6: 0/1. 10 calls, 307.1s, 94,237 tokens, no edit. The skill was never called, so sandbox discovery was not exercised. The model fully read scripts/add_latest_release_date.py and did not edit.

The title-only gate neither improved retrieval nor blocked a valid symbol search on this task. Version 5's higher confidence was a false ranking of the skill tree. Neither v5 nor v6 is promoted.

Decision requested: REQUEST_CHANGES, with the next implementation prompt. Do not approve.
