import asyncio
from datetime import datetime, timezone
from aiokafka import AIOKafkaConsumer
from app.config import settings
from shared.events import decode_event


async def consume_completed_tasks(app) -> None:
    while True:
        consumer = AIOKafkaConsumer(
            settings.task_completed_topic,
            bootstrap_servers=settings.kafka_bootstrap_servers,
            group_id="notification-service-group",
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

                doc = {
                    "task_id": task_id,
                    "status": payload.get("status", "completed"),
                    "source": payload.get("source", "generated"),
                    "message": f"Task {task_id} completed",
                    "created_at": datetime.now(timezone.utc),
                }
                await app.state.collection.insert_one(doc)
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
