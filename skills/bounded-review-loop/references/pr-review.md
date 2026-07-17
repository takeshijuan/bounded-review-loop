# PR Review

## Resolve the PR

Read title, body, linked issue or specification, repository instructions, changed files, base/head refs and SHAs, CI state, and relevant tests. Compare with the target branch when the patch alone does not reveal the contract.

Freeze the reviewed head SHA. If the head changes, identify the new delta before relying on earlier findings.

## Capture the baseline

- Inspect the complete changed-file list and diff.
- Note generated files, dependency or lockfile changes, migrations, public API changes, and workflow changes.
- Run relevant deterministic checks when practical.
- Separate failures already present on the base from failures introduced by the PR.
- Record checks that could not run and why.

## Review lanes

Use tight file/line references:

1. Correctness, regression, and tests.
2. Security, reliability, authorization, data, migration, or API compatibility when the diff touches those surfaces.
3. Architecture and maintainability only for a large systemic change and only when distinct under the strict budget.

Reviewers remain read-only. The main agent deduplicates and, only when authorized, edits locally. A review-and-fix request alone does not authorize a PR comment, commit, push, approval, merge, deployment, or publication.

## Verify and report

After a localized fix, re-review only changed files, unresolved finding IDs, and affected tests/contracts. Repeat the full PR review only for a systemic fix or changed risk boundary.

A locally clean review means required local checks passed and no verified blocker remains. It does not mean GitHub CI is green, the PR is approved or merged, a deployment occurred, or production behavior was verified. Report each state separately.
