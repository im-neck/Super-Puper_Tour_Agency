import enum
from datetime import date

from sqlalchemy import Date, Enum, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class TourStatus(str, enum.Enum):
    available = "Available"
    unavailable = "Unavailable"


class Tour(Base):
    __tablename__ = "tours"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    country: Mapped[str] = mapped_column(String(120), index=True)
    city: Mapped[str] = mapped_column(String(120), index=True)
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    duration_days: Mapped[int] = mapped_column(Integer)
    base_price: Mapped[float] = mapped_column(Numeric(10, 2))
    currency: Mapped[str] = mapped_column(String(10), default="USD")
    description: Mapped[str] = mapped_column(Text)
    hotel_name: Mapped[str] = mapped_column(String(255))
    hotel_stars: Mapped[int] = mapped_column(Integer)
    meal_type: Mapped[str] = mapped_column(String(50))
    included: Mapped[str] = mapped_column(Text)
    status: Mapped[TourStatus] = mapped_column(
        Enum(TourStatus), default=TourStatus.available
    )

    bookings = relationship("Booking", back_populates="tour")
