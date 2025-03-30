from google import genai
from google.genai.client import Client
from google.genai.types import (GenerateContentConfig, GenerationConfig,
                                HarmBlockThreshold, HarmCategory,
                                SafetySetting, Tool, ToolConfig)




import sys
import os
def main():
    diff_input = sys.stdin.read()

    if not diff_input:
        print("No input received.")
        return

    from ui import display_artifact
    from client import App
    client = App(api_key=os.getenv('GOOGLE_API_KEY') or "")
    artifact = client.run(diff_input)
    display_artifact(artifact)

if __name__ == "__main__":
    main()
