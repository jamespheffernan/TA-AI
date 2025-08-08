import os
from openai import OpenAI
from sqlalchemy import text
try:
    from db import SessionLocal
except ImportError:  # pragma: no cover
    from src.db import SessionLocal

# Lazily initialized OpenAI client. Tests may monkeypatch this symbol.
client: OpenAI | None = None


def get_client() -> OpenAI:
    global client
    if client is None:
        client = OpenAI()
    return client

# Embedding model
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
# Number of results
DEFAULT_K = int(os.getenv("KNN_K", 5))


def embed_query(query: str) -> list[float]:
    """Generate embedding for the input query using OpenAI.

    When MOCK_OPENAI=1, returns a deterministic small vector to avoid external calls.
    """
    if os.getenv("MOCK_OPENAI") == "1":
        return [0.1, 0.2, 0.3]

    response = get_client().embeddings.create(input=query, model=EMBEDDING_MODEL)
    return response.data[0].embedding


def retrieve_chunks(course_id: int, query_embedding: list[float], k: int = DEFAULT_K) -> list[dict]:
    """Retrieve the top-k similar chunks.

    - Uses pgvector cosine distance when connected to Postgres.
    - Falls back to a simple top-k by ID for SQLite or when MOCK_OPENAI is enabled.
    """
    session = SessionLocal()
    try:
        use_simple = os.getenv("MOCK_OPENAI") == "1"
        try:
            dialect_name = session.bind.dialect.name  # type: ignore[attr-defined]
            if dialect_name == "sqlite":
                use_simple = True
        except Exception:
            pass

        if use_simple:
            # Simple fallback: return up to k chunks for course_id with dummy distance
            try:
                # Lazy import to avoid circular dependency
                from models.models import Chunk  # type: ignore
            except Exception:
                from src.models.models import Chunk  # type: ignore
            results = (
                session.query(Chunk)
                .filter(Chunk.course_id == course_id)
                .limit(k)
                .all()
            )
            return [{"id": c.id, "text": c.text, "distance": 0.0} for c in results]

        # Postgres with pgvector path
        sql = text(
            "SELECT id, text, embedding <-> :query_embedding AS distance "
            "FROM chunks "
            "WHERE course_id = :course_id "
            "ORDER BY distance "
            "LIMIT :k"
        )
        result = session.execute(
            sql,
            {"query_embedding": query_embedding, "course_id": course_id, "k": k},
        )
        mapped = result.mappings()
        rows = mapped.all() if hasattr(mapped, "all") else list(mapped)
        return rows
    finally:
        session.close()