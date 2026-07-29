import json
import os
import sys
import shutil
import chromadb


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.append(BASE_DIR)


from app.services.embedding_service import embedding_service
from app.utils.text_chunker import create_chunks


DATA_DIR = os.path.join(BASE_DIR, "data")

VECTOR_STORE_DIR = os.path.join(
    BASE_DIR,
    "vector_store"
)


def load_knowledge():

    all_chunks = []

    filenames = sorted(os.listdir(DATA_DIR))

    for filename in filenames:

        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(
            DATA_DIR,
            filename
        )

        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        chunks = create_chunks(
            filename,
            data
        )

        all_chunks.extend(chunks)

        print(
            f"{filename}: {len(chunks)} chunks"
        )

    return all_chunks


def reset_vector_store():

    if os.path.exists(VECTOR_STORE_DIR):

        shutil.rmtree(
            VECTOR_STORE_DIR
        )

        print(
            "Old vector store removed."
        )

    os.makedirs(
        VECTOR_STORE_DIR,
        exist_ok=True
    )


def create_vector_store():

    chunks = load_knowledge()

    print(
        f"\nTotal chunks: {len(chunks)}"
    )

    reset_vector_store()

    client = chromadb.PersistentClient(
        path=VECTOR_STORE_DIR
    )

    collection = client.get_or_create_collection(
        name="nutu_knowledge",
        metadata={
            "hnsw:space": "cosine"
        }
    )

    for index, chunk in enumerate(chunks):

        text = chunk["text"]

        embedding = (
            embedding_service
            .create_embedding(text)
        )

        metadata = {
            key: str(value)
            for key, value in chunk.items()
            if key != "text"
        }

        collection.add(
            ids=[
                f"nutu_{index}"
            ],
            documents=[
                text
            ],
            embeddings=[
                embedding
            ],
            metadatas=[
                metadata
            ]
        )

        print(
            f"Added chunk {index + 1}/{len(chunks)} "
            f"[{metadata.get('category')}]"
        )

    print(
        "\nNUTU vector database created successfully!"
    )

    print(
        f"Total vectors: {collection.count()}"
    )


if __name__ == "__main__":
    create_vector_store()