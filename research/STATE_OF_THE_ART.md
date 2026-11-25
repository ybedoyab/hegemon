# State of the art, applied to this harness

These are engineering judgments about papers and systems the user named. They are not experimental results from this repository. Papers were not re-downloaded today.

| Work | Why it matters here | What we can actually run |
| --- | --- | --- |
| Agentless (arXiv:2407.01489) | Localize, then patch, then test. Fewer agent turns. | The skill's localize-read-edit-test-submit loop is this shape. |
| SWE-agent / mini-swe-agent | Tight shell interface and history control. | Our interface is the harness tool list, not their ACI. |
| OpenHands | General coding agent with a heavy runtime. | The scored runtime cannot import it. |
| SWE-bench | Pass/fail after applying a hidden test patch. | Same scoring story. We have not run SWE-bench. |
| Reflexion (arXiv:2303.11366) | Verbal reflection between trials. | `state_update.py` stores a short failure and rejects a repeated edit. It does not ask the model for a long reflection. |
| GEPA (arXiv:2507.19457) | Reflective prompt evolution offline. | `promote()` refuses an unmeasured mutation. The reflection LLM step is `NOT_RUN`. |
| DSPy / MIPRO | Compiled prompts. | Not in the zip. Adding DSPy to Kaggle would violate the declarative submission. |
| Self-Refine, Self-Debugging, ReAct | Generate, critique, act. | One tool per turn is the ReAct constraint we tell the model to follow. |
| LoRA / QLoRA / DPO / GRPO | Adaptation. | No training run. Shipping an untrained adapter is forbidden by our own policy. |

Highest expected value while the harness is blocked: make the first localization call accurate and the patch small. Learned routers and GRPO wait until trajectories exist.

Generalization risk: the public 129 tasks are from four libraries. Hidden tasks are described as private repositories. Prompts must not name fastapi, rich, requests, or httpx as special cases. The current prompt does not.
