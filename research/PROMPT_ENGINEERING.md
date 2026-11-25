# Prompt engineering

The shipped prompt is `submission/prompts/system.md`, rendered from `submission/prompts/parts/`. A change to a part is an experiment only after `python -m pytest -q` and, once the harness exists, a paired eval.

## Why it is short

Public harness notes say the context window is 32768 and that compaction does not fire inside one task. A long system prompt plus full-file reads will end the task before a patch exists.

## Gemma-specific choices, unmeasured

- Temperature 0.2 matches the starter digest.
- `max_output_tokens` 4096 instead of 16384, to shorten each turn.
- `thinking_level: LOW`, budget 1024, `include_thoughts: false`. Thoughts that are echoed into the next turn would burn the window. This may also reduce repair quality. It is a hypothesis.
- The prompt says "one tool, then stop" because truncated tool calls are a known Gemma failure mode in the digest.
- No few-shot patch from a real issue. That would be a contamination risk.

## Variants not yet run

Minimal, evidence-first, tool-demo, reflection-heavy, and GEPA-mutated. The mutation helper exists. None have a solve rate.
