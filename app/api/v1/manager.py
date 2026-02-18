from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db, require_roles
from app.models.user import UserRole
from app.services.bookings import list_bookings_for_manager, update_booking_status
from app.services.kafka_producer import send_event
from app.shemas.booking import BookingOut, BookingStatusUpdate

router = APIRouter(prefix="/manager")


@router.get("/bookings", response_model=list[BookingOut])
def manager_bookings(
    db: Session = Depends(get_db),
    _user=Depends(require_roles(UserRole.manager, UserRole.admin)),
) -> list[BookingOut]:
    return list_bookings_for_manager(db)


@router.put("/bookings/{booking_id}/status", response_model=BookingOut)
def change_booking_status(
    booking_id: int,
    payload: BookingStatusUpdate,
    db: Session = Depends(get_db),
    _user=Depends(require_roles(UserRole.manager, UserRole.admin)),
) -> BookingOut:
    try:
        booking = update_booking_status(
            db,
            booking_id,
            status=payload.status,
            final_price=payload.final_price,
            manager_comment=payload.manager_comment,
        )
        send_event(
            "booking_status_updated",
            {
                "booking_id": booking.id,
                "status": booking.status.value,
                "final_price": float(booking.final_price),
            },
        )
        return booking
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
