# Plan Review

## Resolve the plan

Read the complete plan, its referenced requirements/specifications, repository constraints, and any named implementation surfaces. Freeze the file revision or content hash. Do not assume implementation work has started.

## Review lanes

Evaluate:

- feasibility against the current system
- dependency and migration ordering
- completeness and testability of acceptance criteria
- verification commands, prototypes, or observable gates
- rollout, rollback, data, security, and irreversible-operation controls
- ownership or prerequisites that can prevent execution

Use one consolidated lane for a small plan. For a normal plan, separate feasibility/dependencies/sequencing from acceptance/verification/rollback/risk. Add a third architecture lens only under the strict budget when it has distinct value.

## Classify findings

Blocking plan findings include:

- a contradiction that prevents execution
- an unavailable prerequisite with no resolution path
- dependency ordering that cannot work
- a required outcome with no observable acceptance gate
- a material irreversible migration or release step with no rollback/control

Advisory plan findings include prose taste, naming, optional detail, and equally viable design alternatives without a demonstrated execution failure. Advisory findings do not trigger repair.

## Edit and verify

Edit only with explicit plan-improvement or repair authority. Apply the smallest plan change that resolves verified blockers; do not silently redesign the project.

Distinguish:

- document review evidence
- commands or prototypes actually run
- checks proposed for future implementation

Never report a proposed command as executed. Passing plan review means no verified execution blocker remains in the plan; it does not mean implementation began, tests passed, deployment occurred, or production was verified.
