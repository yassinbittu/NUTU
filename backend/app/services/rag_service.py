import os
import chromadb

from app.services.embedding_service import embedding_service


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

VECTOR_STORE_DIR = os.path.join(
    BASE_DIR,
    "vector_store"
)


class RAGService:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path=VECTOR_STORE_DIR
        )

        self.collection = self.client.get_collection(
            name="nutu_knowledge"
        )

    def search(self, query: str, top_k: int = 3):

        query_embedding = (
            embedding_service
            .create_embedding(query)
        )

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=[
                "documents",
                "metadatas",
                "distances"
            ]
        )

        retrieved_results = []

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances
        ):

            retrieved_results.append({
                "text": document,
                "metadata": metadata,
                "distance": distance,
                "similarity": 1 - distance
            })

        return retrieved_results


rag_service = RAGService()