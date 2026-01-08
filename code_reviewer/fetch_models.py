import os
import sys
from google import genai
from dotenv import load_dotenv

def list_models():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env file.")
        return

    try:
        # We use a simple client without a specific model to list models
        client = genai.Client(api_key=api_key)
        print("--- Available Models ---")
        # client.models.list() returns a pager
        for model in client.models.list():
            # Check if generate_content is supported
            if 'generateContent' in model.supported_generation_methods:
                print(f"Name: {model.name}")
                print(f"Display Name: {model.display_name}")
                print("-" * 20)
    except Exception as e:
        print(f"Error fetching models: {e}")

if __name__ == "__main__":
    list_models()
