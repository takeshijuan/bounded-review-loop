# Review Policy

## Contents

- Authorization and scope
- Budget presets
- Risk classification
- Lane selection
- Evidence and triage
- Repair and re-review
- Stop conditions
- Final report

## Authorization and scope

Freeze the artifact before review:

| Artifact | Frozen identity |
| --- | --- |
| PR | repository, PR number, base/head refs and SHAs, changed files |
| Local diff | repository root, base ref when relevant, staged/unstaged/untracked scope |
| Plan | file path, revision or content hash, referenced requirements |

Use `review-only` unless the request clearly authorizes changes. “Review,” “audit,” or “tell me what is wrong” alone does not authorize edits. “Review and fix,” “repair,” or “improve this plan” authorizes the main agent to edit the named scope, but does not authorize commit, push, comment, approve, merge, deploy, publish, or destructive cleanup.

Capture applicable repository instructions and specifications. Record baseline failures before repair and distinguish:

- `pre-existing`: reproducible outside the frozen target or already present at the base.
- `target-related`: introduced by or necessary to evaluate the frozen target.
- `unknown`: attribution cannot be established with available evidence.

Do not charge a repair loop for intake, baseline collection, or the first review.

## Budget presets

The numeric columns are hard ceilings:

| Preset | Distinct reviewer ceiling | Concurrent reviewer ceiling | Repair-loop ceiling | Default use |
| --- | ---: | ---: | ---: | --- |
| economy | 1 | 1 | 1 | Trivial or narrow, low-risk changes; use 0 reviewers when deterministic evidence is sufficient |
| standard | 2 | 2 | 2 | Default for normal PRs, diffs, and plans |
| strict | 3 | 2 | 3 | Explicit strict request or high-risk, broad change |

Do not create duplicate voting lanes. Under `strict`, run at most two reviewers in the first batch and run a third lane only if it covers a distinct unresolved surface. If a lane becomes duplicative or low-signal, stop it.

When the user asks for unlimited review, retain the selected ceiling. A phrase such as “perfectly clean” changes neither the pass gate nor the budget.

## Risk classification

| Risk | Typical signals | Policy |
| --- | --- | --- |
| Low | Documentation, localized plan wording, isolated mechanical change with decisive checks | Economy is normally enough |
| Standard | Ordinary behavior change with bounded blast radius and relevant tests | Standard by default |
| High | Authentication, authorization, cryptography, payments, migrations, data loss, concurrency, public API, release, or irreversible action | Use applicable strict lanes; consider Sol only under model-routing policy |

Raise risk when evidence shows a wider blast radius. Do not lower high risk merely because the diff is short.

## Lane selection

Select the smallest set that covers the risk:

| Target | Primary lane | Add only when applicable |
| --- | --- | --- |
| Small PR/diff | Consolidated correctness, regression, and tests | Security/data/API when the surface contains those risks |
| Normal PR/diff | Correctness/regression/tests | Security/reliability/data risk |
| Large architecture | Correctness/regression/tests | Security/data, then architecture/maintainability if distinct |
| Plan | Feasibility/dependencies/sequencing | Acceptance/verification/rollback/risk |

Reviewer packets contain only the frozen scope, raw relevant artifact, applicable requirements, baseline evidence, assigned lens, and output schema. Do not include the desired answer, prior reviewer conclusions, or the long originating transcript.

Reviewers must not edit files, stage changes, write comments, or perform external mutations. Only the main/fixer agent may edit and synthesize.

## Evidence and triage

Use this finding shape:

```text
id:
lane:
classification: blocking | advisory
location:
failure_mode:
evidence:
smallest_remediation:
confidence:
```

A blocking finding requires concrete evidence such as a tight file/line location, a failing command, a violated requirement, or reproducible reasoning. Classify as blocking only for:

- verified correctness or security defects
- data-loss or material regression risk
- broken stated requirement or public compatibility contract
- an executable-plan contradiction
- a missing prerequisite that prevents execution
- a required acceptance gate that cannot be verified
- missing rollback for a material irreversible action

Classify naming, style, optional refactoring, equally valid design alternatives, speculative hardening, and editorial taste as advisory. Downgrade unsupported blocker claims to advisory or reject them.

Deduplicate by failure mode and affected contract, not wording. Preserve the strongest evidence and smallest complete remediation. Resolve conflicts with deterministic evidence first. Escalate model strength only if a material uncertainty remains.

## Repair and re-review

For each authorized repair loop:

1. Order verified blockers by dependency.
2. Apply the smallest complete fix centrally.
3. Run affected deterministic checks.
4. Re-review repaired files, unresolved finding IDs, and directly affected contracts.
5. Re-triage with new evidence.

A fix is systemic when it changes a shared abstraction, schema, migration, public contract, authorization boundary, or cross-cutting behavior beyond the original reviewed surface. Only then repeat the full applicable review. Do not restart all lanes for a localized fix.

Advisory-only results consume no repair loop. If consecutive re-reviews produce no new evidence, stop early.

## Stop conditions

Stop and report when any condition holds:

- required runnable checks pass and no verified blocker remains
- only advisory findings remain
- review-only authority would be exceeded
- the repair-loop ceiling is reached
- a required check cannot run and blocks the gate
- the fix needs broader, destructive, irreversible, or external authority
- another review pass adds no evidence

At the loop ceiling, return the unresolved blocker with evidence and a next action. Never weaken the blocker or silently increase the budget.

## Final report

Use a compact evidence bundle:

```text
Target:
Authorization:
Risk / budget:
Review lanes and actual models:
Repair loops used:
Blockers fixed:
Unresolved blockers:
Advisories left:
Edits:
Checks:
Coverage limitations:

Local verification: passed | failed | partial | not run
Review-clean: yes | no | indeterminate
PR/CI: green | failing | pending | not applicable | not checked
Committed: yes | no | not applicable
Merged: yes | no | not applicable | not checked
Deployed: yes | no | not applicable | not checked
Production-verified: yes | no | not applicable | not checked
Next action:
```

Do not collapse these status lines. Report unknown or unobserved remote state as not checked, not as success.
