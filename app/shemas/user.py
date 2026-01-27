from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.user import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    full_name: str
    phone: str
    registered_at: datetime

    model_config = ConfigDict(from_attributes=True)
