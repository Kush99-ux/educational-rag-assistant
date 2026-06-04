from src.llm.ollama_llm import (
    OllamaLLM
)

llm = OllamaLLM()

response = llm.generate(
    "What is 2 + 2?"
)

print(response)