# Review Policy

Use this reference when scope, risk, or classification needs more detail. The entrypoint owns the mode rules, numeric budgets, and completion gate.

## Scope and evidence

Freeze the repository and artifact identity: PR base/head SHAs and changed files, local diff baseline including selected untracked files, or plan path and content revision. Read applicable AGENTS.md/CLAUDE.md and relevant requirements. Existing authorization from the conversation continues to apply; request more only when the credible fix exceeds it.

Distinguish failures as pre-existing (also present at the base), target-related (introduced by or necessary to evaluate the selected change), or unknown (attribution unproven). Avoid flagging intentional changes, issues silenced by an applicable documented exception, and style preferences as regressions. Surrounding code is evidence even when the final finding points to a changed line.

## Risk and perspectives

Authentication, authorization, cryptography, payments, migrations, data loss, concurrency, public API compatibility, releases, and irreversible actions warrant closer attention. A short diff can still be high risk.

Choose only perspectives that add distinct evidence:

- Small change: consolidated correctness/regression review, or no delegated review when decisive checks suffice.
- Ordinary PR/diff: correctness and tests; add security, data, or API review when applicable.
- Broad systemic change: architecture only when it resolves a distinct uncertainty within the existing budget.
- Plan: feasibility and dependencies; acceptance, verification, and rollback where relevant.

Avoid duplicate voting lanes. Resolve disagreement through concrete evidence; do not add calls beyond the total ceiling to manufacture agreement.

## Findings and repair

Use location, blocking/advisory classification, failure mode, evidence, and smallest remediation. IDs help when findings must be carried into a later fix-only run. Require evidence for correctness/security defects, data loss, material regressions, broken requirements, execution-blocking prerequisites, unobservable required acceptance gates, or missing controls for a material irreversible step.

Naming, optional refactors, prose taste, and equally valid alternatives are advisory. Unsupported speculation is not a verified blocker. Advisory findings do not trigger repairs unless the user separately selects that change as a new task.

Reviewers remain read-only; the main agent owns repair and synthesis. Re-run affected checks and target verification to repaired files, unresolved findings, and directly affected contracts. Full re-review is warranted only when a fix changes a shared abstraction, schema, public contract, or authorization boundary beyond the original surface, and remains subject to the same call and loop ceilings.

When the call budget is exhausted, main-agent verification may finish an in-scope repair, but cannot stand in for an explicitly required independent review. Report the missing gate. At the repair-loop ceiling, report remaining blockers without extending the budget or weakening the gate.
