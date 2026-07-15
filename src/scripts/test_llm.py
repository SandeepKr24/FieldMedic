from src.agents.llm import generate

response = generate(
    "Say hello in exactly five words."
)

print(response)