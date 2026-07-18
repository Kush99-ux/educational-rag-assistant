import ollama

from src.core.base_llm import BaseLLM


import ollama

from src.core.base_llm import BaseLLM
from src.core.settings import load_config


class OllamaLLM(BaseLLM):

    def __init__(self):

        config = load_config()

        self.model = config["llm"]["model"]
        self.temperature = config["llm"]["temperature"]
        self.num_predict = config["llm"]["num_predict"]
        self.num_ctx = config["llm"]["num_ctx"]

        self.client = ollama.Client(
            host="http://localhost:11434"
        )

    def generate(
        self,
        prompt: str
    ) -> str:

        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": self.temperature,
                "num_predict": self.num_predict,
                "num_ctx": self.num_ctx
            }
        )

        return response["message"]["content"]
