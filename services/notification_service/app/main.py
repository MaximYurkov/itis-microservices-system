import asyncio
from contextlib import suppress
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from app.worker import consume_completed_tasks

app = FastAPI(title="Notification Service", version="1.0.0")


@app.on_event("startup")
async def startup_event() -> None:
    app.state.mongo = AsyncIOMotorClient(settings.mongo_url)
    db = app.state.mongo[settings.mongo_db]
    app.state.collection = db[settings.mongo_collection]
    app.state.worker_task = asyncio.create_task(consume_completed_tasks(app))


@app.on_event("shutdown")
async def shutdown_event() -> None:
    worker_task = getattr(app.state, "worker_task", None)
    if worker_task:
        worker_task.cancel()
        with suppress(asyncio.CancelledError):
            await worker_task

    mongo = getattr(app.state, "mongo", None)
    if mongo is not None:
        mongo.close()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.service_name}


@app.get("/notifications")
async def list_notifications() -> list[dict]:
    items = []
    cursor = app.state.collection.find().sort("created_at", -1).limit(100)
    async for item in cursor:
        item["id"] = str(item.pop("_id"))
        items.append(item)
    return items


@app.get("/notifications/{task_id}")
async def get_notification(task_id: str) -> dict:
    item = await app.state.collection.find_one({"task_id": task_id})
    if item is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    item["id"] = str(item.pop("_id"))
    return item
