from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = REPO_ROOT / "scripts" / "validate_skill.py"


class SkillRepositoryValidationTests(unittest.TestCase):
    def run_validator(self, repo: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), "--repo", str(repo)],
            text=True,
            capture_output=True,
            check=False,
        )

    @contextmanager
    def copied_repository(self) -> Iterator[Path]:
        with tempfile.TemporaryDirectory() as temporary_directory:
            destination = Path(temporary_directory) / "repo"
            shutil.copytree(
                REPO_ROOT,
                destination,
                ignore=shutil.ignore_patterns(
                    ".git", ".pytest_cache", ".venv", "__pycache__", "node_modules"
                ),
            )
            yield destination

    def replace(self, repo: Path, relative: str, old: str, new: str) -> None:
        path = repo / relative
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def assert_invalid(self, repo: Path, message: str) -> None:
        result = self.run_validator(repo)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(message, result.stdout)
        self.assertEqual(result.stderr, "")

    def test_complete_repository_validates(self) -> None:
        result = self.run_validator(REPO_ROOT)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout, "skill validation: clean\n")
        self.assertEqual(result.stderr, "")

    def test_missing_required_file_is_rejected(self) -> None:
        with self.copied_repository() as repo:
            (repo / "SECURITY.md").unlink()
            self.assert_invalid(repo, "missing required file: SECURITY.md")

    def test_frontmatter_rejects_extra_field(self) -> None:
        with self.copied_repository() as repo:
            self.replace(
                repo,
                "skills/bounded-review-loop/SKILL.md",
                "name: bounded-review-loop\n",
                "name: bounded-review-loop\nlicense: MIT\n",
            )
            self.assert_invalid(
                repo,
                "frontmatter must contain only name and description",
            )

    def test_openai_default_prompt_must_name_skill(self) -> None:
        with self.copied_repository() as repo:
            self.replace(
                repo,
                "skills/bounded-review-loop/agents/openai.yaml",
                "$bounded-review-loop",
                "the review skill",
            )
            self.assert_invalid(
                repo,
                "default_prompt must mention $bounded-review-loop",
            )

    def test_workflow_rejects_mutable_action_tag(self) -> None:
        with self.copied_repository() as repo:
            self.replace(
                repo,
                ".github/workflows/validate.yml",
                "actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5",
                "actions/checkout@v4",
            )
            self.assert_invalid(
                repo,
                "workflow action must use an immutable SHA: actions/checkout",
            )

    def test_budget_ceiling_increase_is_rejected(self) -> None:
        with self.copied_repository() as repo:
            self.replace(
                repo,
                "skills/bounded-review-loop/SKILL.md",
                "| standard | 2 | 2 | 2 |",
                "| standard | 4 | 4 | 5 |",
            )
            self.assert_invalid(
                repo,
                "standard budget ceilings must be calls/concurrent/loops 2/2/2",
            )

    def test_missing_eval_coverage_is_rejected(self) -> None:
        with self.copied_repository() as repo:
            path = repo / "skills/bounded-review-loop/evals/evals.json"
            payload = json.loads(path.read_text(encoding="utf-8"))
            payload["evals"] = [
                case
                for case in payload["evals"]
                if case["covers"] != "bounded-until-clean"
            ]
            path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            self.assert_invalid(
                repo,
                "evals missing required coverage: bounded-until-clean",
            )

    def test_fix_only_eval_cannot_launch_reviewers(self) -> None:
        with self.copied_repository() as repo:
            path = repo / "skills/bounded-review-loop/evals/evals.json"
            payload = json.loads(path.read_text(encoding="utf-8"))
            case = next(item for item in payload["evals"] if item["covers"] == "fix-only-report")
            case["expected"]["max_review_calls"] = 1
            path.write_text(json.dumps(payload) + "\n", encoding="utf-8")
            self.assert_invalid(repo, "fix-only-report eval must prohibit delegated review calls")

    def test_concurrency_cannot_exceed_total_calls(self) -> None:
        with self.copied_repository() as repo:
            path = repo / "skills/bounded-review-loop/evals/evals.json"
            payload = json.loads(path.read_text(encoding="utf-8"))
            case = next(item for item in payload["evals"] if item["covers"] == "normal-pr")
            case["expected"]["max_review_calls"] = 1
            case["expected"]["max_concurrent_reviewers"] = 2
            path.write_text(json.dumps(payload) + "\n", encoding="utf-8")
            self.assert_invalid(repo, "concurrency cannot exceed review call count")

    def test_broken_relative_markdown_link_is_rejected(self) -> None:
        with self.copied_repository() as repo:
            self.replace(
                repo,
                "skills/bounded-review-loop/SKILL.md",
                "references/pr-review.md",
                "references/missing-pr-review.md",
            )
            self.assert_invalid(repo, "broken markdown link")

    def test_private_absolute_path_is_rejected(self) -> None:
        with self.copied_repository() as repo:
            path = repo / "README.md"
            private_path = "/" + "Users" + "/example/private/repository"
            path.write_text(
                path.read_text(encoding="utf-8") + f"\n{private_path}\n",
                encoding="utf-8",
            )
            self.assert_invalid(repo, "private path or provenance marker in README.md")

    def test_credential_like_value_is_rejected(self) -> None:
        with self.copied_repository() as repo:
            path = repo / "README.md"
            fake_credential = "gh" + "p_" + ("A" * 36)
            path.write_text(
                path.read_text(encoding="utf-8") + f"\n{fake_credential}\n",
                encoding="utf-8",
            )
            self.assert_invalid(repo, "credential-like value in README.md")

    def test_review_only_eval_cannot_allow_repairs(self) -> None:
        with self.copied_repository() as repo:
            path = repo / "skills/bounded-review-loop/evals/evals.json"
            payload = json.loads(path.read_text(encoding="utf-8"))
            case = next(
                item for item in payload["evals"] if item["covers"] == "review-only"
            )
            case["expected"]["max_repair_loops"] = 1
            path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            self.assert_invalid(repo, "review-only eval must prohibit repair loops")


if __name__ == "__main__":
    unittest.main()
