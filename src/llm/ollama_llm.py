import ollama

from src.core.base_llm import BaseLLM


class OllamaLLM(
    BaseLLM
):

    def __init__(
        self,
        model: str = "llama3.1:8b"
    ):
        self.model = model

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
            ]
        )

        return response[
            "message"
        ][
            "content"
        ]