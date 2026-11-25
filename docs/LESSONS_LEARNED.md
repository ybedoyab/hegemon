# Lessons learned

## 2026-11-25

- The live Kaggle competition pages did not render (`Too many requests` inside the site's app bundle). The Kaggle competitions API returned HTTP 401 without credentials. Facts taken from blogs and public GitHub notes stay `UNKNOWN` until `HARNESS_README.md` is local.
- This GPU has 4 GB of VRAM. A 31B QAT checkpoint of about 17 GB, as described in the public harness digest, will not load here. Model comparisons require Kaggle's L4x4 notebook or another machine.
- C: had about 1.1 GB free during discovery. Dependency caches belong on D:.
- The starter's one-minute and ten-call budget is a plausible reason early leaderboards sat near zero. That is a hypothesis from a 2026-09-24 digest, not a measurement we ran.
- Public reports of a 0.24 or 0.29 leaderboard are other people's claims. This project has no submission.
- Skill scripts that write into the workspace would be graded as part of the patch. State lives under the state directory.
- `import` of `common` is cached in one process, so path configuration must be read when a function runs, not only at import.
