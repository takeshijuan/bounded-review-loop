# Bounded Review Loop

[![skills.sh](https://skills.sh/b/takeshijuan/bounded-review-loop)](https://skills.sh/takeshijuan/bounded-review-loop)

`bounded-review-loop` is an Agent Skill for budget-controlled, evidence-based review and optional repair of pull requests, working-tree changes, and implementation plans.

It replaces open-ended “review until clean” behavior with finite reviewer fanout, a central fixer, targeted re-review, and an exact pass gate: required deterministic checks pass and no verified blocking finding remains. Advisory suggestions do not keep the loop running.

## Install

Install only this skill from the public repository:

```bash
npx --yes skills@1.5.17 add takeshijuan/bounded-review-loop --skill bounded-review-loop
```

Use locally from a clone:

```bash
npx --yes skills@1.5.17 add . --skill bounded-review-loop
```

## Usage

Use skill arguments in Codex (`$bounded-review-loop`) or Claude Code (`/bounded-review-loop`); these are instructions to the agent, not a standalone executable.

```text
$bounded-review-loop --review-only --branch
$bounded-review-loop --fix --branch --base origin/release
$bounded-review-loop --review-only --pr 123
$bounded-review-loop --fix-only --pr 123
$bounded-review-loop --fix-only --uncommitted --findings review.md
$bounded-review-loop --review-only --commit HEAD
$bounded-review-loop --fix --plan docs/implementation-plan.md
```

Choose one mode and at most one scope. `--branch` compares committed changes on the current branch with the merge-base of the repository's default branch, or `--base`. `--pr` uses that PR's actual base/head. Explicit targets are preserved even in a dirty worktree. Natural-language requests and previously granted in-scope authorization remain supported. See [Invocation](skills/bounded-review-loop/references/invocation.md) for defaults and invalid combinations.

`--fix-only` repairs existing findings from `--findings`, the selected conversation report, or existing PR feedback. It verifies findings against the current target and runs affected checks without a fresh review sweep. Missing findings are requested instead of invented. Repair completion does not claim the whole artifact is review-clean.

The PR workflow takes inspiration from [Claude Code's code-review command](https://github.com/anthropics/claude-code/tree/main/plugins/code-review): inspect the requested PR and applicable instructions, substantiate findings, and keep results concise. The mode and scope options above belong to this skill; they are not claims about Claude's command flags.

## Budgets

| Preset | Delegated review calls, total | Concurrent calls | Repair loops |
| --- | ---: | ---: | ---: |
| Economy | up to 1 | 1 | 1 |
| Standard (default) | up to 2 | 2 | 2 |
| Strict | up to 3 | 2 | 3 |

Every delegated initial review, follow-up, arbitration, and final pass counts, including reuse of the same agent. These are ceilings, not quotas. After calls are exhausted the main agent verifies repairs; any explicitly required independent re-review remains unmet. Repair-only does not launch reviewers. Review-only permits no repair loops.

Delegation uses the runtime-supported default unless a model policy is selected. The optional [cost-oriented policy](skills/bounded-review-loop/references/model-routing.md) retains Terra/Sol/Spark preferences without imposing them on every runtime.

Reviewers are read-only. The main agent owns all edits. Local repairs never imply permission to comment, commit, push, resolve threads, or merge.

## Validate

```bash
python -m unittest discover -s tests -v
python scripts/validate_skill.py
npx --yes skills@1.5.17 add . --list
```

After publication, verify remote discovery:

```bash
npx --yes skills@1.5.17 add takeshijuan/bounded-review-loop --list
```

The root `skills.sh.json` groups the skill for its skills.sh repository page. Observed installs drive public discovery; no release tag is required for installation from the default branch.

## Safety and state reporting

Preserve existing authorization for the selected scope; review or repair alone grants no external publication or Git mutation authority. Report findings/repairs, actual mode and budget usage, relevant checks, and unmet requirements. Omit unrelated status fields while distinguishing local verification, review-clean, PR/CI, merge, deployment, and production verification whenever relevant.

Schema and validator tests check packaging and invariants; behavioral evals require an agent run against realistic artifacts. Passing static validation alone does not establish review quality.

## License

MIT
