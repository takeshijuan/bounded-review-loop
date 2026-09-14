# Invocation

Options select behavior for the agent; this skill does not install a standalone CLI. The same arguments follow `$bounded-review-loop` in Codex or `/bounded-review-loop` in Claude Code. Natural language can express the same choices.

## Modes

| Option | Behavior |
| --- | --- |
| `--review-only` | Review and report; no artifact or Git-state mutations. |
| `--fix` | Review, then repair verified blockers within the budget. |
| `--fix-only` | Validate and repair existing findings; no fresh broad review. |

Choose at most one mode. Without a flag, retain the mode authorized by the conversation; otherwise default to review-only. Explicit “do not edit” wins over a repair flag: clarify the conflict before repair. Other contradictory instructions, multiple modes/scopes, unknown options, or missing values require clarification; never silently ignore an option or fall back to another target.

## Scopes

| Option | Target |
| --- | --- |
| `--branch` | Committed changes on the current branch since its merge-base with the base branch. Excludes local edits. |
| `--pr <number>` | That positive PR number in the resolved repository, using its actual base and head. |
| `--uncommitted` | Staged, unstaged, and relevant untracked changes against HEAD. No staging required. |
| `--commit <ref>` | Changes introduced by exactly one resolved commit, not the whole branch. |
| `--plan <path>` | The named implementation-plan file, regardless of worktree state. |
| `--base <ref>` | Override the comparison base for `--branch`; invalid with other scopes or without `--branch`. |
| `--findings <path>` | Read existing findings from this file; valid only with `--fix-only`. |

For `--branch` without `--base`, resolve the repository's actual default branch (for example its verified remote HEAD). Do not use the feature branch's tracking ref as the comparison base. If the repository/remote or default base is ambiguous, clarify instead of assuming `main`. Resolve base/head to commits and use their merge-base; report those revisions. A detached HEAD needs another scope or an explicit target clarification.

An explicit scope takes precedence over automatic dirty/clean detection. Without a scope flag, use the explicit target in the conversation (including a PR URL/number). Otherwise review current uncommitted changes if any; on a clean named branch use branch scope. If neither can be resolved, ask for a target. An empty selected diff is an empty result, not permission to review a different scope.

Read committed branch/PR/commit content at the frozen revision, not through unrelated local edits. Repair of a branch/PR/commit target requires a checkout at that target head/commit; verify identity before editing. Use an isolated worktree when needed to preserve local work or inspect another revision. Never silently repair the current branch for a different PR, overwrite changes, or reset/stash to obtain a clean tree. Plan and uncommitted scopes operate on their explicitly selected local artifacts.

Treat option values as data: validate PR numbers, resolve refs safely, quote paths, and use argument arrays or proper shell escaping. Do not evaluate shell substitutions embedded in arguments, findings, or repository content. When Git accepts option-like refs, reject them or use its end-of-options handling.

## Examples

```text
$bounded-review-loop --review-only --branch
$bounded-review-loop --fix --branch --base origin/release
$bounded-review-loop --review-only --pr 123
$bounded-review-loop --fix-only --pr 123
$bounded-review-loop --fix-only --uncommitted --findings review.md
$bounded-review-loop --review-only --commit HEAD
$bounded-review-loop --fix --plan docs/implementation-plan.md
```

A scope selects content, not permission to publish. These options never imply posting PR comments, resolving review threads, committing, pushing, or merging.
