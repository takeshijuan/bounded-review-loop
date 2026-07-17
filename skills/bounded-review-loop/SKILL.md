---
name: bounded-review-loop
description: Run budget-controlled, evidence-based review and optional repair for pull requests, branches or working-tree diffs, and implementation plan files. Use when asked for multi-angle review, review and fix, repeated review until clean, economy/standard/strict review, or review-only without edits. Keep review fanout and repair loops bounded, route only to models exposed by the live runtime, distinguish blockers from advisory suggestions, re-review targeted surfaces, and report local verification separately from CI, merge, deployment, and production state. Do not use this skill to merge, deploy, publish, approve, or destructively clean up unless those actions are separately authorized.
---

# Bounded Review Loop

Replace open-ended “review until clean” behavior with a finite evidence gate. Treat clean as: required deterministic checks pass and no verified blocking findings remain. Advisory suggestions may remain.

## Load the applicable policy

- Always read [Review policy](references/review-policy.md) and [Model routing](references/model-routing.md).
- For a pull request, also read [PR review](references/pr-review.md).
- For a plan file, also read [Plan review](references/plan-review.md).
- For a local branch or working-tree diff, use the core policy and repository-local instructions.

## Run the state machine

### 1. Resolve target and authority

Classify the artifact as `pr`, `local-diff`, or `plan`. Resolve the repository, applicable instructions/specs, base and head or diff snapshot, target plan revision, and practical verification commands.

Classify authorization:

- `review-only`: inspect and report; do not edit. Use this when the user explicitly forbids edits or when edit authority is unclear.
- `review-and-fix`: edit only when the user explicitly asks to fix, repair, improve, or repeat review and repair.

Review-and-fix authority does not authorize comments, commits, pushes, approvals, merges, deployments, publication, or destructive cleanup.

### 2. Freeze a baseline

Capture the initial changed surface and run relevant deterministic checks before model review when practical. Record pre-existing failures separately from failures attributable to the target. Do not silently expand the review scope.

### 3. Classify risk and budget

Default to `standard`. An unqualified “until clean,” “keep going,” or “as many as needed” request does not remove the limits or select `strict`.

- `economy`: use no subagent for a trivial deterministic check or at most one routine reviewer; allow at most one repair loop.
- `standard`: use at most two reviewers and two repair loops.
- `strict`: use at most three distinct review lanes, never more than two concurrently, and three repair loops.

Treat authentication, authorization, cryptography, payments, data loss, migrations, public API compatibility, security, release operations, and irreversible actions as high risk. Apply the detailed selection rules in the review policy.

### 4. Select distinct read-only lanes

Use only lanes with different marginal value:

- Small change: one consolidated correctness reviewer, or no subagent when deterministic evidence fully settles a trivial change.
- Normal PR or diff: correctness/regression/tests plus security/reliability/data risk when applicable.
- Large architectural change: add architecture/maintainability only when distinct from the other lanes.
- Plan: feasibility/dependencies/sequencing plus acceptance/verification/rollback/risk.

Give each reviewer a minimal task-local packet: frozen scope, raw diff or plan sections, applicable requirements, relevant baseline output, one lens, and the finding schema. Prefer no inherited conversation history when the runtime supports it. Reviewers remain read-only; the main agent is the sole fixer and synthesizer.

### 5. Route from live capabilities

Inspect the current delegation tool schema before choosing overrides. Use only exact model and reasoning identifiers exposed there. Apply the Terra, Sol, Spark, and fallback rules in the model-routing reference. Never invent a model identifier or launch an external agent CLI to bypass unavailable controls.

### 6. Review and triage

Require each finding to include:

- artifact location
- `blocking` or `advisory`
- concrete failure mode
- evidence or reproducible reasoning
- smallest credible remediation

Reject unsupported speculation. Deduplicate overlapping findings before deciding what blocks. Reviewer disagreement alone is not a blocker.

Blocking findings are verified correctness defects, security weaknesses, data-loss risks, material regressions, broken requirements, executable-plan contradictions, prerequisites that prevent execution, unverifiable required acceptance gates, or missing rollback for a material irreversible action.

Advisory findings are naming/style preferences, optional refactors, alternate architectures without a demonstrated failure, speculative hardening, and editorial improvements. Advisory findings never trigger a repair loop.

### 7. Repair centrally

In `review-only`, skip repair and report. In `review-and-fix`, let only the main agent apply the smallest complete fix for verified blockers. Avoid opportunistic refactors. Stop for renewed authority if the credible fix materially exceeds the frozen scope.

One repair loop is one central repair batch followed by affected deterministic checks and targeted re-review.

### 8. Verify and target re-review

Re-run affected deterministic checks. Re-review only changed surfaces, unresolved blockers, and directly affected contracts. Repeat a full review only when the fix is systemic or changes the original risk boundary.

Stop early when another pass adds no new evidence. Stop at the configured repair-loop ceiling even if a blocker remains; never continue indefinitely.

### 9. Apply the pass gate

Mark `review-clean: yes` only when all required deterministic checks that could be run pass and no verified blocking findings remain. If a required check could not run, report the limitation and do not imply that gate passed. Advisory findings may remain.

### 10. Report exact state

Report:

- target, authorization, risk, configured budget, actual lanes/models, and repair-loop count
- blockers fixed and unresolved; advisories left
- edits made by the main fixer
- commands/checks with pass, fail, or not-run results
- coverage reductions and next required action
- separate statuses for local verification, review-clean, PR/CI, committed/merged, deployed, and production-verified

Never infer a remote or delivery state from a clean local review.
