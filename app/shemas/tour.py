from datetime import date

from pydantic import BaseModel, ConfigDict

from app.models.tour import TourStatus


class TourCreate(BaseModel):
    name: str
    country: str
    city: str
    start_date: date
    end_date: date
    duration_days: int
    base_price: float
    currency: str
    description: str
    hotel_name: str
    hotel_stars: int
    meal_type: str
    included: str
    status: TourStatus = TourStatus.available


class TourOut(BaseModel):
    id: int
    name: str
    country: str
    city: str
    start_date: date
    end_date: date
    duration_days: int
    base_price: float
    currency: str
    description: str
    hotel_name: str
    hotel_stars: int
    meal_type: str
    included: str
    status: TourStatus

    model_config = ConfigDict(from_attributes=True)
