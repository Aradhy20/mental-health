from pydantic import BaseModel, Field, BeforeValidator
from typing import Optional, Annotated
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None

class UserInDBBase(UserBase):
    user_id: int
    disabled: Optional[bool] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True # Pydantic v2 support for ORM
        populate_by_name = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    password_hash: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class PasswordChange(BaseModel):
    current_password: str
    new_password: str