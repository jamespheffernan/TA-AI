import azure.functions as func
import json
from db import SessionLocal
from models.models import Course


def main(req: func.HttpRequest) -> func.HttpResponse:
    session = SessionLocal()
    try:
        if req.method == 'GET':
            courses = session.query(Course).all()
            items = [{'id': c.id, 'name': c.name} for c in courses]
            return func.HttpResponse(json.dumps(items), mimetype='application/json', status_code=200)
        elif req.method == 'POST':
            try:
                data = req.get_json()
            except:
                return func.HttpResponse('Invalid JSON body', status_code=400)
            name = data.get('name')
            if not name:
                return func.HttpResponse('Missing name', status_code=400)
            new_course = Course(name=name)
            session.add(new_course)
            session.commit()
            return func.HttpResponse(json.dumps({'id': new_course.id, 'name': new_course.name}), mimetype='application/json', status_code=201)
        else:
            return func.HttpResponse('Method not allowed', status_code=405)
    finally:
        session.close()