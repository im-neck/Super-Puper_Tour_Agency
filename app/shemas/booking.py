from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.booking import BookingStatus
from app.shemas.tour import TourOut


class BookingCreate(BaseModel):
    tour_id: int
    client_comment: str | None = None


class BookingStatusUpdate(BaseModel):
    status: BookingStatus
    final_price: float | None = None
    manager_comment: str | None = None


class BookingOut(BaseModel):
    id: int
    user_id: int
    tour_id: int
    created_at: datetime
    final_price: float
    client_comment: str | None
    status: BookingStatus
    manager_comment: str | None

    model_config = ConfigDict(from_attributes=True)


class BookingUserOut(BaseModel):
    id: int
    created_at: datetime
    final_price: float
    client_comment: str | None
    status: BookingStatus
    manager_comment: str | None
    tour: TourOut

    model_config = ConfigDict(from_attributes=True)
