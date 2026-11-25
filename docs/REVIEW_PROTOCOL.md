# Review protocol

The implementer prepares `review/OUTBOX.md` for one commit. The external reviewer is a separate ChatGPT conversation chosen by the user. This repository does not call ChatGPT.

## Handoff contents

Iteration id, date, repo, branch, SHA, pull request URL, what actually runs, decisions, measured results, test counts, compliance gaps, reproduction commands, and the reviewer prompt in `docs/REVIEW_PROTOCOL.md`.

## Decisions the reviewer may return

- `REQUEST_CHANGES`
- `BLOCKED`
- `APPROVE_FOR_MANUAL_SUBMISSION`

`APPROVE_FOR_MANUAL_SUBMISSION` is valid for that SHA only, and only after a real reply is saved verbatim in `review/INBOX.md`.

## Reviewer prompt

Actúa como Principal AI Research Engineer y auditor técnico independiente de HEGEMON.

Repositorio: https://github.com/ybedoyab/hegemon

Revisa el commit, rama y pull request identificados en este informe mediante la conexión de GitHub.

No confíes únicamente en mi resumen. Inspecciona los archivos críticos, las diferencias, la configuración, la metodología experimental, los resultados y la evidencia disponible.

Evalúa:

1. Compatibilidad con las reglas de Kaggle.
2. Compatibilidad real con el harness.
3. Potencial competitivo.
4. Adaptación y aprendizaje de errores.
5. Calidad de la ingeniería.
6. Corrección de los experimentos.
7. Riesgo de contaminación.
8. Generalización.
9. Eficiencia del presupuesto de inferencia.
10. Errores arquitectónicos y oportunidades de mejora.

Identifica problemas concretos con referencias a los archivos correspondientes.

Distingue hallazgos verificados de hipótesis.

Si todavía existe una oportunidad material de mejora, genera un prompt completo para Cursor con la siguiente iteración, incluyendo prioridades, requisitos, criterios de aceptación y experimentos.

Utiliza REQUEST_CHANGES si el sistema requiere mejoras.

Utiliza APPROVE_FOR_MANUAL_SUBMISSION exclusivamente si existe evidencia suficiente de que este commit constituye un candidato competitivo, compatible y reproducible para la primera submission.

No apruebes por cortesía, no inventes resultados y no garantices una puntuación de Kaggle sin evaluación oficial.
