import azure.functions as func
import json
from db import SessionLocal
from models.models import QuestionLog, Feedback
import os


def main(req: func.HttpRequest) -> func.HttpResponse:
    # Enforce API key authentication
    secret = os.getenv("API_KEY_SECRET")
    provided = req.headers.get("x-api-key")
    if provided != secret:
        return func.HttpResponse("Unauthorized", status_code=401)
    session = SessionLocal()
    try:
        if method == 'GET':
            course_id = req.params.get('course_id')
            query = session.query(QuestionLog)
            logs = query.all()
            items = []
            for log in logs:
                fb = (
                    session.query(Feedback)
                    .filter_by(log_id=log.id)
                    .order_by(Feedback.timestamp.desc())
                    .first()
                )
                flagged = False
                feedback_text = ''
                if fb:
                    flagged = fb.flagged.lower() == 'true'
                    feedback_text = fb.corrected_answer or ''
                items.append({
                    "id": log.id,
                    "question": log.question,
                    "answer": log.answer,
                    "timestamp": log.timestamp.isoformat(),
                    "flagged": flagged,
                    "feedback": feedback_text,
                })
            return func.HttpResponse(
                json.dumps(items),
                mimetype="application/json",
                status_code=200,
            )
        elif method == 'POST':
            try:
                data = req.get_json()
                log_id = validate_int(data.get('id'), 'id')
                # flagged should be boolean or string
                flagged_val = data.get('flagged')
                if not isinstance(flagged_val, (bool, str)):
                    raise ValueError('flagged must be boolean or string')
                feedback_text = data.get('feedback', '')
                feedback_text = validate_str(feedback_text, 'feedback', allow_empty=True)
            except ValueError as ve:
                return func.HttpResponse(str(ve), status_code=400)
            except Exception:
                return func.HttpResponse('Invalid JSON body', status_code=400)
            fb = session.query(Feedback).filter_by(log_id=log_id).one_or_none()
            if fb:
                fb.flagged = str(flagged_val)
                fb.corrected_answer = feedback_text
            else:
                fb = Feedback(log_id=log_id, flagged=str(flagged_val), corrected_answer=feedback_text)
                session.add(fb)
            session.commit()
            return func.HttpResponse(
                json.dumps({"status": "success"}),
                mimetype="application/json",
                status_code=200,
            )
        else:
            return func.HttpResponse("Method not allowed", status_code=405)
    except Exception as e:
        session.rollback()
        return func.HttpResponse(f"Error processing request: {e}", status_code=500)
    finally:
        session.close()