"""
PII Detection CLI
=================

Command-line интерфейс для работы с PII детекцией.
"""

import argparse
import json
import sys
from pathlib import Path

from .pipeline import PIIPipeline


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="PII Detection and Masking Tool"
    )

    parser.add_argument(
        "input",
        help="Input text or file path"
    )

    parser.add_argument(
        "-o", "--output",
        help="Output file path for masked content"
    )

    parser.add_argument(
        "-s", "--strategy",
        choices=["replace", "hash", "fake", "redact"],
        default="replace",
        help="Masking strategy"
    )

    parser.add_argument(
        "-t", "--threshold",
        type=float,
        default=0.5,
        help="Detection confidence threshold (0.0-1.0)"
    )

    parser.add_argument(
        "-f", "--file",
        action="store_true",
        help="Treat input as file path"
    )

    parser.add_argument(
        "-r", "--report",
        action="store_true",
        help="Generate PII detection report"
    )

    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Only check for PII without masking"
    )

    args = parser.parse_args()

    # Инициализация пайплайна
    pipeline = PIIPipeline(
        score_threshold=args.threshold,
        masking_strategy=args.strategy
    )

    try:
        if args.file:
            # Обработка файла
            if not Path(args.input).exists():
                print(f"Error: File not found: {args.input}", file=sys.stderr)
                sys.exit(1)

            result = pipeline.process_file(
                args.input,
                output_path=args.output,
                save_report=args.report
            )

            if args.check_only:
                print(json.dumps({
                    "pii_found": result["pii_found"],
                    "pii_count": result["pii_count"],
                    "pii_types": result["pii_types"]
                }, indent=2))
            else:
                print(f"✓ Processed: {args.input}")
                print(f"  PII found: {result['pii_count']}")
                print(f"  Types: {', '.join(result['pii_types'])}")
                if args.output:
                    print(f"  Masked output: {args.output}")

        else:
            # Обработка текста
            result = pipeline.process_text(args.input, return_entities=True)

            if args.check_only:
                print(json.dumps({
                    "pii_found": result["pii_found"],
                    "pii_count": result["pii_count"],
                    "pii_types": result["pii_types"],
                    "entities": result["entities"]
                }, indent=2))
            else:
                print("\n=== Masked Text ===")
                print(result["masked_text"])
                print(f"\n✓ Found {result['pii_count']} PII entities")
                print(f"  Types: {', '.join(result['pii_types'])}")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
