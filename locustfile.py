"""
Locust performance tests for TA AI API.
Usage: pip install locust
       locust -f locustfile.py --host http://localhost:7071
"""
import os
from locust import HttpUser, between, task

API_KEY = os.getenv("API_KEY_SECRET", "test-secret")

class TAUser(HttpUser):
    wait_time = between(1, 2)

    @task(1)
    def health(self):
        self.client.get("/api/health")

    @task(5)
    def query(self):
        payload = {"course_id": 1, "question": "What is the definition of entropy?"}
        headers = {"Content-Type": "application/json", "x-api-key": API_KEY}
        self.client.post("/api/query", json=payload, headers=headers)