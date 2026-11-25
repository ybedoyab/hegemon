## Constraints

- Do not edit `pytest.ini`, `conftest.py`, or files under a tests directory.
- Do not add a dependency and do not use the network.
- Do not print large file bodies back into the conversation. Quote only the lines you will replace.
- Do not keep a hypothesis after `state_update.py` marks it rejected unless new evidence arrives.
- Do not spend the remaining calls on a third rewrite. Submit the best diff that `diff_guard.py` accepts.
- Output of internal decisions stays in the tool arguments. The user-facing text, when you write any, is one sentence.
