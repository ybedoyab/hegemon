# AGENTS.md

Resume contract for every session. Conversation memory is not authoritative.

## Read first

1. `AGENTS.md`
2. `docs/PROJECT_STATE.md`
3. Newest result under `experiments/`
4. `review/INBOX.md` and `review/REVIEW_STATE.json`
5. `git status` and `git rev-parse HEAD`

Then continue the first open item in `docs/BACKLOG.md`.

## What this project is

HEGEMON competes in Kaggle `gemma-4-developer-agent`. The submission is a declarative ADK agent plus skill scripts. The user uploads it. This agent does not submit to Kaggle.

## Non-negotiable rules

- Do not invent solve rates, citations, logs, or reviewer approvals.
- Do not give the solving agent reference patches or hidden tests.
- Keep cross-task evaluation memory and online weight updates disabled.
- Unknown harness features stay out of `submission/` until `docs/COMPETITION_CONTRACT.md` marks them verified.
- Skill scratch files go to `/tmp/hegemon`, not the repo.
- Official rules override this file.

## Commands

`PYTHONPATH=src`, then `python -m pytest -q`, `python scripts/run_localization_probe.py`, `python -m hegemon pack`.

## Promotion

A challenger replaces the champion only after a measured comparison on the same tasks. Synthetic top-1 recall is not that comparison.
