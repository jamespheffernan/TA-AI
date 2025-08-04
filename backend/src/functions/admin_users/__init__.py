import azure.functions as func
import json
from db import SessionLocal
from models.models import User


def main(req: func.HttpRequest) -> func.HttpResponse:
    session = SessionLocal()
    try:
        if req.method == 'GET':
            users = session.query(User).all()
            items = [{'id': u.id, 'external_id': u.external_id, 'role': u.role} for u in users]
            return func.HttpResponse(json.dumps(items), mimetype='application/json', status_code=200)
        elif req.method == 'PUT':
            try:
                data = req.get_json()
            except:
                return func.HttpResponse('Invalid JSON body', status_code=400)
            user_id = data.get('id')
            role = data.get('role')
            if user_id is None or not role:
                return func.HttpResponse('Missing id or role', status_code=400)
            user = session.get(User, int(user_id))
            if not user:
                return func.HttpResponse('User not found', status_code=404)
            user.role = role
            session.commit()
            return func.HttpResponse(json.dumps({'id': user.id, 'role': user.role}), mimetype='application/json', status_code=200)
        else:
            return func.HttpResponse('Method not allowed', status_code=405)
    except Exception as e:
        return func.HttpResponse(f'Error: {e}', status_code=500)
    finally:
        session.close()