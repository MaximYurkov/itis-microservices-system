import asyncio
from contextlib import suppress
from fastapi import Depends, FastAPI, HTTPException, Request, status
from sqlalchemy import desc, select
from sqlalchemy.orm import Session
from aiokafka import AIOKafkaProducer
from app.config import settings
from app.consumer import consume_task_completed_events
from app.database import Base, engine, get_db
from app.models import Task
from app.schemas import TaskCreate, TaskRead
from shared.events import encode_event
from shared.kafka_utils import build_producer

app = FastAPI(title="Task Service", version="1.0.0")


@app.on_event("startup")
async def startup_event() -> None:
    Base.metadata.create_all(bind=engine)
    app.state.producer = await build_producer(settings.kafka_bootstrap_servers)
    app.state.consumer_task = asyncio.create_task(consume_task_completed_events())


@app.on_event("shutdown")
async def shutdown_event() -> None:
    consumer_task = getattr(app.state, "consumer_task", None)
    if consumer_task:
        consumer_task.cancel()
        with suppress(asyncio.CancelledError):
            await consumer_task

    producer: AIOKafkaProducer | None = getattr(app.state, "producer", None)
    if producer is not None:
        await producer.stop()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.service_name}


@app.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(payload: TaskCreate, request: Request, db: Session = Depends(get_db)) -> Task:
    task = Task(prompt=payload.prompt, status="queued")
    db.add(task)
    db.commit()
    db.refresh(task)

    event = {
        "task_id": task.id,
        "prompt": task.prompt,
        "status": task.status,
    }
    producer: AIOKafkaProducer = request.app.state.producer
    await producer.send_and_wait(settings.task_created_topic, encode_event(event))
    return task


@app.get("/tasks", response_model=list[TaskRead])
def list_tasks(db: Session = Depends(get_db)) -> list[Task]:
    tasks = db.scalars(select(Task).order_by(desc(Task.created_at)).limit(100)).all()
    return list(tasks)


@app.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(task_id: str, db: Session = Depends(get_db)) -> Task:
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
