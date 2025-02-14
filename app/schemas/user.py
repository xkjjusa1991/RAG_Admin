from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from .base import BaseSchema


class UserBase(BaseSchema):
    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseSchema):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None


class UserInDB(UserBase):
    user_id: str
    create_at: datetime
    last_login: Optional[datetime]


class UserResponse(UserBase):
    user_id: str
    create_at: datetime
    last_login: Optional[datetime]


class PasswordUpdate(BaseSchema):
    old_password: str
    new_password: str