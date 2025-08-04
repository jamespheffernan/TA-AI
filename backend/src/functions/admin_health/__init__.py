import azure.functions as func
import json
from datetime import datetime
import os


def main(req: func.HttpRequest) -> func.HttpResponse:
    health = {
        'status': 'ok',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'environment': os.getenv('AZURE_FUNCTIONS_ENVIRONMENT', 'Development')
    }
    return func.HttpResponse(json.dumps(health), mimetype='application/json', status_code=200)