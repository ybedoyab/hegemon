# Experiment registry

| ID | Question | Dataset | Status | Result |
| --- | --- | --- | --- | --- |
| E_LOC001 | Does lexical ranking put the intended file first on two synthetic repos? | `tests/fixtures` | MEASURED | top-1 2/2, recall 1.0. See `experiments/E_LOC001.json`. |
| E000 | Official starter solve rate | official dev set | NOT_RUN | Dataset and model absent |
| E001 | Compact ReAct prompt | official dev set | NOT_RUN | |
| E002 | This structured skill policy | official dev set | NOT_RUN | Champion candidate, unmeasured |
| E003–E016 | Graph localization, context, reproduction routing, reflection, budget, multi-candidate, verifier, recovery, prompt evolution, learned routing, combined champion, inference, LoRA, submission candidate | official dev set | NOT_RUN | Do not mark these done by writing code |

`experiments/registry.jsonl` stores the machine-readable copy of measured rows.

Synthetic recall is not a Kaggle score and is not comparable to SWE-bench.
