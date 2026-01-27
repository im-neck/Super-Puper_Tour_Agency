from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db, require_roles
from app.models.user import UserRole
from app.models.tour import Tour
from app.services.tours import get_tour, search_tours
from app.shemas.tour import TourCreate, TourOut

router = APIRouter(prefix="/tours")


@router.get("", response_model=list[TourOut])
def list_tours(
    country: str | None = None,
    city: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    meal_type: str | None = None,
    hotel_stars: int | None = None,
    duration_days: int | None = None,
    db: Session = Depends(get_db),
) -> list[TourOut]:
    return search_tours(
        db,
        country=country,
        city=city,
        start_date=start_date,
        end_date=end_date,
        min_price=min_price,
        max_price=max_price,
        meal_type=meal_type,
        hotel_stars=hotel_stars,
        duration_days=duration_days,
    )


@router.get("/{tour_id}", response_model=TourOut)
def tour_detail(tour_id: int, db: Session = Depends(get_db)) -> TourOut:
    tour = get_tour(db, tour_id)
    if not tour:
        raise HTTPException(status_code=404, detail="Tour not found")
    return tour


@router.post(
    "",
    response_model=TourOut,
    status_code=status.HTTP_201_CREATED,
)
def create_tour(
    payload: TourCreate,
    db: Session = Depends(get_db),
    _user=Depends(require_roles(UserRole.admin)),
) -> TourOut:
    tour = Tour(**payload.model_dump())
    db.add(tour)
    db.commit()
    db.refresh(tour)
    return tour
