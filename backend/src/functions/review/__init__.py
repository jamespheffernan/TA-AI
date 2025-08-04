import azure.functions as func
import json
from db import SessionLocal
from models.models import QuestionLog, Feedback


def main(req: func.HttpRequest) -> func.HttpResponse:
    method = req.method
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
            except:
                return func.HttpResponse("Invalid JSON body", status_code=400)
            log_id = data.get('id')
            flagged = data.get('flagged')
            feedback_text = data.get('feedback')
            if log_id is None or flagged is None:
                return func.HttpResponse("Missing id or flagged", status_code=400)
            fb = session.query(Feedback).filter_by(log_id=log_id).one_or_none()
            if fb:
                fb.flagged = str(flagged)
                fb.corrected_answer = feedback_text
            else:
                fb = Feedback(log_id=log_id, flagged=str(flagged), corrected_answer=feedback_text)
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