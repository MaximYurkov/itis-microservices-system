import asyncio
from aiokafka import AIOKafkaProducer


async def build_producer(bootstrap_servers: str, retries: int = 30, delay: int = 2) -> AIOKafkaProducer:
    last_error = None
    for _ in range(retries):
        producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)
        try:
            await producer.start()
            return producer
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            try:
                await producer.stop()
            except Exception:  # noqa: BLE001
                pass
            await asyncio.sleep(delay)
    raise RuntimeError(f"Kafka producer startup failed: {last_error}")
