# CLAUDE.md — belpho.org rebuild

## Budget discipline

BUDGET: $400 for all remaining work on this project. Report spend at each
phase boundary. If a phase looks like it will breach the ceiling, stop and
tell me rather than continuing.

CONTEXT COST IS THE DOMINANT COST. Opus cache reads are ~60-70% of spend
(1.5B cache-read vs 7.0M output). Therefore:
- Work one phase per session. Start each from RESUME.md, finish it, update
  RESUME.md, and tell me to /clear before the next phase.
- Never poll for status. Use a watcher and report only on state change,
  completion, or a genuine problem.
- Cap any subagent at ~150 tool uses. Split longer jobs into scoped agents
  that hand off in writing. Cost grows quadratically with tool uses inside
  one agent.

MODEL TIERING:
- Opus only for diagnosis, verification design, and judging content loss.
- Sonnet/Haiku for mechanical work: measuring, rendering, running tests,
  applying known edits, tagging, site templating.

WORKFLOWS ARE OPT-IN. Ultracode is off. Do not use the Workflow tool unless
I ask. Default to a single agent, or solo.

VERIFICATION, SCALED TO RISK:
- Multi-agent adversarial verification ONLY for suspected content loss
  (missing figure content, dropped prose, wrong equations) and for the final
  deploy gate. It earned its cost catching the missing N-arrow; it is waste
  on cosmetic findings.
- One fix round per defect. Report the residue honestly instead of iterating
  to zero.

QUALITY IS NOT NEGOTIABLE ON: no missing problems, no missing figures, no
wrong equations, no fabricated content. Cheaper method, same standard. If a
cost rule would compromise one of these, say so and ask.
