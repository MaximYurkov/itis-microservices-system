import asyncio
from aiokafka import AIOKafkaConsumer
from sqlalchemy import select
from app.config import settings
from app.database import SessionLocal
from app.models import Task
from shared.events import decode_event


async def consume_task_completed_events() -> None:
    while True:
        consumer = AIOKafkaConsumer(
            settings.task_completed_topic,
            bootstrap_servers=settings.kafka_bootstrap_servers,
            group_id="task-service-group",
            auto_offset_reset="earliest",
            enable_auto_commit=True,
        )
        try:
            await consumer.start()
            async for message in consumer:
                payload = decode_event(message.value)
                task_id = payload.get("task_id")
                if not task_id:
                    continue

                with SessionLocal() as db:
                    task = db.scalar(select(Task).where(Task.id == task_id))
                    if task is None:
                        continue
                    task.status = payload.get("status", "completed")
                    task.result = payload.get("result")
                    db.add(task)
                    db.commit()
        except asyncio.CancelledError:
            try:
                await consumer.stop()
            finally:
                raise
        except Exception:
            try:
                await consumer.stop()
            except Exception:
                pass
            await asyncio.sleep(3)
        finally:
            try:
                await consumer.stop()
            except Exception:
                pass
