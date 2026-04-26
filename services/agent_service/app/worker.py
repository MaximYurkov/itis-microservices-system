import asyncio
import hashlib
from aiokafka import AIOKafkaConsumer
from redis.asyncio import Redis
from shared.events import decode_event, encode_event
from app.config import settings


def build_agent_result(prompt: str) -> str:
    punctuation = ".,!?;:()[]{}\"'"
    words = [word.strip(punctuation).lower() for word in prompt.split()]
    keywords = []
    for word in words:
        if len(word) >= 4 and word not in keywords:
            keywords.append(word)
        if len(keywords) == 5:
            break

    keywords_text = ", ".join(keywords) if keywords else "нет ключевых слов"
    return (
        f"Статус: обработано агентом\n"
        f"Краткий вывод: {prompt[:120]}\n"
        f"Ключевые слова: {keywords_text}\n"
        f"Рекомендация: можно передать результат в следующий сервис или показать пользователю."
    )


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
                prompt = payload.get("prompt", "")
                if not task_id or not prompt:
                    continue

                redis: Redis = app.state.redis
                cache_key = "prompt:" + hashlib.sha256(prompt.encode("utf-8")).hexdigest()
                status_key = f"task:{task_id}:status"

                cached_result = await redis.get(cache_key)
                if cached_result:
                    result = cached_result.decode("utf-8")
                    source = "cache"
                else:
                    await redis.set(status_key, "processing", ex=3600)
                    await asyncio.sleep(1)
                    result = build_agent_result(prompt)
                    await redis.set(cache_key, result, ex=3600)
                    source = "generated"

                await redis.set(status_key, "completed", ex=3600)

                event = {
                    "task_id": task_id,
                    "status": "completed",
                    "result": result,
                    "source": source,
                }
                await app.state.producer.send_and_wait(settings.task_completed_topic, encode_event(event))
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
