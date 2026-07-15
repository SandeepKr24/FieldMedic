from src.database import get_connection


def initialize_database():
    conn = get_connection()
    cur = conn.cursor()

    # Documents table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cases (
            id SERIAL PRIMARY KEY,
            symptoms TEXT NOT NULL,
            vitals JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Knowledge documents table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_documents (
            id SERIAL PRIMARY KEY,
            source TEXT NOT NULL,
            title TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Knowledge chunks table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_chunks (
            id SERIAL PRIMARY KEY,
            document_id INTEGER NOT NULL
                REFERENCES knowledge_documents(id)
                ON DELETE CASCADE,
            chunk_index INTEGER NOT NULL,
            chunk_text TEXT NOT NULL,
            embedding VECTOR(384)
        );
    """)

    conn.commit()

    cur.close()
    conn.close()