import os
import sys
import argparse
import google.generativeai as genai
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Initialize colorama for Windows terminal support
init()

def setup_api():
    """Load API key and configure Gemini."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print(f"{Fore.RED}Error: GEMINI_API_KEY not found in .env file.{Style.RESET_ALL}")
        print("Please create a .env file based on .env.example")
        sys.exit(1)
        
    genai.configure(api_key=api_key)
    # Using gemini-1.5-flash for speed and efficiency for code tasks
    return genai.GenerativeModel('gemini-1.5-flash')

def get_code_snippet(file_path, start_line, end_line):
    """Read the specific lines from the file."""
    try:
        if not os.path.exists(file_path):
            print(f"{Fore.RED}Error: File not found: {file_path}{Style.RESET_ALL}")
            sys.exit(1)
            
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Adjust for 0-based indexing vs 1-based editor lines
        # VSCode sends 1-based line numbers usually, but let's be safe
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
    You are an expert Senior QA Automation Engineer and Software Architect.
    Analyze the following code snippet strictly according to these 6 criteria.
    
    CODE TO ANALYZE:
    ```
    {code_snippet}
    ```

    CRITERIA:
    1. RELIABILITY & STABILITY (Flaky tests, async handling)
    2. ASSERTS & VERIFIABILITY (Clear checks, correct assertion methods)
    3. READABILITY & INTENT (Naming, logic, self-documenting)
    4. HARDCODE & TEST DATA (Magic strings, fixture usage)
    5. REPEATABILITY & DRY (Duplication, helper functions)
    6. TEST ARCHITECTURE (POM, structure, responsibility)

    OUTPUT FORMAT:
    Provide the response in the following strict format (do not use markdown code blocks for the whole response, just standard text/markdown):

    === CODE REVIEW RESULTS ===

    1. RELIABILITY: [Status: ✅ Excellent / ⚠️ Needs Attention / ❌ Critical]
    [Brief analysis and specific recommendations]

    2. ASSERTS: [Status: ✅ / ⚠️ / ❌]
    [Brief analysis and specific recommendations]

    3. READABILITY: [Status: ✅ / ⚠️ / ❌]
    [Brief analysis and specific recommendations]

    4. HARDCODE: [Status: ✅ / ⚠️ / ❌]
    [Brief analysis and specific recommendations]

    5. DRY PRINCIPLES: [Status: ✅ / ⚠️ / ❌]
    [Brief analysis and specific recommendations]

    6. ARCHITECTURE: [Status: ✅ / ⚠️ / ❌]
    [Brief analysis and specific recommendations]

    ---
    SUMMARY:
    [Bullet points with top 3 priority actions]
    
    SCORE: [X]/6 Passing
    """

def analyze_code(model, prompt):
    """Send request to Gemini."""
    print(f"{Fore.CYAN}Analyzing code with Gemini...{Style.RESET_ALL}")
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"{Fore.RED}API Error: {e}{Style.RESET_ALL}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Gemini Code Reviewer')
    parser.add_argument('--file', required=True, help='Path to the file')
    parser.add_argument('--start', required=True, type=int, help='Start line number')
    parser.add_argument('--end', required=True, type=int, help='End line number')
    
    args = parser.parse_args()
    
    model = setup_api()
    code = get_code_snippet(args.file, args.start, args.end)
    
    # Simple length check
    if len(code) > 10000:
        print(f"{Fore.YELLOW}Warning: Selection is very long ({len(code)} chars). Truncating for analysis.{Style.RESET_ALL}")
        code = code[:10000]

    prompt = build_prompt(code)
    result = analyze_code(model, prompt)
    
    print("\n" + result)

if __name__ == "__main__":
    main()
