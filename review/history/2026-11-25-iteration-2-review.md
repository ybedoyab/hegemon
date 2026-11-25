# **HEGEMON — Revisión de la iteración 2**

REQUEST_CHANGES

**Commit evaluado:** `7dfcd784de8fcac408e4738f882f00905c0b0789`

Esta iteración resuelve el bloqueo administrativo más urgente: según la evidencia de Cursor, ya estamos inscritos, hemos aceptado las reglas y tenemos acceso autenticado a los recursos oficiales de Kaggle.

Ahora debemos concentrar prácticamente todo el esfuerzo en conseguir rendimiento medible.

## **1. Evaluación del progreso**

| Componente                 | Iteración 1   | Iteración 2                        |
| -------------------------- | ------------- | ---------------------------------- |
| Inscripción Kaggle         | Desconocida   | Confirmada por Cursor              |
| Autenticación CLI          | Bloqueada     | Resuelta                           |
| Documentación oficial      | No disponible | Descargada                         |
| Tareas de desarrollo       | 0             | 129 registros                      |
| Configuración YAML         | Especulativa  | Contrastada con el ejemplo oficial |
| Tests unitarios            | 17            | 18                                 |
| Inferencia real            | No            | No                                 |
| Solve rate                 | N/D           | N/D                                |
| Validación oficial         | No            | No                                 |
| Autoevolución demostrada   | No            | No                                 |
| Automatización de revisión | Pendiente     | Pendiente                          |

Intenté acceder directamente a los tres archivos YAML del nuevo commit. La conexión de GitHub sigue devolviendo un error 404. Por tanto, mi revisión se basa en el informe proporcionado por Cursor, no en una auditoría independiente del código fuente.

## **2. Problemas que debemos resolver**

| Prioridad | Hallazgo                                                                         |
| --------- | -------------------------------------------------------------------------------- |
| P0        | Conseguir inferencia real con un modelo Gemma permitido.                         |
| P0        | Ejecutar el validador oficial.                                                   |
| P0        | Reproducir el baseline sobre las tareas descargadas.                             |
| P0        | Aislar completamente los parches de referencia del agente.                       |
| P1        | Revisar si 24 llamadas a herramientas son suficientes.                           |
| P1        | Evaluar el presupuesto de razonamiento de 4096 tokens.                           |
| P1        | Sustituir la adaptación elemental por decisiones dinámicas basadas en evidencia. |
| P1        | Medir el impacto de distintas estrategias de reparación.                         |
| P2        | Ejecutar un ciclo completo de autoevolución.                                     |

Los valores de `max_tool_calls`, `thinking_budget`, `max_turns` y `max_output_tokens` son especialmente importantes. Que una configuración coincida con el ejemplo oficial no significa que sea óptima para competir.

**En la tercera iteración no quiero más infraestructura sin resultados.** Quiero que Cursor ejecute el primer experimento real de reparación de software y, a partir de ahí, comience a optimizar.

## **3. Nueva evidencia sobre nuestros competidores**

