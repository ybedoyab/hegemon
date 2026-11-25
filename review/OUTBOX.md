# HEGEMON outbox — iteration 1

Date: 2026-11-25

## Git

- Repository: https://github.com/ybedoyab/hegemon
- Visibility: private
- Branch: `feat/hegemon-core`
- Agent commit: `11352bb13f2651249c5d04172e4c3ad3a69a59eb`
- Pull request: filled in after `gh pr create`
- Remote verification: pending until push

## Scope

First executable foundation. Not a submission candidate.

## What actually runs

- `submission/skills/hegemon_repair/scripts/localize.py` ranks Python files from issue text and writes `/tmp/hegemon/state.json` (or `HEGEMON_STATE_DIR`).
- `state_update.py` rejects a repeated failing edit and switches action.
- `summarize_pytest.py` summarizes one targeted pytest output and separates `env_error` from `assertion`.
- `diff_guard.py` refuses a test-only diff.
- `python -m hegemon pack` builds `dist/submission.zip` (12425 bytes, SHA-256 `6aef0dcb24d01a3e96aef5d56795c46e821ff88722b3abcdfa0bb276e017f5bd`, 10 entries, `agent.yaml` at root).

## What does not run

- Official starter agent
- Gemma inference of any size
- Official harness
- LoRA training
- Kaggle submission

## Measured results

`experiments/E_LOC001.json`: synthetic top-1 localization 2/2. Solve rate: null. Official status: `NOT_RUN`.

Unit tests before the commit: 17 passed, Python 3.12.3, Windows. No GPU test. No CI run on GitHub yet.

## Decisions

See `docs/DECISIONS.md`. Short version: one agent, skill scripts, scratch outside the repo, 31B as the default id, 4-minute task cap as an unverified YAML hypothesis, no adapter.

## Compliance

Kaggle HTML and the dataset were not readable from this machine on 2026-11-25. The contract in `docs/COMPETITION_CONTRACT.md` is secondary. Cross-task memory and online updates are off. No reference patches are in the repo. Repository is private.

## Limitations

- `eval_config.yaml` keys may be rejected or ignored.
- Skill argument passing is taken from upstream ADK, not from `HARNESS_README.md`.
- Local GPU is a 4 GB RTX 3050 Ti. The 31B checkpoint will not load here.
- No `kaggle.json`, so the dataset cannot be downloaded.
- Entry deadline reported by secondary sources is 2026-11-25 23:59 UTC. This session cannot accept the rules.

## Reproduce

```powershell
$env:PYTHONPATH = "src"
python -m pytest -q
python scripts/run_localization_probe.py
python -m hegemon pack
```

## Requested reviewer decision

`REQUEST_CHANGES`. Do not return `APPROVE_FOR_MANUAL_SUBMISSION`. There is no harness measurement.

Reviewer prompt: `docs/REVIEW_PROTOCOL.md`.
