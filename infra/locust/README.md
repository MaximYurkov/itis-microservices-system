# Locust

## Установка

```bash
pip install locust
```

## Запуск

```bash
locust -f infra/locust/locustfile.py --host http://localhost:8081
```

## Адрес UI
http://localhost:8089

## Что тестируется
- GET /tasks
- POST /tasks
- POST /tasks с запрещённым содержимым

## Цель
Проверить работу ingress, сервисов, Kafka-цепочки и rate limiting под нагрузкой.