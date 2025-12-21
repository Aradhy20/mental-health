from sqlalchemy.orm import Session
from sqlalchemy import or_
from shared.models import User as DBUser
from auth_utils import get_password_hash, verify_password
from models import UserCreate
from datetime import datetime

def get_user_by_username(db: Session, username: str):
    return db.query(DBUser).filter(DBUser.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(DBUser).filter(DBUser.email == email).first()

def create_user(db: Session, user: UserCreate):
    db_user = DBUser(
        username=user.username,
        email=user.email,
        name=user.full_name,
        password_hash=get_password_hash(user.password),
        disabled=False,
        created_at=datetime.utcnow()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def get_user(db: Session, user_id: int):
    return db.query(DBUser).filter(DBUser.user_id == user_id).first()