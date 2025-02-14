from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash
import uuid

class CRUDUser:
    async def get(self, db: AsyncSession, user_id: str) -> Optional[User]:
        result = await db.execute(
            select(User).filter(User.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        result = await db.execute(
            select(User).filter(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, db: AsyncSession, username: str) -> Optional[User]:
        result = await db.execute(
            select(User).filter(User.username == username)
        )
        return result.scalar_one_or_none()

    async def get_multi(
        self, 
        db: AsyncSession, 
        *, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[User]:
        result = await db.execute(
            select(User)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        db_obj = User(
            user_id=uuid.uuid4().hex,
            email=obj_in.email,
            username=obj_in.username,
            password_hash=get_password_hash(obj_in.password),
            full_name=obj_in.full_name
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, 
        db: AsyncSession, 
        db_obj: User, 
        obj_in: UserUpdate
    ) -> User:
        if obj_in.email is not None:
            db_obj.email = obj_in.email
        if obj_in.username is not None:
            db_obj.username = obj_in.username
        if obj_in.full_name is not None:
            db_obj.full_name = obj_in.full_name
        if obj_in.password is not None:
            db_obj.password_hash = get_password_hash(obj_in.password)
        
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


user_crud = CRUDUser()