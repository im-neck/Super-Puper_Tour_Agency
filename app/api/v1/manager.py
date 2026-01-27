from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db, require_roles
from app.models.user import UserRole
from app.services.bookings import list_bookings_for_manager, update_booking_status
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
        return update_booking_status(
            db,
            booking_id,
            status=payload.status,
            final_price=payload.final_price,
            manager_comment=payload.manager_comment,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
