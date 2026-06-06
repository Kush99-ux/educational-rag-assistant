# test_remote_llm.py

from src.llm.ollama_llm import (
    OllamaLLM
)

llm = OllamaLLM()

print(
    llm.generate(
        "Respond with exactly one word: Hello"
    )
)