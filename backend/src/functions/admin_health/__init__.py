import azure.functions as func
import json
from datetime import datetime
import os


def main(req: func.HttpRequest) -> func.HttpResponse:
    # Enforce API key authentication
    secret = os.getenv("API_KEY_SECRET")
    provided = req.headers.get("x-api-key")
    if provided != secret:
        return func.HttpResponse("Unauthorized", status_code=401)
    health = {
        'status': 'ok',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'environment': os.getenv('AZURE_FUNCTIONS_ENVIRONMENT', 'Development')
    }
    return func.HttpResponse(json.dumps(health), mimetype='application/json', status_code=200)