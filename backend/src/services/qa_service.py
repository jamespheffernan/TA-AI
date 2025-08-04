import os
import openai
from typing import List, Dict
from services.embedding_service import embed_query, retrieve_chunks

# Load Azure OpenAI configuration
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
openai.api_type = os.getenv("OPENAI_API_TYPE", "azure")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT", os.getenv("OPENAI_API_BASE"))
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION", os.getenv("OPENAI_API_VERSION"))

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

    # 4. Call ChatCompletion
    response = openai.ChatCompletion.create(
        model=CHAT_MODEL,
        messages=messages,
        temperature=0.2,
    )
    answer = response["choices"][0]["message"]["content"]

    # 5. Return answer and citations
    citations: List[int] = [row["id"] for row in chunks]
    return {"answer": answer, "citations": citations}