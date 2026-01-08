import os
import sys
import argparse
import requests
import json
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Set stdout/stderr encoding to utf-8 explicitly for Windows to handle emojis
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Initialize colorama for Windows terminal support
init()

def setup_client():
    """Ollama doesn't strictly need a client setup like GenAI, but we'll check connectivity."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code != 200:
            print(f"{Fore.RED}Error: Ollama is not responding correctly.{Style.RESET_ALL}")
            sys.exit(1)
        return "http://localhost:11434/api/chat"
    except Exception as e:
        print(f"{Fore.RED}Error connecting to Ollama: {e}{Style.RESET_ALL}")
        print("Please ensure Ollama is running.")
        sys.exit(1)

def get_code_snippet(file_path, start_line=None, end_line=None):
    """Read the specific lines from the file."""
    try:
        if not os.path.exists(file_path):
            print(f"{Fore.RED}Error: File not found: {file_path}{Style.RESET_ALL}")
            sys.exit(1)
            
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        if start_line is None or end_line is None:
            snippet = "".join(lines)
        else:
            start_idx = max(0, int(start_line) - 1)
            end_idx = min(len(lines), int(end_line))
            snippet = "".join(lines[start_idx:end_idx])
        
        if not snippet.strip():
            print(f"{Fore.YELLOW}Warning: Selected text is empty.{Style.RESET_ALL}")
            sys.exit(0)
            
        return snippet
    except Exception as e:
        print(f"{Fore.RED}Error reading file: {e}{Style.RESET_ALL}")
        sys.exit(1)

def build_prompt(code_snippet):
    """Construct the analysis prompt."""
    return f"""
    Ты опытный старший QA-инженер по автоматизации (Senior QA Automation Engineer) и архитектор программного обеспечения.
    Проанализируй следующий фрагмент кода строго по этим 6 критериям. Отвечай на русском языке.
    
    КОД ДЛЯ АНАЛИЗА:
    ```
    {code_snippet}
    ```

    КРИТЕРИИ:
    1. НАДЕЖНОСТЬ И СТАБИЛЬНОСТЬ (Flaky tests, обработка асинхронности)
    2. ПРОВЕРКИ И ВЕРИФИКАЦИЯ (Четкие проверки, правильные методы assert)
    3. ЧИТАЕМОСТЬ И ПОНЯТНОСТЬ (Именование, логика, самодокументируемость)
    4. ХАРДКОД И ТЕСТОВЫЕ ДАННЫЕ (Магические строки, использование фикстур)
    5. ПОВТОРЯЕМОСТЬ И ПРИНЦИП DRY (Дублирование, вспомогательные функции)
    6. АРХИТЕКТУРА ТЕСТОВ (POM, структура, ответственность)

    ФОРМАТ ВЫВОДА:
    === РЕЗУЛЬТАТЫ КОД-РЕВЬЮ ===

    1. НАДЕЖНОСТЬ: [Статус: ✅ Отлично / ⚠️ Требует внимания / ❌ Критично]
    [Краткий анализ и конкретные рекомендации]

    2. ПРОВЕРКИ (ASSERTS): [Статус: ✅ / ⚠️ / ❌]
    [Краткий анализ и конкретные рекомендации]

    3. ЧИТАЕМОСТЬ: [Статус: ✅ / ⚠️ / ❌]
    [Краткий анализ и конкретные рекомендации]

    4. ХАРДКОД: [Статус: ✅ / ⚠️ / ❌]
    [Краткий анализ и конкретные рекомендации]

    5. ПРИНЦИП DRY: [Статус: ✅ / ⚠️ / ❌]
    [Краткий анализ и конкретные рекомендации]

    6. АРХИТЕКТУРА: [Статус: ✅ / ⚠️ / ❌]
    [Краткий анализ и конкретные рекомендации]

    ---
    ИТОГ:
    [Список из 3-х приоритетных действий]
    
    ОЦЕНКА: [X]/6 (Проходной балл)
    "

def analyze_code(endpoint, prompt):
    """Send request to Ollama."""
    print(f"{Fore.CYAN}Analyzing code with Ollama (gemma3)...{Style.RESET_ALL}")
    try:
        payload = {
            "model": "gemma3",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        return response.json()['message']['content']
    except Exception as e:
        print(f"{Fore.RED}Ollama Error: {e}{Style.RESET_ALL}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='AI Code Reviewer (Ollama)')
    parser.add_argument('--file', required=True, help='Path to the file')
    parser.add_argument('--start', type=int, default=None, help='Start line number')
    parser.add_argument('--end', type=int, default=None, help='End line number')
    
    args = parser.parse_args()
    
    endpoint = setup_client()
    code = get_code_snippet(args.file, args.start, args.end)
    
    if len(code) > 10000:
        print(f"{Fore.YELLOW}Warning: Selection is very long. Truncating.{Style.RESET_ALL}")
        code = code[:10000]

    prompt = build_prompt(code)
    result = analyze_code(endpoint, prompt)
    
    print("\n" + result)

if __name__ == "__main__":
    main()