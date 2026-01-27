from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.services.bookings import (
    cancel_booking_by_client,
    create_booking,
    list_bookings_for_user,
)
from app.shemas.booking import BookingCreate, BookingOut, BookingUserOut

router = APIRouter(prefix="/bookings")


@router.post("", response_model=BookingOut, status_code=status.HTTP_201_CREATED)
def create_booking_endpoint(
    payload: BookingCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> BookingOut:
    try:
        return create_booking(db, user.id, payload.tour_id, payload.client_comment)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/my", response_model=list[BookingUserOut])
def my_bookings(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[BookingUserOut]:
    return list_bookings_for_user(db, user.id)


@router.put("/{booking_id}/cancel", response_model=BookingOut)
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> BookingOut:
    try:
        return cancel_booking_by_client(db, booking_id, user.id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
