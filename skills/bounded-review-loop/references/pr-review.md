# PR Review

Resolve the explicit `--pr <number>` (or conversational PR target) in the correct repository. Read its title, body, linked requirements, applicable AGENTS.md/CLAUDE.md, base/head SHAs, changed files, and CI state. Inspect the complete diff and relevant surrounding code. Do not replace the requested PR with the current branch's PR.

Closed, draft, automated, previously reviewed, or small PRs may still be explicitly requested for review. Report their state and avoid duplicate work, but do not silently skip the user's target solely on those grounds. Use blame/history and previous comments when they resolve an uncertainty; verify purported problems against the current code and filter unsupported or pre-existing findings.

Freeze the reviewed head SHA. Point findings to tight file/line locations at that revision. Before concluding, check whether the head changed; inspect any new delta before claiming the current PR was reviewed. If required data or permissions are unavailable, report the coverage gap.

With `--fix-only`, use [Repair only](repair-only.md) to collect and validate existing findings; skip the fresh review sweep. With either repair mode, verify the checkout belongs to the selected PR/head and preserve unrelated work as described in [Invocation](invocation.md).

After a localized repair, verify only the repaired surface and unresolved findings. Full re-review requires a systemic change and remaining call budget. Report relevant CI status separately from local checks, and never infer approval, merge, deployment, or production success from a clean local review. Posting comments or resolving threads requires separate existing authorization.
