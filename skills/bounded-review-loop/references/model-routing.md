# Model Routing

## Discover capabilities first

Inspect the live delegation or subagent tool schema before selecting a model or reasoning override. Build the allowed set from exact identifiers and levels exposed by that runtime. Never construct an identifier from a family name, copy a stale identifier from this reference, or assume every runtime exposes the same models.

If model override controls are unavailable, omit the override, use the runtime-supported default, and report the coverage limitation. Do not launch an external agent CLI to bypass unavailable model controls or usage limits.

## Route by marginal value

| Work | Preferred route |
| --- | --- |
| Trivial deterministic or mechanical check | Main agent without a reviewer; Spark only if the live schema explicitly exposes a valid Spark override |
| Narrow routine review | A live Terra identifier at medium reasoning |
| Complex normal review | A live Terra identifier at high reasoning |
| Conflicting findings, high-risk synthesis, or risky fix design | A live Sol identifier at high reasoning |
| Exceptional security, cryptographic, data-loss, or irreversible-release decision | Sol at `xhigh` only when both identifier and reasoning level are live-supported |

When Spark is unavailable or unsupported, fall back to a live Terra identifier at medium reasoning. Do not fail the workflow and do not invent a Spark model name. If Terra is also unavailable, use the runtime-supported default and mark coverage reduced.

Sol is not a routine reviewer. Use it only after deterministic evidence and Terra review leave a material conflict, or for a risk-sensitive synthesis/final pass. A high-risk label alone does not require `xhigh`.

## Bound delegation

- `economy`: zero or one reviewer.
- `standard`: at most two Terra reviewers.
- `strict`: at most three distinct lanes, with no more than two reviewers running concurrently.
- Never create additional voters to manufacture confidence.

Count every delegated review, arbitration, or final-pass call against the preset's reviewer ceiling, regardless of model. A Sol pass must replace or reserve a Terra slot; it is never an extra call outside the budget. For example, a strict security review may use two Terra lanes plus one Sol final lane, not three Terra lanes plus Sol.

If two Terra reviewers have already consumed the standard ceiling and then disagree, do not add Sol. Let the main agent arbitrate from deterministic evidence or report the unresolved conflict. When high-risk arbitration is foreseeable, reserve the second standard slot for Sol and use at most one Terra reviewer first.

Use `fork_turns="none"` or the runtime equivalent when supported. Otherwise pass the minimum task-local context and explicitly omit unrelated history.

Each reviewer prompt includes:

- frozen artifact scope
- raw relevant diff or plan sections
- applicable requirement excerpts
- baseline command evidence
- one review lens
- the structured finding format
- an explicit read-only/no-edit constraint

Do not include earlier reviewers’ answers unless the task is explicit arbitration. The main agent owns edits, deduplication, model escalation decisions, and the final report.
