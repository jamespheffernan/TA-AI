import azure.functions as func
import json
from sqlalchemy import func
from db import SessionLocal
from models.models import QuestionLog, Feedback


def main(req: func.HttpRequest) -> func.HttpResponse:
    session = SessionLocal()
    try:
        total_questions = session.query(func.count(QuestionLog.id)).scalar() or 0
        flagged_count = session.query(func.count(Feedback.id)).filter(Feedback.flagged == 'true').scalar() or 0
        # Most asked questions
        results = (
            session.query(QuestionLog.question, func.count(QuestionLog.id).label('count'))
            .group_by(QuestionLog.question)
            .order_by(func.count(QuestionLog.id).desc())
            .limit(5)
            .all()
        )
        most_asked = [{"question": q, "count": c} for q, c in results]
        overview = {
            "totalQuestions": total_questions,
            "flaggedCount": flagged_count,
            "mostAsked": most_asked,
        }
        return func.HttpResponse(
            json.dumps({"overview": overview}),
            mimetype="application/json",
            status_code=200,
        )
    except Exception as e:
        return func.HttpResponse(f"Error generating analytics: {e}", status_code=500)
    finally:
        session.close()