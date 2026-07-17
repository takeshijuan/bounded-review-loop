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

## Budgets

| Preset | Reviewers | Concurrent | Repair loops |
| --- | ---: | ---: | ---: |
| Economy | 0–1 | 1 | 1 |
| Standard (default) | up to 2 | 2 | 2 |
| Strict | up to 3 distinct lanes | 2 | 3 |

Routine review uses live-supported Terra models. Sol is reserved for materially conflicting evidence, risky synthesis, or a warranted high-risk final pass, and its call counts against the same reviewer ceiling. Spark is used only when the runtime explicitly exposes it; otherwise the skill falls back to Terra without inventing a model name.

Reviewers are read-only. One main/fixer agent owns all edits. Review-only requests never edit.

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

The skill does not grant authority to comment, commit, push, approve, merge, deploy, publish, or clean up destructively. Its final report keeps these states separate:

- local verification
- review-clean
- PR/CI
- committed and merged
- deployed
- production-verified

## License

MIT
