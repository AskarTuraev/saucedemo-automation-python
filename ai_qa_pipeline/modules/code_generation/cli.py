"""
Code Generation CLI
===================

Command-line интерфейс для генерации автотестов из JSON-контрактов.
"""

import argparse
import json
import sys
from pathlib import Path

from .code_generator import CodeGenerator, TestFramework
from .json_contract import JSONContractGenerator
from ..test_generation import TestScenarioGenerator
from ..test_generation.llm_client import LLMProvider


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="AI-Powered Test Code Generator"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: generate (from JSON contracts)
    gen_parser = subparsers.add_parser("generate", help="Generate test code from JSON contracts")
    gen_parser.add_argument("contracts", help="Path to JSON contracts file")
    gen_parser.add_argument("-o", "--output", default="generated_tests", help="Output directory")
    gen_parser.add_argument("-f", "--framework", choices=["playwright", "selenium"], default="playwright")

    # Command: full-pipeline (requirements → scenarios → contracts → code)
    full_parser = subparsers.add_parser("full", help="Full pipeline: requirements to code")
    full_parser.add_argument("requirements", help="Business requirements file")
    full_parser.add_argument("-o", "--output", default="generated_tests", help="Output directory")
    full_parser.add_argument("--llm", choices=["openai", "anthropic", "ollama"], default="openai")
    full_parser.add_argument("--api-key", help="LLM API key")
    full_parser.add_argument("--base-url", required=True, help="Base URL of application")

    # Command: create-contracts (scenarios → contracts)
    contract_parser = subparsers.add_parser("contracts", help="Create JSON contracts from scenarios")
    contract_parser.add_argument("scenarios", help="Path to test scenarios JSON")
    contract_parser.add_argument("-o", "--output", default="test_contracts.json")
    contract_parser.add_argument("--base-url", help="Base URL of application")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "generate":
            # Генерация кода из контрактов
            print(f"Loading contracts from: {args.contracts}")

            generator = CodeGenerator(
                framework=TestFramework[args.framework.upper()],
                output_dir=args.output
            )

            # Загрузка контрактов
            contract_gen = JSONContractGenerator()
            contracts = contract_gen.import_from_json(args.contracts)

            print(f"Loaded {len(contracts)} test contracts")

            # Генерация тестов
            print("\nGenerating test code...")
            generated_files = generator.generate_batch(contracts)

            print(f"\n✓ Generated {len(generated_files)} test files:")
            for file_path in generated_files:
                print(f"  - {file_path}")

            # Генерация conftest.py
            if contracts:
                conftest = generator.generate_conftest(
                    base_url=contracts[0].to_dict().get("base_url", "http://localhost"),
                    browser=contracts[0].browser,
                    headless=contracts[0].headless
                )
                print(f"\n✓ Generated conftest: {conftest}")

        elif args.command == "contracts":
            # Создание контрактов из сценариев
            print(f"Loading scenarios from: {args.scenarios}")

            with open(args.scenarios, 'r') as f:
                data = json.load(f)

            from ..test_generation.models import TestScenario
            scenarios = []
            for scenario_data in data.get("test_scenarios", []):
                scenarios.append(TestScenario.from_dict(scenario_data))

            print(f"Loaded {len(scenarios)} scenarios")

            # Генерация контрактов
            print("\nGenerating JSON contracts...")
            contract_gen = JSONContractGenerator()
            contracts = contract_gen.generate_batch_contracts(
                scenarios,
                base_url=args.base_url
            )

            # Экспорт
            contract_gen.export_to_json(contracts, args.output)
            print(f"\n✓ Exported {len(contracts)} contracts to: {args.output}")

        elif args.command == "full":
            # Полный пайплайн
            print("=== Full AI-Driven QA Pipeline ===\n")

            # Step 1: Load requirements
            print(f"[1/4] Loading requirements from: {args.requirements}")
            with open(args.requirements, 'r') as f:
                requirements = f.read()

            # Step 2: Generate scenarios
            print("[2/4] Generating test scenarios with LLM...")
            scenario_gen = TestScenarioGenerator(
                llm_provider=LLMProvider[args.llm.upper()],
                api_key=args.api_key
            )
            scenarios = scenario_gen.generate_from_requirements(requirements)
            print(f"  ✓ Generated {len(scenarios)} test scenarios")

            # Step 3: Create JSON contracts
            print("[3/4] Creating JSON contracts...")
            contract_gen = JSONContractGenerator()
            contracts = contract_gen.generate_batch_contracts(
                scenarios,
                base_url=args.base_url
            )
            print(f"  ✓ Created {len(contracts)} test contracts")

            # Step 4: Generate code
            print("[4/4] Generating Playwright test code...")
            code_gen = CodeGenerator(
                framework=TestFramework.PLAYWRIGHT,
                output_dir=args.output
            )
            generated_files = code_gen.generate_batch(contracts)
            conftest = code_gen.generate_conftest(
                base_url=args.base_url,
                browser="chromium",
                headless=False
            )

            print(f"\n✓ Pipeline complete!")
            print(f"  - Scenarios: {len(scenarios)}")
            print(f"  - Contracts: {len(contracts)}")
            print(f"  - Test files: {len(generated_files)}")
            print(f"  - Output dir: {args.output}")

            print(f"\nGenerated files:")
            for file_path in generated_files[:5]:  # Show first 5
                print(f"  - {file_path}")
            if len(generated_files) > 5:
                print(f"  ... and {len(generated_files) - 5} more")

            print(f"\nRun tests:")
            print(f"  cd {args.output}")
            print(f"  pytest -v")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
