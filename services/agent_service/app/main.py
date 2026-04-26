import asyncio
from contextlib import suppress
from fastapi import FastAPI
from redis.asyncio import from_url
from aiokafka import AIOKafkaProducer
from app.config import settings
from app.worker import consume_created_tasks
from shared.kafka_utils import build_producer

app = FastAPI(title="Agent Service", version="1.0.0")


@app.on_event("startup")
async def startup_event() -> None:
    app.state.redis = from_url(settings.redis_url, decode_responses=False)
    app.state.producer = await build_producer(settings.kafka_bootstrap_servers)
    app.state.worker_task = asyncio.create_task(consume_created_tasks(app))


@app.on_event("shutdown")
async def shutdown_event() -> None:
    worker_task = getattr(app.state, "worker_task", None)
    if worker_task:
        worker_task.cancel()
        with suppress(asyncio.CancelledError):
            await worker_task

    redis = getattr(app.state, "redis", None)
    if redis is not None:
        await redis.close()

    producer: AIOKafkaProducer | None = getattr(app.state, "producer", None)
    if producer is not None:
        await producer.stop()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.service_name}
