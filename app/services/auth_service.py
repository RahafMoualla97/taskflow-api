from sqlalchemy.orm import Session

from app.models.user import User
from app.services.security import verify_password
from app.services.user_service import get_user_by_email


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user