import os
from openai import OpenAI
from typing import List, Dict
try:
    from services.embedding_service import embed_query, retrieve_chunks
except ImportError:  # pragma: no cover
    from src.services.embedding_service import embed_query, retrieve_chunks

# Load Azure OpenAI configuration
# Lazily initialized OpenAI client
client: OpenAI | None = None

def get_client() -> OpenAI:
    global client
    if client is None:
        client = OpenAI()
    return client

# Models and defaults
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4-turbo")
DEFAULT_K = int(os.getenv("KNN_K", 5))

SYSTEM_PROMPT = os.getenv(
    "SYSTEM_PROMPT",
    "You are an AI teaching assistant answering student questions in the style of the professor. Always cite the exact source ID of the material.",
)


def generate_answer(question: str, course_id: int, k: int = DEFAULT_K) -> Dict:
    """
    Generate an answer for a student question given a course ID.
    Returns a dict with 'answer' text and 'citations' list of chunk IDs.
    """
    # 1. Embed the query
    query_embedding = embed_query(question)

    # 2. Retrieve relevant chunks
    chunks = retrieve_chunks(course_id, query_embedding, k)

    # 3. Assemble prompt with citations
    snippet_texts: List[str] = [f"[ID {row['id']}] {row['text']}" for row in chunks]
    context = "\n".join(snippet_texts)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Here are relevant snippets:\n{context}\n\nQuestion: {question}"},
    ]

    # 4. Call Chat Completions API (responses API if streaming desired)
    if os.getenv("MOCK_OPENAI") == "1":
        answer = "This is a mocked answer. [ID 1][ID 2]"
    else:
        response = get_client().chat.completions.create(
            model=CHAT_MODEL,
            messages=messages,
            temperature=0.2,
        )
        answer = response.choices[0].message.content

    # 5. Return answer and citations
    citations: List[int] = [row["id"] for row in chunks]
    return {"answer": answer, "citations": citations}