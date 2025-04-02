from google import genai
from google.genai.client import Client
from google.genai.types import (GenerateContentConfig, GenerationConfig,
                                HarmBlockThreshold, HarmCategory,
                                SafetySetting, ToolConfig)

from pre_commit_hooks.model import Artifact  # Your Pydantic model
from pre_commit_hooks.prompt import prompt   # Your system prompt string
from typing import List, Any

class App:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self._setup()

    def _setup(self):
        self._client: Client = genai.Client(api_key=self.api_key)
        self.generation_config = GenerationConfig(
            temperature=0.7,           # 0.0 is deterministic, 1.0 is most random
            top_p=0.95,                # Consider tokens with up to 95% cumulative probability
            top_k=40,                  # Consider the top 40 most likely tokens
            max_output_tokens=20192,    # Maximum tokens in the response
            stop_sequences=[],         # Add stop sequences if needed
        )
        self.safety_settings = [
            SafetySetting(category=HarmCategory.HARM_CATEGORY_HARASSMENT,
                          threshold=HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
            SafetySetting(category=HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                          threshold=HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
            SafetySetting(category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                          threshold=HarmBlockThreshold.BLOCK_ONLY_HIGH),
            SafetySetting(category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                          threshold=HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
        ]
        self.config = GenerateContentConfig(
            # System instructions as a list (can add more if needed)
            system_instruction=[prompt],
            response_schema=Artifact,       # Your Pydantic model for the expected response
            # tools=file_operations,
            response_mime_type='application/json',
            safety_settings=self.safety_settings,
            # tool_config= ToolConfig(function_calling_config=FunctionCallingConfig(mode=FunctionCallingConfigMode.ANY, allowed_function_names=["UpdateFile", "CreateFile"]))
        )
        self.chat = self._client.chats.create(
            model='gemini-2.0-flash-001',
            history=[],
            config=self.generation_config,
        )

    def set_generation_config(self, config: GenerationConfig):
        self.generation_config = config

    def set_safety_settings(self, safety_settings: List[SafetySetting]):
        self.safety_settings = safety_settings

    def set_tool_config(self, tool_config: ToolConfig):
        self.tool_config = tool_config

    def client(self):
        return self.client

    def __check_blocked(self, response: Any) -> bool:
        if hasattr(response, 'prompt_feedback') and response.prompt_feedback is not None:
            if response.prompt_feedback.block_reason:
                print(
                    f"Prompt blocked due to: {response.prompt_feedback.block_reason}")
                print(
                    f"Safety Ratings: {response.prompt_feedback.safety_ratings}")
                return True
        return False

    def run(self, value: str)-> Artifact:
        try:
            response = self.chat.send_message(message=value, config=self.config)
            # Check for safety issues (ensure prompt_feedback exists before accessing its attributes)
            if self.__check_blocked(response):
                pass
            # Print the response text (assuming the response text is available as .text)
            if response.text:
                return Artifact.model_validate_json(response.text)
            else:
                return "Error"
            # Save model parts on exit
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
