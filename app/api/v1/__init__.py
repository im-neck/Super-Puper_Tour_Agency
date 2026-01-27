from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.bookings import router as bookings_router
from app.api.v1.manager import router as manager_router
from app.api.v1.tours import router as tours_router

router = APIRouter(prefix="/api")
router.include_router(auth_router, tags=["auth"])
router.include_router(tours_router, tags=["tours"])
router.include_router(bookings_router, tags=["bookings"])
router.include_router(manager_router, tags=["manager"])
