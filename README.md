# itis-microservices-system

Микросервисная система асинхронной модерации пользовательских объявлений.

## Идея проекта

Пользователь отправляет текст объявления через API.  
Система сохраняет его в основной базе данных, отправляет событие в Kafka и запускает фоновую модерацию.  
После завершения модерации статус объявления обновляется, а отдельный сервис формирует уведомление о результате проверки.

## Сервисы

- `task-service` — приём и хранение объявлений
- `agent-service` — модерация объявлений
- `notification-service` — уведомления о результате модерации
- `gateway` — единая точка входа, маршрутизация и rate limiting

## Стек

- FastAPI
- Kafka
- PostgreSQL
- Redis
- MongoDB
- Nginx
- Docker Compose

## Как работает система

1. Клиент отправляет `POST /tasks` через gateway.
2. `task-service` сохраняет объявление в PostgreSQL со статусом `pending`.
3. `task-service` публикует событие `content.created` в Kafka.
4. `agent-service` получает событие, проверяет текст объявления и использует Redis-кэш.
5. После проверки `agent-service` публикует событие `content.moderated`.
6. `task-service` получает результат модерации и обновляет статус объявления.
7. `notification-service` получает событие `content.moderated` и сохраняет уведомление в MongoDB.

## Статусы модерации

- `pending` — объявление создано и ожидает проверки
- `approved` — объявление прошло модерацию
- `rejected` — объявление отклонено

## Быстрый старт

```bash
docker compose up --build
```

Для полной перезаписи контейнеров и данных:

```bash
docker compose down -v
docker compose up --build
```

## URL

- Gateway: `http://localhost:8080`
- Task service docs: `http://localhost:8001/docs`
- Agent service docs: `http://localhost:8002/docs`
- Notification service docs: `http://localhost:8003/docs`

## Примеры запросов

### Создать объявление

```bash
curl -X POST http://localhost:8080/tasks \
  -H "Content-Type: application/json" \
  -d "{\"content\":\"Продам велосипед в хорошем состоянии, писать в личные сообщения\"}"
```

### Получить список объявлений

```bash
curl http://localhost:8080/tasks
```

### Получить объявление по id

```bash
curl http://localhost:8080/tasks/<TASK_ID>
```

### Получить уведомления

```bash
curl http://localhost:8080/notifications
```

## Примеры сценариев

### Объявление проходит модерацию

```json
{
  "content": "Продам велосипед в хорошем состоянии, писать в личные сообщения"
}
```

Ожидаемый результат:
- статус `approved`

### Объявление отклоняется

```json
{
  "content": "Скам проект, заходите http://spam.com http://spam2.com"
}
```

Ожидаемый результат:
- статус `rejected`

## Структура проекта

```text
itis-microservices-system/
├── docker-compose.yml
├── .env.example
├── README.md
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

## Хранилища

- PostgreSQL — основная база данных объявлений
- Redis — кэш результатов модерации
- MongoDB — хранение уведомлений
- Kafka — обмен событиями между сервисами
