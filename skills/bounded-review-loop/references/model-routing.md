# Model Routing

Read only when delegating. Use the runtime-supported default model unless the user or repository specifies a model policy. If an override is requested, inspect the live tool schema and use only exact identifiers and supported reasoning levels. Never invent model names or launch an external agent CLI to bypass unavailable controls or usage limits.

A model family being absent does not itself mean coverage is reduced. Use an available suitable default and disclose only a material limitation, such as an explicitly required independent capability that cannot run.

## Optional cost-oriented policy

Use these preferences only when the user or repository selects this cost-oriented policy:

- Narrow routine review: live-supported Terra at medium reasoning; high for a complex change.
- Material disagreement or risky synthesis: live-supported Sol at high reasoning. Reserve xhigh for an exceptional, justified need.
- Trivial deterministic work: main agent; Spark only if the live schema exposes a valid override. If Spark is unavailable, use Terra when suitable and available, otherwise the runtime-supported default.

The same total call budget applies to all models. Stronger arbitration replaces or reserves a call; it is never an extra call. After two calls under standard, the main agent synthesizes or reports an unmet independent-review requirement.

## Delegate with focused context

Give each reviewer the frozen scope, raw relevant diff/plan, applicable requirements, baseline evidence, one useful perspective, and a read-only constraint. Prefer no inherited conversation history (`fork_turns="none"` where supported). Do not preload the desired answer or previous reviewers' conclusions except for explicit arbitration.

Count every delegated review or follow-up, including reuse of an existing agent, against the entrypoint's total. Never reset counters by changing models or agents. The main agent owns edits, deduplication, and the final result.
