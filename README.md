# HEGEMON

Adaptive software-repair agent for the [Gemma 4 Developer Agent competition](https://www.kaggle.com/competitions/gemma-4-developer-agent/overview).

The scored artifact is `submission/`: one Gemma 4 agent config, a short policy prompt, and standard-library skill scripts. `src/hegemon/` is the development harness. It does not run inside Kaggle.

## Current evidence

| Check | Result |
| --- | --- |
| Unit tests | 17 passed locally on Python 3.12 |
| Synthetic localization top-1 | 2/2 fixtures (`experiments/E_LOC001.json`) |
| Official harness solve rate | `NOT_RUN` |
| Real Gemma inference | `NOT_RUN` (4 GB GPU; checkpoints not downloaded) |
| Kaggle leaderboard | no submission from this project |

A public score of 0.24 is the target. It is not a result we have.

## Commands

```powershell
$env:PYTHONPATH = "src"
python -m pytest -q
python scripts/run_localization_probe.py
python -m hegemon env
python -m hegemon budget
python -m hegemon pack
```

`python -m hegemon pack` writes `dist/submission.zip` with `agent.yaml` at the archive root.

## Blocker before any Kaggle run

Accept the competition rules on Kaggle before 2026-11-25 23:59 UTC if that has not already been done. Place an API token at `%USERPROFILE%\.kaggle\kaggle.json` without pasting it into chat. This machine does not have that file, so the 22 GB dataset and `HARNESS_README.md` are not local.

## Layout

- `submission/` — zip contents
- `src/hegemon/` — policy wrappers, packager, offline evolution gate
- `experiments/` — measured results only
- `docs/PROJECT_STATE.md` — resume here
