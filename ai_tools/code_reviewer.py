"""
AI-Powered Code Reviewer
Uses local Granite model to review code changes, find bugs, and suggest improvements
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import List, Dict, Optional
import logging

# Add ai_tools to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from ollama_client import OllamaClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CodeReviewer:
    """AI-powered code review using local models"""

    def __init__(self, model: str = "granite-code:3b"):
        self.client = OllamaClient(model=model)
        self.system_prompt = """You are an expert code reviewer. Analyze code for:
- Security vulnerabilities
- Performance issues
- Code quality and best practices
- Potential bugs
- Documentation gaps
Provide clear, actionable feedback."""

    def review_file(self, filepath: str) -> Dict[str, any]:
        """
        Review a single file

        Args:
            filepath: Path to file to review

        Returns:
            Review results dictionary
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()

            prompt = f"""Review this {Path(filepath).suffix} file:

```
{code[:2000]}  # Limit for context
```

File: {filepath}

Provide:
1. Security Issues (if any)
2. Code Quality Issues
3. Suggestions for Improvement
4. Overall Rating (1-10)
"""

            response = self.client.generate(prompt, system=self.system_prompt)

            return {
                "file": filepath,
                "review": response,
                "status": "success"
            }

        except Exception as e:
            logger.error(f"Error reviewing {filepath}: {e}")
            return {
                "file": filepath,
                "review": "",
                "status": "error",
                "error": str(e)
            }

    def review_git_diff(self, base_branch: str = "main") -> Dict[str, any]:
        """
        Review git diff against base branch

        Args:
            base_branch: Branch to compare against

        Returns:
            Review of changes
        """
        try:
            # Get diff
            result = subprocess.run(
                ["git", "diff", base_branch, "--", "*.py"],
                capture_output=True,
                text=True
            )

            diff = result.stdout

            if not diff:
                return {"status": "no_changes"}

            prompt = f"""Review these code changes:

```diff
{diff[:3000]}  # Limit context
```

Focus on:
1. Breaking changes
2. Security implications
3. Code quality
4. Potential bugs introduced
"""

            response = self.client.generate(prompt, system=self.system_prompt)

            return {
                "type": "git_diff",
                "review": response,
                "status": "success"
            }

        except Exception as e:
            logger.error(f"Error reviewing git diff: {e}")
            return {"status": "error", "error": str(e)}

    def review_directory(self, directory: str, extensions: List[str] = ['.py']) -> List[Dict]:
        """
        Review all files in a directory

        Args:
            directory: Directory path
            extensions: File extensions to review

        Returns:
            List of review results
        """
        reviews = []
        path = Path(directory)

        for ext in extensions:
            for filepath in path.rglob(f"*{ext}"):
                if self._should_skip(filepath):
                    continue

                logger.info(f"Reviewing: {filepath}")
                review = self.review_file(str(filepath))
                reviews.append(review)

        return reviews

    def _should_skip(self, filepath: Path) -> bool:
        """Check if file should be skipped"""
        skip_dirs = {'.git', '__pycache__', '.venv', 'venv', 'node_modules', '.idea'}
        return any(part in skip_dirs for part in filepath.parts)

    def generate_report(self, reviews: List[Dict]) -> str:
        """
        Generate markdown report from reviews

        Args:
            reviews: List of review results

        Returns:
            Markdown formatted report
        """
        report = ["# Code Review Report\n"]

        for review in reviews:
            if review.get("status") == "success":
                report.append(f"## {review['file']}\n")
                report.append(review['review'])
                report.append("\n---\n")

        return "\n".join(report)


def main():
    """Run code review from command line"""
    import argparse

    parser = argparse.ArgumentParser(description="AI Code Reviewer")
    parser.add_argument("--file", help="Review single file")
    parser.add_argument("--dir", help="Review directory")
    parser.add_argument("--diff", action="store_true", help="Review git diff")
    parser.add_argument("--output", help="Output file for report")

    args = parser.parse_args()

    reviewer = CodeReviewer()

    if not reviewer.client.is_available():
        print("Error: Ollama service not available")
        print(f"Make sure Ollama is running at {reviewer.client.host}")
        sys.exit(1)

    reviews = []

    if args.file:
        reviews = [reviewer.review_file(args.file)]
    elif args.dir:
        reviews = reviewer.review_directory(args.dir)
    elif args.diff:
        result = reviewer.review_git_diff()
        if result.get("status") == "success":
            print(result["review"])
        return

    if reviews:
        report = reviewer.generate_report(reviews)

        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"Report saved to {args.output}")
        else:
            print(report)


if __name__ == "__main__":
    main()
