# Validation report

Date: 2026-11-25

Command: `python -m hegemon pack` with `PYTHONPATH=src`.

| Check | Result |
| --- | --- |
| Zip path | `dist/submission.zip` |
| Bytes | 12425 |
| SHA-256 | `6aef0dcb24d01a3e96aef5d56795c46e821ff88722b3abcdfa0bb276e017f5bd` |
| Entries | 10 |
| `agent.yaml` at archive root | yes |
| Path traversal | none found by `verify_zip` |
| Symlinks | none found |
| Duplicate names | none found |
| Official Kaggle validator | NOT_RUN |

This checksum matches the tree at pack time. Rebuild after any edit under `submission/` and do not trust this file if the hash differs.

Unit tests at pack time: 17 passed. Official harness: NOT_RUN.
