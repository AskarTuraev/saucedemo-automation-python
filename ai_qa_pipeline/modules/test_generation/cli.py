"""
Test Generation CLI
===================

Command-line интерфейс для генерации тест-сценариев.
"""

import argparse
import json
import sys
from pathlib import Path

from .generator import TestScenarioGenerator
from .llm_client import LLMProvider


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="AI-Powered Test Scenario Generator"
    )

    parser.add_argument(
        "requirements",
        help="Business requirements (text or file path)"
    )

    parser.add_argument(
        "-o", "--output",
        default="test_scenarios.json",
        help="Output JSON file path"
    )

    parser.add_argument(
        "-p", "--provider",
        choices=["openai", "anthropic", "ollama"],
        default="openai",
        help="LLM provider"
    )

    parser.add_argument(
        "-m", "--model",
        help="Specific model name (optional)"
    )

    parser.add_argument(
        "--api-key",
        help="API key for LLM provider"
    )

    parser.add_argument(
        "-f", "--file",
        action="store_true",
        help="Treat requirements as file path"
    )

    parser.add_argument(
        "--analyze-only",
        action="store_true",
        help="Only analyze requirements without generating scenarios"
    )

    parser.add_argument(
        "--edge-cases",
        help="Generate edge cases for specific scenario"
    )

    parser.add_argument(
        "--optimize",
        help="Optimize existing scenarios from JSON file"
    )

    args = parser.parse_args()

    try:
        # Инициализация генератора
        provider = LLMProvider[args.provider.upper()]
        generator = TestScenarioGenerator(
            llm_provider=provider,
            model=args.model,
            api_key=args.api_key
        )

        # Режим оптимизации
        if args.optimize:
            print(f"Loading scenarios from {args.optimize}...")
            scenarios = generator.import_from_json(args.optimize)
            print(f"Loaded {len(scenarios)} scenarios")

            print("\nAnalyzing and optimizing...")
            optimization = generator.optimize_scenarios(scenarios)

            print("\n=== Optimization Results ===")
            print(json.dumps(optimization, indent=2))
            sys.exit(0)

        # Режим граничных случаев
        if args.edge_cases:
            print(f"Generating edge cases for: {args.edge_cases}")
            edge_cases = generator.suggest_edge_cases(
                feature_name=args.requirements,
                base_scenario=args.edge_cases
            )

            print("\n=== Edge Cases ===")
            print(json.dumps(edge_cases, indent=2))
            sys.exit(0)

        # Загрузка требований
        if args.file:
            if not Path(args.requirements).exists():
                print(f"Error: File not found: {args.requirements}", file=sys.stderr)
                sys.exit(1)

            with open(args.requirements, 'r', encoding='utf-8') as f:
                requirements = f.read()
            print(f"Loaded requirements from: {args.requirements}")
        else:
            requirements = args.requirements

        # Режим анализа
        if args.analyze_only:
            print("\nAnalyzing requirements...")
            analysis = generator.analyze_requirements(requirements)

            print("\n=== Requirements Analysis ===")
            print(f"Feature: {analysis.feature_name}")
            print(f"\nUser Stories ({len(analysis.user_stories)}):")
            for story in analysis.user_stories:
                print(f"  - {story}")

            print(f"\nAcceptance Criteria ({len(analysis.acceptance_criteria)}):")
            for criteria in analysis.acceptance_criteria:
                print(f"  - {criteria}")

            print(f"\nEdge Cases ({len(analysis.edge_cases)}):")
            for edge_case in analysis.edge_cases:
                print(f"  - {edge_case}")

            print(f"\nSuggested Scenarios ({len(analysis.suggested_scenarios)}):")
            for scenario in analysis.suggested_scenarios:
                print(f"  - {scenario}")

            # Сохранение анализа
            analysis_file = Path(args.output).with_suffix('.analysis.json')
            with open(analysis_file, 'w', encoding='utf-8') as f:
                json.dump(analysis.to_dict(), f, indent=2, ensure_ascii=False)
            print(f"\nAnalysis saved to: {analysis_file}")

        else:
            # Полная генерация сценариев
            print("\nGenerating test scenarios...")
            scenarios = generator.generate_from_requirements(requirements)

            print(f"\n✓ Generated {len(scenarios)} test scenarios")

            # Вывод summary
            print("\n=== Summary ===")
            priorities = {}
            types = {}
            total_time = 0

            for scenario in scenarios:
                priorities[scenario.priority.value] = priorities.get(scenario.priority.value, 0) + 1
                types[scenario.test_type.value] = types.get(scenario.test_type.value, 0) + 1
                total_time += scenario.estimated_time or 0

            print(f"Total scenarios: {len(scenarios)}")
            print(f"Estimated time: {total_time}s (~{total_time//60}m)")
            print(f"\nBy priority:")
            for priority, count in sorted(priorities.items()):
                print(f"  {priority}: {count}")
            print(f"\nBy type:")
            for test_type, count in sorted(types.items()):
                print(f"  {test_type}: {count}")

            # Сохранение
            generator.export_to_json(scenarios, args.output)
            print(f"\n✓ Scenarios saved to: {args.output}")

            # Вывод превью
            if scenarios:
                print(f"\n=== Preview: {scenarios[0].title} ===")
                print(f"Description: {scenarios[0].description}")
                print(f"Priority: {scenarios[0].priority.value}")
                print(f"Steps: {len(scenarios[0].steps)}")
                print(f"Tags: {', '.join(scenarios[0].tags)}")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
