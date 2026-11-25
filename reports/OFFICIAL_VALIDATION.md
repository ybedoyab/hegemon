# Official validation

Status: IN_PROGRESS. Not a pass.

Notebook: https://www.kaggle.com/code/ybedoyab/hegemon-dev-eval
Version: 2 (version 1 was replaced before model load; its evaluator call used a wrong keyword)
Status at second launch: KernelWorkerStatus.QUEUED
Accelerator requested: NvidiaL4 (the official starter metadata uses this single L4 shape, not four L4s)
Internet: disabled
Model for this run: gemma-4-12b-it-qat-w4a16-ct, rewritten inside the notebook only
Checked-in submission model: gemma-4-31b-it-qat-w4a16-ct
Package: dist/submission.zip sha256 5bee3c2553d90e553003fbd773f3dcc2186c38a50a04adec41e5543bad51b677

The notebook calls `adk_submission.validate_directory` before loading the model. No validator output has been retrieved yet.

No task has been scored. No leaderboard submission was made.
