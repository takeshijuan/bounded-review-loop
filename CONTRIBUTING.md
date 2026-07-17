# Contributing

Thanks for improving Bounded Review Loop.

## Guidelines

- Keep reviewer fanout, concurrency, repair loops, and model escalation finite.
- Preserve review-only mode and central fixer ownership.
- Require evidence for blockers; do not make advisory findings gate completion.
- Keep `SKILL.md` concise and references one level deep.
- Add or update eval coverage for behavior changes.
- Do not add private paths, credentials, transcripts, or repository-local operating files.

Run before opening a pull request:

```bash
python -m unittest discover -s tests -v
python scripts/validate_skill.py
npx --yes skills@1.5.17 add . --list
```

Include the behavior changed, validation evidence, and any remaining limitations.
