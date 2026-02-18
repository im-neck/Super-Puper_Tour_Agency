import json
from datetime import datetime
from typing import Any

from kafka import KafkaProducer

from app.settings import settings

_producer: KafkaProducer | None = None


def _get_producer() -> KafkaProducer:
    global _producer
    if _producer is None:
        _producer = KafkaProducer(
            bootstrap_servers=[s.strip() for s in settings.kafka_bootstrap_servers.split(",")],
            value_serializer=lambda v: json.dumps(v, ensure_ascii=True).encode("utf-8"),
        )
    return _producer


def send_number(value: int) -> None:
    producer = _get_producer()
    producer.send(settings.kafka_topic_numbers, {"value": value})
    producer.flush()


def send_dlq(raw_value: str, reason: str) -> None:
    producer = _get_producer()
    payload: dict[str, Any] = {
        "raw": raw_value,
        "reason": reason,
        "ts": datetime.utcnow().isoformat(),
    }
    producer.send(settings.kafka_topic_dlq, payload)
    producer.flush()


def send_event(event: str, data: dict[str, Any]) -> None:
    payload: dict[str, Any] = {
        "event": event,
        "ts": datetime.utcnow().isoformat(),
        "data": data,
    }
    try:
        producer = _get_producer()
        producer.send(settings.kafka_topic_events, payload)
        producer.flush()
    except Exception:
        return


def close_producer() -> None:
    global _producer
    if _producer is not None:
        _producer.flush()
        _producer.close()
        _producer = None