Encontré un dato que debemos tomar como referencia técnica. El repositorio público [happyc0der/gemma-swe-agent](https://github.com/happyc0der/gemma-swe-agent?utm_source=chatgpt.com) documenta experimentos con el harness y reporta **13 problemas resueltos de 33**, aproximadamente un 39,4 % en su conjunto de desarrollo. Es un resultado autodeclarado, no una puntuación oficial de Kaggle.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub



Por otra parte, el [notebook oficial de Kaggle](https://www.kaggle.com/code/ryanholbrook/getting-started-gemma-4-developer-agent?utm_source=chatgpt.com) muestra ejecuciones con GPU L4 × 4. La CLI oficial permite desplegar notebooks privados, seleccionar aceleradores, consultar su estado y descargar automáticamente los resultados.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub+2



Por tanto, **no necesitamos descargar los 22 GB completos en tu computador ni ejecutar Gemma 31B en tu RTX 3050 Ti**. Debemos trasladar el ciclo experimental a Kaggle y utilizar Cursor como orquestador.

## **4. Prompt para Cursor — Iteración 3**

# HEGEMON — ITERATION 3: REAL GEMMA INFERENCE AND COMPETITIVE EXPERIMENTATION

## 0. EXTERNAL REVIEW DECISION

Decision: REQUEST_CHANGES

Reviewed commit: 7dfcd784de8fcac408e4738f882f00905c0b0789

Repository: [https://github.com/ybedoyab/hegemon](https://github.com/ybedoyab/hegemon)

Branch: feat/hegemon-core

PR: [https://github.com/ybedoyab/hegemon/pull/1](https://github.com/ybedoyab/hegemon/pull/1)

Iteration 2 successfully resolved registration, authentication and initial configuration discovery.

However, HEGEMON remains an unmeasured software repair agent.

The independent reviewer could not access the private repository: GitHub returned HTTP 404 when fetching the three submission YAML files at the reviewed commit.

No approval is granted.

The next iteration must focus on real Gemma inference and measured performance, not additional speculative infrastructure.

All previous mission requirements remain applicable.

Target: reach or exceed 0.24 in the first official Kaggle submission and ultimately compete for first place.

---

## 1. NON-NEGOTIABLE PRIORITIES

Execute in this order:

1. Establish GPU execution on Kaggle.
2. Execute the official validator.
3. Reproduce the official baseline.
4. Execute HEGEMON on the same real tasks.
5. Analyze actual failures.
6. Optimize repair strategies.
7. Optimize inference budgets.
8. Implement measured reflective evolution.
9. Push evidence to GitHub.
10. Request independent review.
11. Continue improving.

Do not spend another iteration exclusively on documentation, mock tests or configuration files.

Do not ask the user to manually create a Kaggle notebook when this can be accomplished through the authenticated official CLI.

Do not automatically submit anything to the competition leaderboard.

Private development notebook execution is authorized.

---

## 2. P0 — KAGGLE GPU EXECUTION

The local 4 GB RTX 3050 Ti is unsuitable for the full 31B model.

Do not attempt to solve this by downloading a 31B checkpoint locally.

Use the existing authenticated Kaggle account.

Official resources:

[https://www.kaggle.com/code/ryanholbrook/getting-started-gemma-4-developer-agent](https://www.kaggle.com/code/ryanholbrook/getting-started-gemma-4-developer-agent)

[https://github.com/Kaggle/kaggle-cli/blob/main/docs/kernels.md](https://github.com/Kaggle/kaggle-cli/blob/main/docs/kernels.md)

[https://github.com/Kaggle/kaggle-cli/blob/main/docs/kernels_metadata.md](https://github.com/Kaggle/kaggle-cli/blob/main/docs/kernels_metadata.md)

[https://github.com/Kaggle/kaggle-cli/blob/main/skills/references/kernels.md](https://github.com/Kaggle/kaggle-cli/blob/main/skills/references/kernels.md)

Inspect the installed CLI:

```
kaggle kernels --help
kaggle kernels pull --help
kaggle kernels push --help
kaggle kernels status --help
kaggle kernels output --help
kaggle kernels logs --help
```

Use the exact supported syntax.

Retrieve the official starter notebook and its metadata.

Investigate the accelerator configuration used by the official notebook.

Do not assume a particular accelerator identifier maps to four L4 GPUs without verifying the actual allocation.

Inspect:

- Available accelerators.
- Existing GPU quota.
- Quota charging rate.
- Competition-specific GPU entitlement.
- Notebook execution limits.
- Offline mode requirements.
- Available model attachments.
- Competition data attachments.
- Disk space in the Kaggle environment.

Create a private development notebook:

```
ybedoyab/hegemon-dev-eval
```

Use a notebook configuration derived from the official starter.

Preserve required competition_sources, model_sources, dataset_sources and kernel_sources from the official metadata where applicable.

Set notebook privacy to private.

Disable internet when required.

Attach the competition data directly.

Do not download the entire 22 GB competition dataset to the local Windows computer merely to duplicate files already available inside Kaggle.

Implement the supported equivalent of:

```
kaggle kernels push -p <notebook-directory> --accelerator <verified-accelerator>
kaggle kernels status ybedoyab/hegemon-dev-eval
kaggle kernels logs ybedoyab/hegemon-dev-eval
kaggle kernels output ybedoyab/hegemon-dev-eval -p <output-directory>
```

Use bounded polling and appropriate retry intervals.

Capture the exact notebook version.

Keep the notebook private throughout development.

Before launching long runs, verify remaining GPU quota and expected resource consumption.

Do not purchase compute.

Do not automatically activate paid accelerator services.

---

## 3. P0 — OFFICIAL VALIDATOR

The current ZIP has only been validated by the project's own packer.

Execute the validator from the official starter notebook or harness.

Verify:

- Agent YAML schema.
- Evaluation configuration schema.
- Sampling configuration schema.
- Skill discovery.
- Skill script execution.
- Tool availability.
- Exact tool signatures.
- Model identifier.
- Archive structure.
- Model loading.
- Agent initialization.
- Runtime permissions.
- Sandbox behavior.

Record actual validation output.

Investigate whether the sample configuration is merely illustrative or reflects mandatory constraints.

Do not label the package officially valid until the actual validator succeeds.

Create:

```
reports/OFFICIAL_VALIDATION.md
```

Include the notebook version, commit SHA, exact package hash and original validator output.

---

## 4. P0 — DATASET AUDIT AND ORACLE ISOLATION

The official tasks.jsonl contains 129 public development records.

Perform dataset analysis locally without exposing reference answers to the solving agent.

Verify:

- Unique task count.
- Repository distribution.
- Task completeness.
- Available graph and embedding resources.
- Base commit availability.
- Test environment availability.
- Duplicate tasks.
- Missing or empty graph files.

Public sources suggest that the development data may contain approximately:

- FastAPI: 67 tasks.
- Rich: 48 tasks.
- Requests: 13 tasks.
- HTTPX: 1 task.

Verify these numbers directly.

Treat the dataset as highly imbalanced.

Create a sanitized task manifest containing only permitted fields.

Maintain a strict boundary between:

SOLVER:

- Problem statement.
- Allowed repository state.
- Allowed tools.
- Allowed graph information.
- Other explicitly permitted task inputs.

EVALUATOR:

- Reference patch.
- Test patch.
- Evaluation-only metadata.
- Official verification results.

The solver must not be able to read evaluator-only material through filesystem exploration, skill scripts, prompts, logs or environment variables.

Ensure that reference test patches are never applied before the solver executes unless the official harness explicitly requires it.

Do not inspect evaluator-only files from inside the solving process.

Add automated negative tests demonstrating that the agent cannot access prohibited fields.

Use a separate sanitized manifest for any model-facing operation.

---

## 5. DEVELOPMENT SPLIT STRATEGY

Define the evaluation methodology before examining comparative results.

Recommended initial partition:

- Smoke set: 4 tasks.
- Fast iteration set: 16 tasks.
- Optimization set: 60 tasks.
- Validation set: 24 tasks.
- Frozen holdout: 25 tasks.

Total: 129 tasks.

Adjust the split if task availability or official constraints require it.

Keep these sets disjoint.

Stratify by repository and legitimate pre-solution task characteristics.

Do not select validation tasks because the current agent happens to solve them.

Do not select tasks based on the content of the reference patch.

Because HTTPX may contain only one development task, document how its split assignment is handled.

Run additional repository-disjoint experiments where feasible.

The frozen holdout must not drive routine prompt mutations.

Freeze task identifiers and manifest hashes before experiments.

Record the split-generation seed.

---

## 6. P0 — FIRST REAL INFERENCE

Execute the official starter agent on at least one development task immediately after establishing GPU access.

A successful real run must demonstrate:

1. Actual Gemma checkpoint loaded.
2. Actual inference requests.
3. Valid tool calls.
4. Repository exploration.
5. Patch generation or documented repair failure.
6. Official verification.
7. Recorded runtime.
8. Recorded resource usage.

A failed repair still counts as useful experimental evidence if the runtime worked correctly.

Do not confuse successful inference with successful repair.

Preserve the full permitted trajectory locally.

Then execute HEGEMON on the same task.

Do not change the model, task or evaluation budget between these two comparisons.

Once the first smoke test works, expand to all four smoke tasks.

---

## 7. P0 — BASELINE COMPARISON

Establish three configurations:

B0 — Official starter.

B1 — HEGEMON Iteration 2, unchanged.

B2 — HEGEMON adaptive challenger.

Run B0 and B1 before modifying the champion.

Use:

- Identical development tasks.
- Identical checkpoint revisions.
- Identical evaluator versions.
- Comparable hardware.
- Identical generation seeds where supported.
- Comparable budgets.

Record:

- Solved tasks.
- Attempted tasks.
- Runtime failures.
- Invalid patches.
- No-edit failures.
- Timeout failures.
- Tool errors.
- Tokens.
- Inference time.
- Tool time.
- Total wall time.
- VRAM.
- Verification results.

Preserve task-level outcomes.

A configuration must not receive a better score merely because difficult tasks were silently excluded.

Report unavailable or invalid tasks separately.

Generate:

```
reports/BASELINE_COMPARISON.md
experiments/results/b0.jsonl
experiments/results/b1.jsonl
experiments/results/b2.jsonl
```

The baseline comparison must contain genuine harness outcomes.

---

## 8. P1 — AUDIT AND OPTIMIZE THE INFERENCE BUDGET

The current configuration is:

```
timeout_seconds: 120
max_tool_calls: 24
max_time_minutes: 5
max_turns: 40
```

Sampling:

```
max_output_tokens: 16384
thinking_budget: 4096
include_thoughts: false
```

These are unvalidated hyperparameters.

Determine the exact semantics of each field using HARNESS_README.md and the actual implementation.

Verify whether:

- timeout_seconds applies to tool execution or another operation.
- max_time_minutes includes inference, tools or total elapsed time.
- max_tool_calls is enforced globally or per agent.
- max_turns includes tool messages or only model turns.
- thinking_budget is per generation or per task.
- max_output_tokens includes reasoning tokens.

Do not guess.

Evaluate a focused budget matrix using only supported values.

Candidate configurations for investigation:

A — Current efficient configuration.

- 24 tool calls.
- 5-minute task limit.
- 4096 thinking tokens.

B — Balanced configuration.

- Approximately 40–48 tool calls.
- Approximately 8–10 minutes.
- 4096 thinking tokens.

C — Increased reasoning configuration.

- Approximately 40–48 tool calls.
- Approximately 8–10 minutes.
- 8192 thinking tokens, if permitted.

D — Exploration-heavy configuration.

- Larger tool allowance.
- Conservative generation length.
- Explicit evidence-driven stopping rules.

These values are experimental proposals, not verified competition limits.

Adjust them to actual supported ranges and global budget requirements.

Do not execute the entire Cartesian product of hyperparameters.

Use successive halving or another resource-efficient search process.

Measure the expected total solve rate under the official aggregate runtime limit.

Account for:

- Model startup.
- Container initialization.
- Parallelism.
- Repository setup.
- Test execution.
- Tool overhead.
- Generation.
- Worst-case tasks.
- Failed tasks.
- Final serialization.

Do not assume that increasing the per-task timeout is harmless.

Reserve a safety margin against total evaluation timeout.

Produce a runtime simulation using empirical task-duration distributions.

---

## 9. P1 — STUDY COMPETITIVE PUBLIC EVIDENCE

Review:

[https://github.com/happyc0der/gemma-swe-agent](https://github.com/happyc0der/gemma-swe-agent)

[https://github.com/happyc0der/gemma-swe-agent/blob/main/docs/competition.md](https://github.com/happyc0der/gemma-swe-agent/blob/main/docs/competition.md)

[https://github.com/Peoplerepabulic/kaggle-gemma4-developer-agent](https://github.com/Peoplerepabulic/kaggle-gemma4-developer-agent)

[https://github.com/johnsonhk88/kaggle-Google-The-Gemma-4-Developer-Agent-Competition](https://github.com/johnsonhk88/kaggle-Google-The-Gemma-4-Developer-Agent-Competition)

[https://github.com/MadeNavaneeth/Gemma-4-Developer-Agent-Kaggle](https://github.com/MadeNavaneeth/Gemma-4-Developer-Agent-Kaggle)

The happyc0der repository reports a result of 13/33 on a faithful development evaluation.

Treat this as a self-reported external benchmark, not a verified Kaggle leaderboard score.

Investigate its:

- Evaluation methodology.
- Model.
- Tool budgets.
- Prompt architecture.
- Failure patterns.
- Candidate-generation policy.
- No-edit failures.
- Search loops.
- Test execution strategy.
- Regression behavior.

An important reported failure mode is spending too much of the task budget exploring without actually modifying the code.

HEGEMON must explicitly detect and avoid this failure.

Do not optimize against individual task identities or competitor-specific known solutions.

Do not copy competitor code unless licensing and competition rules explicitly permit it.

Extract generalized technical lessons.

Document independently reproduced findings separately from external claims.

---

## 10. P1 — PRODUCTIVE ACTION CONTROLLER

Replace the current simplistic strategy switch with an evidence-driven controller.

Define task phases:

```
UNDERSTAND
LOCALIZE
FORM_HYPOTHESIS
INVESTIGATE
REPAIR
VERIFY
RECOVER
FINALIZE
```

These are logical states, not mandatory sequential steps.

The controller should select the next action according to observed evidence.

Track:

- Remaining budget.
- Relevant symbols discovered.
- Distinct hypotheses.
- Contradictory evidence.
- Repeated file reads.
- Repeated tool calls.
- Whether any meaningful edit exists.
- Whether a candidate is preserved.
- Whether the issue has been reproduced.
- Verification status.

Introduce a no-edit watchdog.

If localization has consumed a significant fraction of the task budget without producing new information:

- Reassess the strongest hypothesis.
- Reduce unnecessary exploration.
- Form a concrete repair plan.
- Execute the best supported repair when evidence is sufficient.

Do not force an arbitrary edit merely to satisfy the watchdog.

Introduce an information-gain mechanism.

Repeated exploration is permitted only if it is expected to produce new relevant evidence.

Distinguish:

- A repeated action with identical inputs and no new evidence.
- A justified revisit after a failed test or updated hypothesis.

The second is legitimate debugging.

Measure:

- Time to first useful edit.
- No-edit failure rate.
- Repeated-tool-call rate.
- Recovery success.
- Solve rate.

---

## 11. P1 — STRATEGY PORTFOLIO

Implement three initial repair strategies:

S1 — Direct localized repair.

Suitable for:

- Clear bugs.
- Strong localization.
- Small behavioral changes.
- Obvious incorrect conditions or transformations.

S2 — Evidence-first investigation.

Suitable for:

- Ambiguous root causes.
- Multiple relevant files.
- Complex invariants.
- Uncertain requirements.

S3 — Reproduction-driven repair.

Suitable for:

- Behavioral bugs.
- Edge cases.
- Failures with reproducible inputs.
- Compatibility issues.

Select the strategy dynamically.

Allow strategy transitions when evidence changes.

Do not introduce three separate heavyweight agents unless measured results justify the extra inference.

A single Gemma instance can implement different cognitive roles through supported prompts, state and skills.

Measure each strategy independently where possible.

Then measure adaptive routing against a fixed strategy.

---

## 12. P1 — PATCH VERIFICATION AND RECOVERY

Implement an evidence-driven verification policy.

A proposed patch should be evaluated using applicable checks:

- Syntax.
- Diff integrity.
- Causal relationship to issue.
- Existing relevant tests.
- Reproduction tests.
- Boundary conditions.
- Compatibility.
- Related callers.
- Unintended behavior changes.

Prefer reproduction tests that fail before repair and pass afterward.

Never include evaluation-only test patches in the solving context.

Do not treat generated tests as an infallible oracle.

If a test fails:

1. Classify the failure.
2. Determine whether the test environment is valid.
3. Determine whether the patch hypothesis was wrong.
4. Update the task state.
5. Choose the highest-value recovery action.

When multiple candidate patches are supported by the harness:

- Preserve the strongest candidate.
- Isolate alternatives.
- Verify candidates under comparable conditions.
- Avoid overwriting a good candidate with a weaker speculative edit.

Measure oracle pass\@k separately from selected-patch accuracy.

The final output is the selected candidate, not the entire candidate portfolio.

---

## 13. P1 — FAILURE TAXONOMY

Classify every unsuccessful development task into one or more categories:

F01 — Incorrect issue interpretation.

F02 — Incorrect file localization.

F03 — Incorrect symbol localization.

F04 — Insufficient context.

F05 — Incorrect root-cause hypothesis.

F06 — Correct hypothesis, incorrect implementation.

F07 — No edit produced.

F08 — Invalid or malformed patch.

F09 — Relevant regression introduced.

F10 — Tool-call failure.

F11 — Sandbox or environment failure.

F12 — Time budget exhausted.

F13 — Token budget exhausted.

F14 — Repetitive exploration.

F15 — Incorrect candidate selection.

F16 — Inadequate verification.

F17 — Premature termination.

F18 — Unsupported harness behavior.

F19 — Unknown or insufficient evidence.

Record the supporting trajectory evidence.

Do not assign failure categories based only on intuition.

Create:

```
reports/FAILURE_TAXONOMY.md
```

Rank failure categories by:

- Frequency.
- Potential recoverability.
- Expected solve-rate impact.
- Cost of mitigation.

Select the next engineering improvement based on measured bottlenecks.

---

## 14. P2 — FIRST REAL SELF-EVOLUTION CYCLE

Implement and execute a complete measured reflective optimization cycle.

Use actual B0/B1/B2 trajectories from the optimization split.

Procedure:

1. Collect verified failures.
2. Select a representative failure category.
3. Extract generalized lessons.
4. Generate two or three targeted prompt or policy mutations.
5. Assign each mutation a unique configuration hash.
6. Evaluate mutations on identical tasks.
7. Compare against the current champion.
8. Reject weaker variants.
9. Promote only evidence-backed improvements.
10. Preserve the experiment lineage.

Example:

If several failures involve repeated exploration without useful edits, mutate only the action-selection and stopping policy.

Do not simultaneously modify unrelated verification, model settings and localization mechanisms in the same ablation.

Measure:

- Solve-rate change.
- No-edit rate change.
- Token consumption.
- Latency.
- Regression impact.

Use GEPA-inspired reflective optimization.

References:

[https://arxiv.org/abs/2507.19457](https://arxiv.org/abs/2507.19457)

[https://github.com/gepa-ai/gepa](https://github.com/gepa-ai/gepa)

[https://github.com/stanfordnlp/dspy](https://github.com/stanfordnlp/dspy)

Do not build a large generic GEPA integration before testing whether a simple reflective mutation process improves this specific agent.

Do not use the frozen holdout for prompt mutation.

If no challenger improves the champion, report the failed evolution cycle honestly.

A failed experiment is acceptable.

A fabricated improvement is not.

---

## 15. P2 — MODEL SELECTION

Start with the currently configured model only after confirming its exact permitted identifier.

Investigate the official model list again.

Evaluate:

- Largest permitted Gemma checkpoint.
- Intermediate checkpoints, if allowed.
- Small models eligible for additional prizes.

Do not switch models merely because the larger checkpoint is difficult to run locally.

Kaggle remote inference is the preferred initial path.

Measure:

- Solve rate.
- Tool reliability.
- Token throughput.
- Runtime.
- Total tasks solvable under aggregate budget.

A smaller model may outperform a larger model under a constrained total runtime.

Treat this as an empirical hypothesis.

Do not begin LoRA training before identifying a concrete, measured model limitation.

---

## 16. EXPERIMENTAL TARGETS

These are internal engineering targets, not verified predictions of leaderboard performance.

Target A:

- Complete the four-task smoke set.
- Demonstrate reliable official runtime execution.
- Produce actual patches.

Target B:

- Complete the 16-task fast iteration set.
- Establish B0/B1/B2 comparisons.
- Identify dominant failure categories.

Target C:

- Achieve meaningful improvement over the official baseline on a broader optimization set.

Target D:

- Demonstrate at least one measured self-evolution cycle.

Target E:

- Achieve a competitive validation result with a runtime budget compatible with the official evaluator.

Use the external self-reported 13/33 result as one contextual research reference.

Aim for 40–50% or higher on an appropriately constructed development evaluation if feasible, while acknowledging dataset composition, sample size and differences in difficulty.

Do not translate a 40% development score into a guaranteed public leaderboard score.

Do not lower evaluation standards to reach a numerical target.

---

## 17. AUTOMATED KAGGLE EXPERIMENT LOOP

Implement the missing operational automation.

The orchestrator should:

1. Build a candidate package.
2. Validate it locally.
3. Compute its SHA-256 hash.
4. Prepare a private development notebook.
5. Embed or attach the authorized package.
6. Launch the notebook using the official Kaggle CLI.
7. Record the notebook version.
8. Poll execution status.
9. Retrieve logs and permitted output artifacts.
10. Parse task-level results.
11. Classify failures.
12. Update the experiment registry.
13. Compare against the champion.
14. Generate the next experimental intervention.
15. Invoke the supported Cursor Agent CLI or continue the active Agent session.
16. Repeat.

Persist resumable state.

Prevent duplicate GPU runs.

Cache completed experiments using:

- Candidate hash.
- Dataset manifest hash.
- Model revision.
- Sampling configuration.
- Evaluation configuration.
- Harness version.

Do not launch identical experiments repeatedly unless replication is intentional.

Ensure notebook outputs can be associated with the exact candidate package.

Do not confuse results from different notebook versions.

Add quota-aware scheduling.

Do not automatically submit to the competition.

---

## 18. EXTERNAL REVIEW ACCESS

The GitHub reviewer still receives HTTP 404.

Investigate the precise reason.

The repository was previously accessible before becoming private.

Likely causes include GitHub App repository selection or changed installation access, but verify rather than assume.

Keep the repository private.

Use the existing authorized GitHub account and inspect the relevant application configuration.

If the application requires explicit user consent to access HEGEMON, open the exact authorization page.

Do not grant access to unrelated repositories.

Do not make the repository public.

Meanwhile, produce a sanitized review bundle containing:

- Exact YAML configurations.
- Relevant skill scripts.
- Agent instructions.
- Evaluation methodology.
- Experiment summaries.
- Validator results.
- CI results.
- Candidate hashes.
- Changed-file inventory.
- Selected source diffs.
- Known limitations.

Do not include restricted datasets or credentials.

If an approved independent reviewer API is available, use it to automate the review process.

Do not extract responses automatically from the ChatGPT consumer web interface.

Do not falsely claim that an API review came from the existing ChatGPT conversation.

Do not stop independent experiments solely because the external GitHub connection is unavailable.

---

## 19. CONTINUOUS AUTONOMY

The user wants minimum manual intervention.

Use the prior orchestration requirements.

Continue automatically through successive research and development cycles while:

- Authorized compute is available.
- Experiments remain useful.
- Competition rules are respected.
- No required human authorization blocks the action.

Do not send a report after every trivial code change and terminate the entire workflow.

Generate external review checkpoints after meaningful experimental results.

Where an authorized reviewer API is unavailable, preserve the review request and continue independent engineering work that does not require approval.

Do not simulate external approval.

Do not create hidden persistence mechanisms.

Maintain explicit resource limits, resumability and a stop mechanism.

---

## 20. ITERATION 3 REQUIRED DELIVERABLES

Push the next verified checkpoint to feat/hegemon-core or an appropriately related experimental branch.

Update PR #1.

Required artifacts:

```
reports/OFFICIAL_VALIDATION.md
reports/BASELINE_COMPARISON.md
reports/FAILURE_TAXONOMY.md
reports/BUDGET_ANALYSIS.md
reports/EVOLUTION_RESULTS.md
experiments/manifest.json
experiments/results/
notebooks/
automation/
review/OUTBOX.md
```

The exact structure may change if required by the implementation.

Every report must contain actual evidence or clearly labeled NOT_RUN status.

Include:

- Commit SHA.
- Notebook URL and version.
- Exact package checksum.
- Official validator result.
- Model identifier.
- GPU allocation.
- Actual development tasks attempted.
- Actual tasks solved.
- Baseline comparison.
- Failure categories.
- Runtime measurements.
- Remaining GPU quota where available.
- Self-evolution outcome.
- Next highest-value intervention.

---

## 21. REVIEW GATES

Do not request approval for manual submission unless:

- Official validation passes.
- Real Gemma inference works.
- Official development task evaluation works.
- Baseline comparison exists.
- Adaptive improvements have been tested.
- Resource usage is compatible.
- Data isolation is demonstrated.
- At least one reflective evolution cycle has been executed.
- The release archive corresponds exactly to the reviewed commit.

External review decision remains REQUEST_CHANGES.

No leaderboard result exists.

Do not submit to Kaggle.

---

## 22. START IMMEDIATELY

Your first action should be establishing the private Kaggle notebook using the already authenticated account and official starter.

Do not reply with a speculative implementation plan.

Launch real computation.

Retrieve actual results.

Analyze failures.

Improve HEGEMON.

Repeat.

Push the evidence.

Request the next independent review.

The objective is not a larger repository or more passing unit tests.

The objective is more verified software repairs under the competition's actual constraints.

Proceed autonomously.

## **5. Objetivos de rendimiento para la siguiente fase**

Objetivo primera submission oficial

**24%**

Referencia externa de desarrollo — 13/33

**39.4%**

Meta interna de desarrollo

**50%**

Meta interna ambiciosa

**60%**

El leaderboard y los conjuntos de desarrollo no son directamente comparables. Estas cifras son referencias y objetivos, no resultados obtenidos por HEGEMON.

**No entrenaría LoRA todavía.** Primero debemos descubrir si nuestro principal cuello de botella es la capacidad de razonamiento de Gemma, la localización, la verificación o el presupuesto de inferencia. Esa decisión debe salir de los experimentos, no de nuestras suposiciones arquitectónicas.
