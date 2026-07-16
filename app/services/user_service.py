from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.security import get_password_hash


def get_user_by_email(db: Session, email: str):
    return (
        db.query(User)
        .filter(
            User.email == email,
            User.deleted_at.is_(None)
        )
        .first()
    )


def get_user_by_email_including_archived(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_id_including_archived(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_id(db: Session, user_id: int):
    return (
        db.query(User)
        .filter(
            User.id == user_id,
            User.deleted_at.is_(None),
            User.is_active.is_(True)
        )
        .first()
    )

def create_user(db: Session, user_data: UserCreate):
    existing_email = get_user_by_email_including_archived(db, user_data.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered"
        )

    existing_username = get_user_by_username(db, user_data.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already taken"
        )

    hashed_password = get_password_hash(user_data.password)

    new_user = User(
        email=user_data.email,
        username=user_data.username,
        password_hash=hashed_password
    )

    try:
        db.add(new_user)

        db.commit()
        db.refresh(new_user)

    except Exception:
        db.rollback()
        raise

    return new_user


def archive_user(db: Session, user: User):
    try:
        user.is_active = False
        user.deleted_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(user)

    except Exception:
        db.rollback()
        raise

    return user


def restore_user(db: Session, user: User):
    try:
        user.is_active = True
        user.deleted_at = None

        db.commit()
        db.refresh(user)

    except Exception:
        db.rollback()
        raise

    return user