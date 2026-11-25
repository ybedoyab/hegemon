Iteration 4 measurement. This is not a request for approval.

Commit measured: 8d537ad on feat/hegemon-core.
Notebook: https://www.kaggle.com/code/ybedoyab/hegemon-dev-eval version 7.
Model in the notebook: gemma-4-12b-it-qat-w4a16-ct. Checked-in model remains gemma-4-31b-it-qat-w4a16-ct.
Tasks and budget: fastapi_15661, fastapi_13537, rich_2725, requests_6629. Five minutes, 24 tool calls, for both the official sample and V7A.

Solved/attempted: sample 1/4, V7A 1/4. Both solved rich_2725 only. V7A called submit_patch on that task at 153 seconds, first edit at 117 seconds. The sample did not call submit_patch; the harness kept its edit and the tests passed after a 307-second agent timeout.

The other three V7A runs produced no library edit. fastapi_15661 and fastapi_13537 hit the agent time budget. requests_6629 hit the tool-call budget after shell redirects into test files, which the harness strips. No trace contains a compaction event. Cached tokens are 0. No tool command timed out.

V7A is not promoted. Decision requested: REQUEST_CHANGES. Do not approve a leaderboard upload.
