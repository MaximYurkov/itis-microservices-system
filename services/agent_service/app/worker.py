import asyncio
import hashlib
from aiokafka import AIOKafkaConsumer
from redis.asyncio import Redis
from shared.events import decode_event, encode_event
from app.config import settings


BANNED_WORDS = [
    "скам",
    "мошенник",
    "наркотики",
    "оружие",
]


def moderate_content(content: str) -> tuple[str, str]:
    text = content.lower()

    for word in BANNED_WORDS:
        if word in text:
            return "rejected", f"Объявление отклонено: найдено запрещённое слово '{word}'."

    if len(content.strip()) < 10:
        return "rejected", "Объявление отклонено: слишком короткий текст."

    if text.count("http") > 1 or text.count("www") > 1:
        return "rejected", "Объявление отклонено: обнаружен спам или избыток ссылок."

    return "approved", "Объявление успешно прошло модерацию."


async def consume_created_tasks(app) -> None:
    while True:
        consumer = AIOKafkaConsumer(
            settings.task_created_topic,
            bootstrap_servers=settings.kafka_bootstrap_servers,
            group_id="agent-service-group",
            auto_offset_reset="earliest",
            enable_auto_commit=True,
        )
        try:
            await consumer.start()
            async for message in consumer:
                payload = decode_event(message.value)
                task_id = payload.get("task_id")
                content = payload.get("content", "")
                if not task_id or not content:
                    continue

                redis: Redis = app.state.redis
                cache_key = "content:" + hashlib.sha256(content.encode("utf-8")).hexdigest()
                status_key = f"task:{task_id}:status"

                cached_result = await redis.get(cache_key)
                if cached_result:
                    moderation_result = cached_result.decode("utf-8")
                    status = "approved" if "успешно прошло модерацию" in moderation_result.lower() else "rejected"
                    source = "cache"
                else:
                    await redis.set(status_key, "processing", ex=3600)
                    await asyncio.sleep(1)
                    status, moderation_result = moderate_content(content)
                    await redis.set(cache_key, moderation_result, ex=3600)
                    source = "generated"

                await redis.set(status_key, status, ex=3600)

                event = {
                    "task_id": task_id,
                    "status": status,
                    "moderation_result": moderation_result,
                    "source": source,
                }
                await app.state.producer.send_and_wait(
                    settings.task_completed_topic,
                    encode_event(event),
                )
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