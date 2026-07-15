from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.database import (
    insert_case,
    insert_knowledge_document,
    insert_knowledge_chunk,
    retrieve_chunks,
)

from src.config import EMBEDDING_MODEL

# Load the embedding model once when the application starts
# embedding_model = SentenceTransformer(
#     "sentence-transformers/all-MiniLM-L6-v2"
# )

embedding_model = SentenceTransformer(EMBEDDING_MODEL)

def ingest_case(symptoms: str, vitals: dict | None = None):
    """
    Stores a patient case.
    """

    case_id = insert_case(symptoms, vitals)

    return {
        "status": "accepted",
        "case_id": case_id,
    }


def ingest_knowledge_document(
    source: str,
    title: str,
    text: str,
):
    """
    Splits a knowledge document into chunks,
    generates embeddings,
    and stores everything in PostgreSQL.
    """

    document_id = insert_knowledge_document(
        source=source,
        title=title,
    )

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
    )

    chunks = text_splitter.split_text(text)

    for index, chunk in enumerate(chunks):

        embedding = embedding_model.encode(chunk)

        insert_knowledge_chunk(
            document_id=document_id,
            chunk_index=index,
            chunk_text=chunk,
            embedding=embedding,
        )

    return {
        "document_id": document_id,
        "chunks": len(chunks),
    }

def search_knowledge(
    question: str,
    top_k: int = 5,
):
    """
    Searches the knowledge base using semantic similarity.
    """

    query_embedding = embedding_model.encode(question)

    results = retrieve_chunks(
        query_embedding,
        top_k,
    )

    return [
        # {
        #     "chunk": row[0],
        #     "distance": float(row[1]),
        # }
        row[0]
        for row in results
    ]