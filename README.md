# itis-microservices-system

Микросервисная система асинхронной модерации пользовательских объявлений.

Сервисы:
- task-service — приём и хранение объявлений
- agent-service — модерация объявлений
- notification-service — уведомления о результате модерации

Стек:
- FastAPI
- Kafka
- PostgreSQL
- Redis
- MongoDB
- Nginx
- Docker Compose

## Быстрый старт

```bash
docker compose up --build
```

## Что делает проект

1. Клиент отправляет `POST /tasks` через gateway.
2. `task-service` сохраняет задачу в Postgres и публикует событие `task.created`.
3. `agent-service` получает событие, "обрабатывает" prompt, использует Redis-кэш и публикует `task.completed`.
4. `task-service` получает `task.completed` и обновляет статус задачи.
5. `notification-service` получает `task.completed` и пишет уведомление в MongoDB.

## URL

- Gateway: `http://localhost:8080`
- Task service docs: `http://localhost:8001/docs`
- Agent service docs: `http://localhost:8002/docs`
- Notification service docs: `http://localhost:8003/docs`

## Примеры запросов

Создать задачу:

```bash
curl -X POST http://localhost:8080/tasks   -H "Content-Type: application/json"   -d '{"prompt":"Сделай краткий анализ идеи AI помощника для студентов"}'
```

Получить список задач:

```bash
curl http://localhost:8080/tasks
```

Получить задачу по id:

```bash
curl http://localhost:8080/tasks/<TASK_ID>
```

Получить уведомления:

```bash
curl http://localhost:8080/notifications
```

## Структура

```text
ai-agent-microservices/
├── docker-compose.yml
├── .env.example
├── gateway/
│   └── nginx.conf
└── services/
    ├── shared/
    │   ├── __init__.py
    │   ├── events.py
    │   └── kafka_utils.py
    ├── task_service/
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   └── app/
    ├── agent_service/
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   └── app/
    └── notification_service/
        ├── Dockerfile
        ├── requirements.txt
        └── app/
```
