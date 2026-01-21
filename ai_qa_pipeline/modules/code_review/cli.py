"""
Code Review CLI
===============

Command-line интерфейс для статического анализа и AI code review.
"""

import argparse
import json
import sys
from pathlib import Path

from .linter import CodeLinter
from .ai_reviewer import AICodeReviewer, ReviewSeverity
from ..test_generation.llm_client import LLMProvider


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Code Quality & AI Review Tool"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: lint (static analysis)
    lint_parser = subparsers.add_parser("lint", help="Run static code analysis")
    lint_parser.add_argument("path", help="File or directory to lint")
    lint_parser.add_argument("--pylint", action="store_true", default=True)
    lint_parser.add_argument("--flake8", action="store_true", default=True)
    lint_parser.add_argument("--mypy", action="store_true", default=True)
    lint_parser.add_argument("--bandit", action="store_true", default=True)
    lint_parser.add_argument("--fail-on-error", action="store_true", default=True)
    lint_parser.add_argument("-o", "--output", help="Save report to file")

    # Command: ai-review
    ai_parser = subparsers.add_parser("ai-review", help="AI-powered code review")
    ai_parser.add_argument("path", help="File or directory to review")
    ai_parser.add_argument("--llm", choices=["openai", "anthropic", "ollama"], default="openai")
    ai_parser.add_argument("--api-key", help="LLM API key")
    ai_parser.add_argument("--context", help="Additional context for review")
    ai_parser.add_argument("--format", choices=["markdown", "json", "html"], default="markdown")
    ai_parser.add_argument("-o", "--output", help="Save report to file")

    # Command: full (lint + ai-review)
    full_parser = subparsers.add_parser("full", help="Full review: lint + AI")
    full_parser.add_argument("path", help="File or directory to review")
    full_parser.add_argument("--llm", choices=["openai", "anthropic", "ollama"], default="openai")
    full_parser.add_argument("--api-key", help="LLM API key")
    full_parser.add_argument("-o", "--output", help="Save combined report")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "lint":
            # Static analysis
            print(f"Running static analysis on: {args.path}\n")

            linter = CodeLinter(
                enable_pylint=args.pylint,
                enable_flake8=args.flake8,
                enable_mypy=args.mypy,
                enable_bandit=args.bandit,
                fail_on_error=args.fail_on_error
            )

            # Lint file or directory
            path = Path(args.path)
            if path.is_file():
                result = linter.lint_file(args.path)
            else:
                result = linter.lint_directory(args.path)

            # Format report
            report = linter.format_report(result)
            print(report)

            # Save if requested
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(result.to_dict(), f, indent=2)
                print(f"\n✓ Report saved to: {args.output}")

            # Exit code
            sys.exit(0 if result.passed else 1)

        elif args.command == "ai-review":
            # AI code review
            print(f"Running AI code review on: {args.path}\n")

            reviewer = AICodeReviewer(
                llm_provider=LLMProvider[args.llm.upper()],
                api_key=args.api_key
            )

            # Review file or directory
            path = Path(args.path)
            if path.is_file():
                result = reviewer.review_file(args.path, context=args.context)
            else:
                result = reviewer.review_directory(args.path)

            # Generate report
            report = reviewer.generate_report(result, output_format=args.format)
            print(report)

            # Save if requested
            if args.output:
                with open(args.output, 'w') as f:
                    f.write(report)
                print(f"\n✓ Report saved to: {args.output}")

            # Exit code
            sys.exit(0 if result.approved else 1)

        elif args.command == "full":
            # Full review
            print("=== Full Code Review ===\n")

            # Step 1: Static analysis
            print("[1/2] Running static analysis...")
            linter = CodeLinter()

            path = Path(args.path)
            if path.is_file():
                lint_result = linter.lint_file(args.path)
            else:
                lint_result = linter.lint_directory(args.path)

            print(f"  ✓ Lint score: {lint_result.score}/10.0")
            print(f"  Issues: {lint_result.total_issues} ({lint_result.errors} errors)")

            # Step 2: AI review
            print("\n[2/2] Running AI code review...")
            reviewer = AICodeReviewer(
                llm_provider=LLMProvider[args.llm.upper()],
                api_key=args.api_key
            )

            if path.is_file():
                ai_result = reviewer.review_file(args.path)
            else:
                ai_result = reviewer.review_directory(args.path)

            print(f"  ✓ AI score: {ai_result.overall_score}/100")
            print(f"  Comments: {ai_result.total_comments}")

            # Combined report
            combined_report = f"""# Full Code Review Report

## Static Analysis
Score: {lint_result.score}/10.0
Status: {'✓ PASSED' if lint_result.passed else '✗ FAILED'}
Issues: {lint_result.total_issues}

{linter.format_report(lint_result)}

---

## AI Code Review
{reviewer.generate_report(ai_result, output_format="markdown")}
"""

            print("\n" + combined_report)

            # Save if requested
            if args.output:
                with open(args.output, 'w') as f:
                    f.write(combined_report)
                print(f"\n✓ Combined report saved to: {args.output}")

            # Exit code
            passed = lint_result.passed and ai_result.approved
            sys.exit(0 if passed else 1)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
