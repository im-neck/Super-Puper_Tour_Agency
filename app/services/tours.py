from datetime import date

from sqlalchemy.orm import Session

from app.models.tour import Tour, TourStatus


def search_tours(
    db: Session,
    country: str | None = None,
    city: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    meal_type: str | None = None,
    hotel_stars: int | None = None,
    duration_days: int | None = None,
) -> list[Tour]:
    query = db.query(Tour).filter(Tour.status == TourStatus.available)
    if country:
        query = query.filter(Tour.country.ilike(f"%{country}%"))
    if city:
        query = query.filter(Tour.city.ilike(f"%{city}%"))
    if start_date:
        query = query.filter(Tour.start_date >= start_date)
    if end_date:
        query = query.filter(Tour.end_date <= end_date)
    if min_price is not None:
        query = query.filter(Tour.base_price >= min_price)
    if max_price is not None:
        query = query.filter(Tour.base_price <= max_price)
    if meal_type:
        query = query.filter(Tour.meal_type.ilike(f"%{meal_type}%"))
    if hotel_stars:
        query = query.filter(Tour.hotel_stars == hotel_stars)
    if duration_days:
        query = query.filter(Tour.duration_days == duration_days)
    return query.all()


def get_tour(db: Session, tour_id: int) -> Tour | None:
    return db.query(Tour).filter(Tour.id == tour_id).first()
