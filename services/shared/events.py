import json
from typing import Any

TASK_CREATED_TOPIC_DEFAULT = "task.created"
TASK_COMPLETED_TOPIC_DEFAULT = "task.completed"


def encode_event(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, ensure_ascii=False).encode("utf-8")


def decode_event(payload: bytes | bytearray | memoryview | None) -> dict[str, Any]:
    if payload is None:
        return {}
    if isinstance(payload, memoryview):
        payload = payload.tobytes()
    if isinstance(payload, bytearray):
        payload = bytes(payload)
    if isinstance(payload, bytes):
        return json.loads(payload.decode("utf-8"))
    raise TypeError(f"Unsupported payload type: {type(payload)!r}")
