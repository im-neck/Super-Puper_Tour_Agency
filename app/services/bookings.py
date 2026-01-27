from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.booking import Booking, BookingStatus
from app.models.tour import Tour, TourStatus
from app.settings import settings


def _auto_cancel_expired(db: Session) -> None:
    threshold = datetime.utcnow() - timedelta(hours=settings.booking_auto_cancel_hours)
    expired = (
        db.query(Booking)
        .filter(
            Booking.status == BookingStatus.created,
            Booking.created_at < threshold,
        )
        .all()
    )
    for booking in expired:
        booking.status = BookingStatus.cancelled
        booking.manager_comment = "Auto-cancelled due to timeout"
    if expired:
        db.commit()


def create_booking(
    db: Session, user_id: int, tour_id: int, client_comment: str | None
) -> Booking:
    tour = db.query(Tour).filter(Tour.id == tour_id).first()
    if not tour or tour.status != TourStatus.available:
        raise ValueError("Tour not available")

    booking = Booking(
        user_id=user_id,
        tour_id=tour_id,
        final_price=float(tour.base_price),
        client_comment=client_comment,
        status=BookingStatus.created,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def list_bookings_for_user(db: Session, user_id: int) -> list[Booking]:
    _auto_cancel_expired(db)
    return (
        db.query(Booking)
        .filter(Booking.user_id == user_id)
        .order_by(Booking.created_at.desc())
        .all()
    )


def cancel_booking_by_client(db: Session, booking_id: int, user_id: int) -> Booking:
    booking = (
        db.query(Booking)
        .filter(Booking.id == booking_id, Booking.user_id == user_id)
        .first()
    )
    if not booking:
        raise ValueError("Booking not found")
    if booking.status != BookingStatus.created:
        raise ValueError("Booking cannot be cancelled")
    booking.status = BookingStatus.cancelled
    booking.manager_comment = "Cancelled by client"
    db.commit()
    db.refresh(booking)
    return booking


def list_bookings_for_manager(db: Session) -> list[Booking]:
    _auto_cancel_expired(db)
    return db.query(Booking).order_by(Booking.created_at.desc()).all()


def update_booking_status(
    db: Session,
    booking_id: int,
    status: BookingStatus,
    final_price: float | None,
    manager_comment: str | None,
) -> Booking:
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise ValueError("Booking not found")
    if status == BookingStatus.cancelled and not manager_comment:
        manager_comment = "Cancelled by manager"
    booking.status = status
    if final_price is not None:
        booking.final_price = final_price
    booking.manager_comment = manager_comment
    db.commit()
    db.refresh(booking)
    return booking
