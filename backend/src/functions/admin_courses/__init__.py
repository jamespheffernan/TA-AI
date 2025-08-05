import azure.functions as func
import json
from db import SessionLocal
from models.models import Course
import os


def main(req: func.HttpRequest) -> func.HttpResponse:
    # Enforce API key authentication
    secret = os.getenv("API_KEY_SECRET")
    provided = req.headers.get("x-api-key")
    if provided != secret:
        return func.HttpResponse("Unauthorized", status_code=401)
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
        elif req.method == 'PUT':
            try:
                data = req.get_json()
            except:
                return func.HttpResponse('Invalid JSON body', status_code=400)
            course_id = data.get('id')
            name = data.get('name')
            if course_id is None or not name:
                return func.HttpResponse('Missing id or name', status_code=400)
            course = session.get(Course, int(course_id))
            if not course:
                return func.HttpResponse('Course not found', status_code=404)
            course.name = name
            session.commit()
            return func.HttpResponse(json.dumps({'id': course.id, 'name': course.name}), mimetype='application/json', status_code=200)
        elif req.method == 'DELETE':
            course_id = req.params.get('id')
            if not course_id:
                return func.HttpResponse('Missing id', status_code=400)
            course = session.get(Course, int(course_id))
            if not course:
                return func.HttpResponse('Course not found', status_code=404)
            session.delete(course)
            session.commit()
            return func.HttpResponse(json.dumps({'status': 'deleted'}), mimetype='application/json', status_code=200)
        else:
            return func.HttpResponse('Method not allowed', status_code=405)
    finally:
        session.close()