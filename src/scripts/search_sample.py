from src.agents.rag import search_knowledge

results = search_knowledge(
    "What should I do if someone has severe chest pain?"
)

for result in results:
    print(result)