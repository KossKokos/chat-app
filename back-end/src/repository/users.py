# import pytz
from sqlalchemy.orm import Session

from datetime import datetime
from decimal import Decimal

from ..database.models import User, BanList
from ..schemas.users import (
    UserModel,
    UserResponse,
)

async def create_user(body: UserModel, db: Session) -> User:
    user: User = User(**body.dict())
    db.add(user)
    db.commit()
    # if user.id == 1:
    #     user.role = "admin"
    #     db.commit()
    db.refresh(user)
    return user


async def get_user_by_email(email: str, db: Session) -> User | None:
    return db.query(User).filter(User.email == email).first()


async def get_user_by_username(username: str, db: Session) -> User | None:
    return db.query(User).filter(User.username == username).first()


async def is_banned(user_id: int, db: Session) -> bool:
    banned = db.query(BanList).filter(BanList.user_id == user_id).first()
    if banned:
        return True
    return False


async def update_token(user: User, refresh_token: str, db: Session) -> None:
    user.refresh_token = refresh_token
    db.commit()
    db.refresh(user)