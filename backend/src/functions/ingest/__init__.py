import azure.functions as func
import json
import os
from services.validation_service import validate_int, validate_str
from services.document_parser import parse_document
from db import SessionLocal
from models.models import Chunk
from openai import OpenAI
import tiktoken

# Lazily initialized OpenAI client. Tests may monkeypatch this symbol.
client: OpenAI | None = None

def get_client() -> OpenAI:
    global client
    if client is None:
        client = OpenAI()
    return client

# Configure embedding model
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
# Initialize tokenizer for token counting
tokenizer = tiktoken.get_encoding("cl100k_base")

# Maximum tokens per chunk
MAX_TOKENS = int(os.getenv("CHUNK_SIZE", 500))


def chunk_text(text: str, max_tokens: int):
    tokens = tokenizer.encode(text)
    for i in range(0, len(tokens), max_tokens):
        yield tokenizer.decode(tokens[i : i + max_tokens])


def main(req: func.HttpRequest) -> func.HttpResponse:
    # Enforce API key authentication
    secret = os.getenv("API_KEY_SECRET")
    provided = req.headers.get("x-api-key")
    if provided != secret:
        return func.HttpResponse("Unauthorized", status_code=401)
    try:
        data = req.get_json()
        course_id = validate_int(data.get("course_id"), "course_id")
        file_path = validate_str(data.get("path"), "path")
    except ValueError as ve:
        return func.HttpResponse(str(ve), status_code=400)
    except Exception:
        return func.HttpResponse("Invalid JSON body", status_code=400)

    try:
        text = parse_document(file_path)
    except FileNotFoundError:
        return func.HttpResponse(f"File not found: {file_path}", status_code=404)

    session = SessionLocal()
    created = 0
    try:
        for chunk in chunk_text(text, MAX_TOKENS):
            # generate embedding
            if os.getenv("MOCK_OPENAI") == "1":
                embedding = [0.1, 0.2, 0.3]
            else:
                resp = get_client().embeddings.create(input=chunk, model=EMBEDDING_MODEL)
                embedding = resp.data[0].embedding
            # persist chunk
            db_chunk = Chunk(course_id=course_id, text=chunk, embedding=embedding)
            session.add(db_chunk)
            created += 1
        session.commit()
    except Exception as e:
        session.rollback()
        return func.HttpResponse(f"Error during ingestion: {e}", status_code=500)
    finally:
        session.close()

    return func.HttpResponse(
        json.dumps({"course_id": course_id, "chunks_created": created}),
        mimetype="application/json",
        status_code=200,
    )