import os
import sys


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.append(BASE_DIR)


from app.services.rag_service import rag_service


def test_query(query):

    print("\n" + "=" * 70)
    print(f"QUESTION: {query}")
    print("=" * 70)

    results = rag_service.search(
        query=query,
        top_k=3
    )

    for index, result in enumerate(results, start=1):

        print(f"\nRESULT {index}")
        print(
            f"Source: "
            f"{result['metadata'].get('source')}"
        )
        print(
            f"Category: "
            f"{result['metadata'].get('category')}"
        )
        print(
            f"Similarity: "
            f"{result['similarity']:.4f}"
        )

        print("\nRetrieved text:")
        print(result["text"])

        print("-" * 70)


if __name__ == "__main__":

    questions = [
    # Direct questions
    "What skills does Yassin have?",
    "Tell me about Yassin's projects",
    "Where did Yassin study?",
    "Does Yassin know Python?",

    # Indirect Yassin questions
    "What kind of developer is Yassin?",
    "Tell me more about Yassin",
    "What does Yassin do?",
    "What technologies does he work with?",
    "Does he have experience with databases?",
    "Has he worked with React?",
    "What has he built?",
    "What is his educational background?",
    "Does he know artificial intelligence?",
    "What development tools has he used?",
    "Where has he worked?",

    # Unrelated questions
    "Tell me a joke",
    "What is the time now?",
    "Who is Virat Kohli?",
    "How to make biryani?",
    "What is today's weather?",
    "Write Python code to reverse a string",
    "Who is Elon Musk?"
]

    for question in questions:
        test_query(question)