#!/usr/bin/env python3
"""Validate the Bounded Review Loop public skill repository."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

import yaml


SKILL_NAME = "bounded-review-loop"
REQUIRED_FILES = (
    ".github/FUNDING.yml",
    ".github/workflows/validate.yml",
    ".gitignore",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "package-lock.json",
    "package.json",
    "README.md",
    "requirements-validation.txt",
    "SECURITY.md",
    "skills.sh.json",
    "skills/bounded-review-loop/SKILL.md",
    "skills/bounded-review-loop/agents/openai.yaml",
    "skills/bounded-review-loop/evals/evals.json",
    "skills/bounded-review-loop/references/invocation.md",
    "skills/bounded-review-loop/references/repair-only.md",
    "skills/bounded-review-loop/references/model-routing.md",
    "skills/bounded-review-loop/references/plan-review.md",
    "skills/bounded-review-loop/references/pr-review.md",
    "skills/bounded-review-loop/references/review-policy.md",
    "tests/test_validate_skill.py",
)
REQUIRED_EVAL_COVERAGE = {
    "fix-only-report",
    "fix-only-missing-source",
    "fix-only-pr-feedback",
    "branch-scope",
    "explicit-pr-scope",
    "invalid-options",
    "empty-scope",
    "untrusted-options",
    "exhausted-call-budget",
    "concise-report",
    "inherited-authorization",
    "advisory-stop",
    "bounded-until-clean",
    "loop-limit",
    "minimal-readonly-context",
    "normal-pr",
    "plan-classification",
    "review-only",
    "security-sensitive",
    "sol-arbitration-budget",
    "spark-fallback",
    "state-separation",
    "targeted-rereview",
    "trivial-deterministic",
}
EXPECTED_BUDGET_CEILINGS = {
    "economy": (1, 1, 1),
    "standard": (2, 2, 2),
    "strict": (3, 2, 3),
}
SKIP_DIRS = {
    ".git",
    ".pytest_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
}
FORBIDDEN_PUBLIC_FILENAMES = {
    ".env",
    "AGENTS.md",
    "CLAUDE.md",
    "memory.md",
    "skills-lock.json",
}


class Validation:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.skill_dir = self.root / "skills" / SKILL_NAME
        self.errors: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def read(self, relative: str | Path) -> str:
        path = self.root / relative
        try:
            return path.read_text(encoding="utf-8")
        except FileNotFoundError:
            self.error(f"missing required file: {path.relative_to(self.root)}")
        except UnicodeDecodeError:
            self.error(f"expected UTF-8 text file: {path.relative_to(self.root)}")
        return ""

    def public_files(self) -> Iterable[Path]:
        for path in self.root.rglob("*"):
            if not path.is_file():
                continue
            relative = path.relative_to(self.root)
            if any(part in SKIP_DIRS for part in relative.parts):
                continue
            yield path

    def validate_required_files(self) -> None:
        for relative in REQUIRED_FILES:
            if not (self.root / relative).is_file():
                self.error(f"missing required file: {relative}")

    def parse_frontmatter(self, text: str) -> dict[str, Any] | None:
        match = re.match(r"\A---\n(.*?)\n---(?:\n|\Z)", text, re.DOTALL)
        if not match:
            self.error("SKILL.md must start with closed YAML frontmatter")
            return None
        try:
            data = yaml.safe_load(match.group(1))
        except yaml.YAMLError as exc:
            self.error(f"SKILL.md frontmatter is invalid YAML: {exc}")
            return None
        if not isinstance(data, dict):
            self.error("SKILL.md frontmatter must be a mapping")
            return None
        return data

    def validate_frontmatter(self) -> None:
        skill_text = self.read(self.skill_dir / "SKILL.md")
        if len(skill_text.splitlines()) >= 500:
            self.error("SKILL.md must remain under 500 lines")
        frontmatter = self.parse_frontmatter(skill_text)
        if frontmatter is None:
            return
        if set(frontmatter) != {"name", "description"}:
            self.error("SKILL.md frontmatter must contain only name and description")
        name = frontmatter.get("name")
        if name != SKILL_NAME:
            self.error(f"SKILL.md name must be {SKILL_NAME}")
        if self.skill_dir.name != name:
            self.error("skill directory name must match frontmatter name")
        if not isinstance(name, str) or not re.fullmatch(
            r"[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?", name
        ):
            self.error("skill name must be valid lowercase hyphen-case")
        description = frontmatter.get("description")
        if not isinstance(description, str) or not description.strip():
            self.error("SKILL.md description must be a non-empty string")
            return
        if len(description) > 1024:
            self.error("SKILL.md description must be at most 1024 characters")
        if "<" in description or ">" in description:
            self.error("SKILL.md description cannot contain angle brackets")

    def load_yaml(self, relative: str) -> Any:
        text = self.read(relative)
        try:
            return yaml.safe_load(text)
        except yaml.YAMLError as exc:
            self.error(f"{relative} is invalid YAML: {exc}")
            return None

    def load_json(self, relative: str) -> Any:
        text = self.read(relative)
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            self.error(f"{relative} is invalid JSON: {exc}")
            return None

    def validate_serialized_metadata(self) -> None:
        openai = self.load_yaml(
            "skills/bounded-review-loop/agents/openai.yaml"
        )
        if not isinstance(openai, dict) or not isinstance(
            openai.get("interface"), dict
        ):
            self.error("agents/openai.yaml must contain an interface mapping")
        else:
            interface = openai["interface"]
            required = {"display_name", "short_description", "default_prompt"}
            if not required.issubset(interface):
                self.error(
                    "agents/openai.yaml must define display_name, "
                    "short_description, and default_prompt"
                )
            for key, value in interface.items():
                if not isinstance(value, str):
                    self.error(f"agents/openai.yaml interface.{key} must be a string")
            short = interface.get("short_description", "")
            if isinstance(short, str) and not 25 <= len(short) <= 64:
                self.error(
                    "agents/openai.yaml short_description must be 25-64 characters"
                )
            prompt = interface.get("default_prompt", "")
            if isinstance(prompt, str) and f"${SKILL_NAME}" not in prompt:
                self.error(
                    f"agents/openai.yaml default_prompt must mention ${SKILL_NAME}"
                )

        metadata = self.load_json("skills.sh.json")
        if isinstance(metadata, dict):
            if (
                metadata.get("$schema")
                != "https://skills.sh/schemas/skills.sh.schema.json"
            ):
                self.error("skills.sh.json must use the current schema URL")
            groupings = metadata.get("groupings")
            if not isinstance(groupings, list) or not any(
                isinstance(group, dict)
                and SKILL_NAME in group.get("skills", [])
                for group in groupings
            ):
                self.error("skills.sh.json must group bounded-review-loop")
        elif metadata is not None:
            self.error("skills.sh.json must contain a JSON object")

        workflow = self.load_yaml(".github/workflows/validate.yml")
        if not isinstance(workflow, dict):
            self.error("validation workflow must be a YAML mapping")
        workflow_text = self.read(".github/workflows/validate.yml")
        if not re.search(
            r"(?m)^permissions:\s*\n\s+contents:\s*read\s*$", workflow_text
        ):
            self.error("validation workflow must declare contents: read permissions")
        for command in (
            "python -m pip install --require-hashes -r requirements-validation.txt",
            "npm ci --ignore-scripts --no-audit --no-fund",
            "python -m unittest discover",
            "python scripts/validate_skill.py",
            "npx --no-install skills add . --list",
        ):
            if command not in workflow_text:
                self.error(f"validation workflow is missing command: {command}")
        action_uses = re.findall(r"(?m)^\s*-\s+uses:\s+([^@\s]+)@([^\s#]+)", workflow_text)
        if not action_uses:
            self.error("validation workflow must contain pinned actions")
        for action, revision in action_uses:
            if not re.fullmatch(r"[0-9a-f]{40}", revision):
                self.error(
                    f"validation workflow action must use an immutable SHA: {action}"
                )

        funding = self.load_yaml(".github/FUNDING.yml")
        if not isinstance(funding, dict) or not funding.get("github"):
            self.error("FUNDING.yml must contain the established GitHub sponsor")

    def parse_budget_rows(self, text: str) -> dict[str, tuple[int, int, int]]:
        rows: dict[str, tuple[int, int, int]] = {}
        for line in text.splitlines():
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if not cells or cells[0].lower() not in EXPECTED_BUDGET_CEILINGS:
                continue
            if len(cells) < 4:
                continue
            numbers: list[int] = []
            for cell in cells[1:4]:
                match = re.search(r"\d+", cell)
                if not match:
                    self.error(
                        f"budget row {cells[0]} contains a non-numeric ceiling"
                    )
                    break
                numbers.append(int(match.group(0)))
            if len(numbers) == 3:
                rows[cells[0].lower()] = tuple(numbers)  # type: ignore[assignment]
        return rows

    def validate_contract(self) -> None:
        skill = self.read("skills/bounded-review-loop/SKILL.md")
        for reference in (
            "invocation.md", "repair-only.md", "review-policy.md",
            "model-routing.md", "pr-review.md", "plan-review.md",
        ):
            if f"references/{reference}" not in skill:
                self.error(f"SKILL.md must directly reference references/{reference}")
        budget_rows = self.parse_budget_rows(skill)
        for preset, expected in EXPECTED_BUDGET_CEILINGS.items():
            if budget_rows.get(preset) != expected:
                self.error(
                    f"{preset} budget ceilings must be calls/concurrent/loops "
                    f"{expected[0]}/{expected[1]}/{expected[2]}"
                )

    def validate_evals(self) -> None:
        relative = "skills/bounded-review-loop/evals/evals.json"
        payload = self.load_json(relative)
        if not isinstance(payload, dict):
            self.error("evals.json must contain an object")
            return
        if payload.get("schema_version") != 2:
            self.error("evals.json schema_version must be 2")
        if payload.get("skill_name") != SKILL_NAME:
            self.error(f"evals.json skill_name must be {SKILL_NAME}")
        evals = payload.get("evals")
        if not isinstance(evals, list):
            self.error("evals.json evals must be a list")
            return
        if len(evals) < len(REQUIRED_EVAL_COVERAGE):
            self.error("evals.json does not contain enough representative cases")

        ids: set[str] = set()
        coverage: set[str] = set()
        for index, case in enumerate(evals):
            label = f"eval[{index}]"
            if not isinstance(case, dict):
                self.error(f"{label} must be an object")
                continue
            case_id = case.get("id")
            if not isinstance(case_id, str) or not case_id:
                self.error(f"{label}.id must be a non-empty string")
            elif case_id in ids:
                self.error(f"duplicate eval id: {case_id}")
            else:
                ids.add(case_id)
            covers = case.get("covers")
            if not isinstance(covers, str) or not covers:
                self.error(f"{label}.covers must be a non-empty string")
            else:
                coverage.add(covers)
            if case.get("target") not in {"pr", "local-diff", "plan"}:
                self.error(f"{label}.target must be pr, local-diff, or plan")
            if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
                self.error(f"{label}.prompt must be a non-empty string")
            expected = case.get("expected")
            if not isinstance(expected, dict):
                self.error(f"{label}.expected must be an object")
                continue
            budget = expected.get("budget")
            if budget not in EXPECTED_BUDGET_CEILINGS:
                self.error(f"{label}.expected.budget is invalid")
                continue
            call_limit, concurrent_limit, loop_limit = (
                EXPECTED_BUDGET_CEILINGS[budget]
            )
            numeric_fields = (
                ("max_review_calls", call_limit),
                ("max_concurrent_reviewers", concurrent_limit),
                ("max_repair_loops", loop_limit),
            )
            for field, ceiling in numeric_fields:
                value = expected.get(field)
                if type(value) is not int or value < 0:
                    self.error(f"{label}.expected.{field} must be a non-negative int")
                elif value > ceiling:
                    self.error(
                        f"{label}.expected.{field} exceeds the {budget} ceiling"
                    )
            calls = expected.get("max_review_calls")
            concurrent = expected.get("max_concurrent_reviewers")
            if (
                isinstance(calls, int)
                and isinstance(concurrent, int)
                and concurrent > calls
            ):
                self.error(f"{label} concurrency cannot exceed review call count")
            for field in ("must", "must_not"):
                value = expected.get(field)
                if not isinstance(value, list) or not value or not all(
                    isinstance(item, str) and item.strip() for item in value
                ):
                    self.error(
                        f"{label}.expected.{field} must be a non-empty string list"
                    )

        missing = REQUIRED_EVAL_COVERAGE - coverage
        extra = coverage - REQUIRED_EVAL_COVERAGE
        if missing:
            self.error(f"evals missing required coverage: {', '.join(sorted(missing))}")
        if extra:
            self.error(f"evals contain unknown coverage: {', '.join(sorted(extra))}")

        by_coverage = {
            case.get("covers"): case
            for case in evals
            if isinstance(case, dict) and isinstance(case.get("expected"), dict)
        }
        for key in ("review-only", "advisory-stop"):
            case = by_coverage.get(key, {})
            if case.get("expected", {}).get("max_repair_loops") != 0:
                self.error(f"{key} eval must prohibit repair loops")
        bounded = by_coverage.get("bounded-until-clean", {}).get("expected", {})
        if bounded.get("budget") != "standard" or bounded.get(
            "max_repair_loops"
        ) != 2:
            self.error("bounded-until-clean eval must retain the standard limit")
        for key in ("fix-only-report", "fix-only-missing-source", "fix-only-pr-feedback"):
            case = by_coverage.get(key, {}).get("expected", {})
            if case.get("max_review_calls") != 0:
                self.error(f"{key} eval must prohibit delegated review calls")

    def validate_links(self) -> None:
        markdown_link = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        for path in self.public_files():
            if path.suffix.lower() != ".md":
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for raw_target in markdown_link.findall(text):
                target = raw_target.strip().strip("<>")
                if (
                    not target
                    or target.startswith(("#", "http://", "https://", "mailto:"))
                ):
                    continue
                target_path = target.split("#", 1)[0]
                resolved = (path.parent / target_path).resolve()
                if not resolved.is_relative_to(self.root):
                    self.error(
                        f"markdown link escapes repository: "
                        f"{path.relative_to(self.root)} -> {target}"
                    )
                elif not resolved.exists():
                    self.error(
                        f"broken markdown link: "
                        f"{path.relative_to(self.root)} -> {target}"
                    )

    def validate_public_safety(self) -> None:
        for path in self.public_files():
            relative = path.relative_to(self.root)
            if path.name in FORBIDDEN_PUBLIC_FILENAMES:
                self.error(f"forbidden public operating file: {relative}")

        private_fragments = (
            "/" + "Users" + "/",
            "C:" + "\\" + "Users" + "\\",
            "/" + "home" + "/",
            ".codex" + "/worktrees",
            "conversation" + " transcript",
            "prompt-generation" + " time",
            "memory" + " facts",
        )
        secret_patterns = (
            re.compile("gh" + r"p_[A-Za-z0-9]{30,}"),
            re.compile("github_pat" + r"_[A-Za-z0-9_]{20,}"),
            re.compile("s" + r"k-[A-Za-z0-9_-]{20,}"),
            re.compile("AK" + r"IA[0-9A-Z]{16}"),
            re.compile("xo" + r"x[baprs]-[A-Za-z0-9-]{10,}"),
            re.compile("-----BEGIN " + "PRIVATE KEY-----"),
        )
        for path in self.public_files():
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            relative = path.relative_to(self.root)
            for fragment in private_fragments:
                if fragment.lower() in text.lower():
                    self.error(f"private path or provenance marker in {relative}")
            for pattern in secret_patterns:
                if pattern.search(text):
                    self.error(f"credential-like value in {relative}")

        license_text = self.read("LICENSE")
        if not license_text.startswith("MIT License\n"):
            self.error("LICENSE must contain the MIT license text")
        readme = self.read("README.md")
        for required in (
            "npx --yes skills@1.5.17 add takeshijuan/bounded-review-loop "
            "--skill bounded-review-loop",
            "npx --yes skills@1.5.17 add . --list",
            "npx --yes skills@1.5.17 add "
            "takeshijuan/bounded-review-loop --list",
        ):
            if required not in readme:
                self.error(f"README is missing verified install/discovery command: {required}")

    def run(self) -> list[str]:
        self.validate_required_files()
        self.validate_frontmatter()
        self.validate_serialized_metadata()
        self.validate_contract()
        self.validate_evals()
        self.validate_links()
        self.validate_public_safety()
        return self.errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root to validate (defaults to this repository).",
    )
    args = parser.parse_args()
    errors = Validation(args.repo).run()
    if errors:
        for message in errors:
            print(f"error: {message}")
        return 1
    print("skill validation: clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
