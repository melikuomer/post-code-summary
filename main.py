from google import genai
from google.genai.client import Client
from google.genai.types import (GenerateContentConfig, GenerationConfig,
                                HarmBlockThreshold, HarmCategory,
                                SafetySetting, Tool, ToolConfig)




import sys

def main():
    diff_input = sys.stdin.read()

    if not diff_input:
        print("No input received.")
        return

    # Process the diff as needed, here's an example of just printing file changes
    print("Processing git diff...\n")

    for line in diff_input.splitlines():
        if line.startswith('+++ ') or line.startswith('--- '):
            print(line)

if __name__ == "__main__":
    main()
