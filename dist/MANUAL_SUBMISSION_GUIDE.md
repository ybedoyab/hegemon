# Manual submission guide

Do not treat this zip as a scored submission. The official notebook and `HARNESS_README.md` are not in this workspace.

1. Accept the competition rules on Kaggle before the entry deadline (secondary sources say 2026-11-25 23:59 UTC).
2. Copy the official starter notebook. Do not replace its vLLM or evaluator cells with anything from this repo.
3. Put the contents of `dist/submission.zip` where that notebook expects the agent tree, with `agent.yaml` at the root of the archive it writes to `/kaggle/working/submission.zip`.
4. Confirm the model id against the official list. This zip selects `gemma-4-31b-it-qat-w4a16-ct` and includes no LoRA.
5. Run the starter's own validator. If it rejects `eval_config.yaml`, delete that file and pack again. The key names are an unverified hypothesis.
6. Submit from the Kaggle UI. This repository has no submit command.

Rebuild locally with:

```powershell
$env:PYTHONPATH = "src"
python -m hegemon pack
```

Compare `dist/SHA256SUMS` with the file you upload.
