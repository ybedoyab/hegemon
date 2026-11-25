# Project state

Updated: 2026-11-25

## Phase

`IMPLEMENTING`. Foundation is executable. Official baseline is `NOT_RUN`.

## Machine

- Windows 11, Ryzen 7 5800U, 16 logical CPUs, 15.36 GB RAM (about 2.4 GB free at discovery)
- NVIDIA GeForce RTX 3050 Ti Laptop, 4096 MiB, driver 591.44, compute capability 8.6
- Python 3.12.3 and 3.11.9, Git 2.41, GitHub CLI logged in as `ybedoyab`, uv 0.12.5
- Docker client 29.8.0 installed; the daemon was not running. WSL2 Ubuntu is installed.
- Kaggle CLI is not installed. `%USERPROFILE%\.kaggle\kaggle.json` is absent.
- Hugging Face cache contains only `sentence-transformers/all-MiniLM-L6-v2`. No Gemma checkpoint.
- C: had about 1.1 GB free. D: had about 142 GB free. Keep caches on D:.

## Repository

- `https://github.com/ybedoyab/hegemon`
- Private, default branch `main`, initial commit `5134dcb` at discovery
- Push permission works for `ybedoyab`
- Branch protection API returned HTTP 403 (GitHub Pro required). Treat `main` as unprotected.

## Champion

`configs/champion.json`: structured single-agent policy. Solve rate `null`. Status `NOT_RUN` on the official harness.

## What is implemented

- Submission prompt and skill scripts: localize, state update, pytest summary, diff guard
- Development policy wrappers, budget split, experience compiler, evolution gate
- Zip builder and 17 unit tests
- Synthetic localization probe: 2/2 top-1

## What is not implemented

- Official starter reproduction
- Any Gemma generation
- LoRA training
- A scored Kaggle submission

## Immediate blocker

The official dataset and `HARNESS_README.md` are behind a Kaggle rules acceptance. Without them, tool schemas and `eval_config.yaml` field names stay corroborated, not verified. The entry deadline is 2026-11-25 23:59 UTC.
