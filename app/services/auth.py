from sqlalchemy.orm import Session

from app.models.user import User, UserRole
from app.security import hash_password, verify_password
from app.services.user import get_user_by_email


def create_user(
    db: Session,
    email: str,
    password: str,
    full_name: str,
    phone: str,
    role: UserRole = UserRole.client,
) -> User:
    user = User(
        email=email,
        hashed_password=hash_password(password),
        role=role,
        full_name=full_name,
        phone=phone,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
