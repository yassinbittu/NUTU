import os
import sys

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.append(BASE_DIR)

from app.services.rag_service import rag_service
from app.services.llm_service import llm_service


def ask_nutu(question: str):

    print("\n" + "=" * 70)
    print(f"USER: {question}")
    print("=" * 70)

    # Step 1: Retrieve relevant information
    results = rag_service.search(
        query=question,
        top_k=4
    )

    # Step 2: Build context for Groq
    context_parts = []

    for result in results:
        context_parts.append(result["text"])

    context = "\n\n---\n\n".join(context_parts)

    # Optional: see what RAG retrieved
    print("\nRAG CONTEXT:")
    print(context)

    print("\n" + "-" * 70)

    # Step 3: Send retrieved context to Groq
    answer = llm_service.generate_answer(
        question=question,
        context=context
    )

    print("\nNUTU:")
    print(answer)


if __name__ == "__main__":

    question = input("\nAsk NUTU: ")

    ask_nutu(question)