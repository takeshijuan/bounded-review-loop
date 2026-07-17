# Security Policy

## Reporting

Use GitHub private vulnerability reporting when available. Otherwise open a minimal issue requesting maintainer contact without publishing exploit details or credentials.

## Scope

Reports are in scope when they concern:

- unauthorized edits or external mutations
- unbounded delegation or repair behavior
- model-routing behavior that bypasses runtime controls
- false verification or clean-state claims
- prompt-injection or secret-exposure risk in the skill
- supply-chain or workflow-permission risk

The skill must not request access-control bypasses, conceal changes, expose task transcripts, or claim evidence it did not observe.
