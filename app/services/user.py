from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user import user_crud
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.models.user import User
from sqlalchemy import func
from sqlalchemy.sql import select
from app.core.security import verify_password, get_password_hash
from datetime import datetime
from app.core.cache import RedisCache
from app.core.logger import logger

class UserService:
    """用户服务类
    
    提供用户相关的业务逻辑处理，包括：
    - 用户查询
    - 用户创建
    - 用户更新
    - 用户验证等
    """
    
    async def create_user(
        self,
        db: AsyncSession,
        user_in: UserCreate
    ) -> User:
        """创建用户"""
        # 检查邮箱是否已存在
        db_user = await user_crud.get_by_email(db, email=user_in.email)
        if db_user:
            raise ValueError("Email already registered")
        
        # 检查用户名是否已存在
        db_user = await user_crud.get_by_username(db, username=user_in.username)
        if db_user:
            raise ValueError("Username already taken")
        
        return await user_crud.create(db=db, obj_in=user_in)

    async def get_user(
        self,
        db: AsyncSession,
        user_id: str
    ) -> Optional[User]:
        """通过用户ID获取用户信息
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            
        Returns:
            User: 用户对象，如果不存在则返回None
        """
        return await user_crud.get(db=db, user_id=user_id)

    async def get_user_by_email(
        self,
        db: AsyncSession,
        email: str
    ) -> Optional[User]:
        """通过邮箱获取用户信息
        
        Args:
            db: 数据库会话
            email: 用户邮箱
            
        Returns:
            User: 用户对象，如果不存在则返回None
        """
        return await user_crud.get_by_email(db=db, email=email)

    async def get_users(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        """获取用户列表
        
        Args:
            db: 数据库会话
            skip: 跳过的记录数
            limit: 返回的最大记录数
            
        Returns:
            List[User]: 用户列表
        """
        return await user_crud.get_multi(db=db, skip=skip, limit=limit)

    async def authenticate_user(
        self, 
        db: AsyncSession, 
        username: str,
        password: str
    ) -> Optional[User]:
        """用户认证并更新最后登录时间"""
        user = await user_crud.get_by_username(db, username)
        if not user or not verify_password(password, user.password_hash):
            return None
            
        # 更新最后登录时间
        user.last_login = datetime.now()
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        return user

    async def update_user(
        self,
        db: AsyncSession,
        user_id: str,
        user_in: UserUpdate
    ) -> Optional[User]:
        """更新用户信息"""
        db_user = await user_crud.get(db=db, user_id=user_id)
        if not db_user:
            return None
        
        # 如果要更新邮箱，检查新邮箱是否已被使用
        if user_in.email and user_in.email != db_user.email:
            existing_user = await user_crud.get_by_email(db, email=user_in.email)
            if existing_user:
                raise ValueError("Email already registered")
        
        # 如果要更新用户名，检查新用户名是否已被使用
        if user_in.username and user_in.username != db_user.username:
            existing_user = await user_crud.get_by_username(db, username=user_in.username)
            if existing_user:
                raise ValueError("Username already taken")
        
        return await user_crud.update(db=db, db_obj=db_user, obj_in=user_in)

    async def get_users_count(self, db: AsyncSession) -> int:
        """获取用户总数
        
        Args:
            db: 数据库会话
            
        Returns:
            int: 用户总数
        """
        result = await db.execute(select(func.count()).select_from(User))
        return result.scalar()

    async def update_password(
        self,
        db: AsyncSession,
        user_id: str,
        old_password: str,
        new_password: str
    ) -> Optional[User]:
        """更新用户密码
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            old_password: 旧密码
            new_password: 新密码
            
        Returns:
            User: 更新后的用户对象
            
        Raises:
            ValueError: 当旧密码验证失败时
        """
        user = await user_crud.get(db=db, user_id=user_id)
        if not user:
            return None
            
        if not verify_password(old_password, user.password_hash):
            raise ValueError("Old password is incorrect")
            
        user.password_hash = get_password_hash(new_password)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

user_service = UserService()