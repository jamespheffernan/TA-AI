import azure.functions as func
import json
from services.qa_service import generate_answer


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        data = req.get_json()
    except Exception:
        return func.HttpResponse("Invalid JSON body", status_code=400)

    course_id = data.get("course_id")
    question = data.get("question")
    if course_id is None or not question:
        return func.HttpResponse("Missing course_id or question", status_code=400)

    try:
        result = generate_answer(question, course_id)
    except Exception as e:
        return func.HttpResponse(f"Error generating answer: {e}", status_code=500)

    return func.HttpResponse(
        json.dumps(result),
        mimetype="application/json",
        status_code=200,
    )