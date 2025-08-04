import azure.functions as func
import json
from services.qa_service import generate_answer
from services.validation_service import validate_int, validate_str
from db import SessionLocal
from models.models import QuestionLog


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        data = req.get_json()
        course_id = validate_int(data.get("course_id"), "course_id")
        question = validate_str(data.get("question"), "question")
    except ValueError as ve:
        return func.HttpResponse(str(ve), status_code=400)
    except Exception:
        return func.HttpResponse("Invalid JSON body", status_code=400)

    try:
        result = generate_answer(question, course_id)
    except Exception as e:
        return func.HttpResponse(f"Error generating answer: {e}", status_code=500)

    # Persist question log for review
    session = SessionLocal()
    try:
        qlog = QuestionLog(user_id=1, question=question, answer=result["answer"], citations=result.get("citations"))
        session.add(qlog)
        session.commit()
    finally:
        session.close()

    return func.HttpResponse(
        json.dumps(result),
        mimetype="application/json",
        status_code=200,
    )