from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.services.kafka_producer import send_dlq, send_number

router = APIRouter(prefix="/ingest")


class NumberIn(BaseModel):
    value: str


@router.post("/number")
def ingest_number(payload: NumberIn) -> dict:
    raw_value = payload.value.strip()
    try:
        number = int(raw_value)
    except ValueError:
        send_dlq(raw_value, "not integer")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Value must be integer. Sent to DLQ.",
        )
    send_number(number)
    return {"status": "ok", "value": number}
