import psycopg
from pgvector.psycopg import register_vector
from pgvector import Vector
from psycopg.types.json import Jsonb
from src.config import DATABASE_URL

# DATABASE_URL = (
#     "postgresql://postgres:postgres@postgres:5432/fieldmedic"
# )


def get_connection():
    conn = psycopg.connect(DATABASE_URL)

    # Register the pgvector type with this connection
    register_vector(conn)

    return conn


def insert_case(symptoms: str, vitals: dict | None) -> int:
    """
    Inserts a patient case into the database and returns its ID.
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO cases (symptoms, vitals)
        VALUES (%s, %s)
        RETURNING id;
        """,
        (
            symptoms,
            Jsonb(vitals)
        )
    )

    case_id = cur.fetchone()[0]

    conn.commit()

    cur.close()
    conn.close()

    return case_id


def insert_knowledge_document(
    source: str,
    title: str | None = None
) -> int:
    """
    Inserts a knowledge document and returns its ID.
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO knowledge_documents (
            source,
            title
        )
        VALUES (%s, %s)
        RETURNING id;
        """,
        (
            source,
            title
        )
    )

    document_id = cur.fetchone()[0]

    conn.commit()

    cur.close()
    conn.close()

    return document_id


def insert_knowledge_chunk(
    document_id: int,
    chunk_index: int,
    chunk_text: str,
    embedding: list[float]
):
    """
    Inserts one chunk and its embedding.
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO knowledge_chunks (
            document_id,
            chunk_index,
            chunk_text,
            embedding
        )
        VALUES (%s, %s, %s, %s);
        """,
        (
            document_id,
            chunk_index,
            chunk_text,
            Vector(embedding),
        )
    )

    conn.commit()

    cur.close()
    conn.close()

def retrieve_chunks(
    query_embedding: list[float],
    top_k: int = 5
):
    """
    Returns the most similar knowledge chunks.
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            chunk_text,
            embedding <=> %s::vector AS distance
        FROM knowledge_chunks
        ORDER BY embedding <=> %s::vector
        LIMIT %s;
        """,
        (
            Vector(query_embedding),
            Vector(query_embedding),
            top_k,
        ),
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows