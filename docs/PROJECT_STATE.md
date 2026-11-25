# Project state

Updated: 2026-11-25

## Phase

`IMPLEMENTING`. Official harness file and sample submission are downloaded. Rules are accepted. Gemma inference is `NOT_RUN`. Official baseline is `NOT_RUN`.

## Machine

- Windows 11, Ryzen 7 5800U, 16 logical CPUs, 15.36 GB RAM (about 2.4 GB free at discovery)
- NVIDIA GeForce RTX 3050 Ti Laptop, 4096 MiB, driver 591.44, compute capability 8.6
- Python 3.12.3 and 3.11.9, Git 2.41, GitHub CLI logged in as `ybedoyab`, uv 0.12.5
- Docker client 29.8.0 installed; the daemon was not running. WSL2 Ubuntu is installed.
- Kaggle CLI 2.2.5 is installed in `D:\cache\hegemon-venv` and logged in as `ybedoyab` through browser OAuth. Credentials are outside the repository.
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

No permitted Gemma checkpoint has been executed. The local GPU has 4 GB and cannot load the 31B checkpoint. The submission schema now matches the downloaded harness. A solve rate does not exist yet.
