from locust import HttpUser, task, between
import random
import uuid


class ContentModerationUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def get_tasks(self):
        self.client.get("/tasks", name="GET /tasks")

    @task(1)
    def create_task(self):
        payload = {
            "content": f"Тестовое объявление {uuid.uuid4()}",
        }
        self.client.post("/tasks", json=payload, name="POST /tasks")

    @task(1)
    def create_rejected_task(self):
        payload = {
            "content": f"Скам проект {uuid.uuid4()} заходите http://spam.com",
        }
        self.client.post("/tasks", json=payload, name="POST /tasks (bad)")