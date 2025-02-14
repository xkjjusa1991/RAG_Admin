'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-02-04 01:27:37
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-02-10 09:02:33
FilePath: \RAG_Admin\app\crud\crud_user.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from typing import Optional, List, Union, Dict, Any
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class CRUDUser:
    """用户CRUD操作类
    
    提供用户的基础数据库操作：
    - 创建用户
    - 读取用户信息
    - 更新用户信息
    - 删除用户
    """
    
    async def get(self, db: AsyncSession, user_id: int) -> Optional[User]:
        """异步获取用户信息"""
        result = await db.execute(
            select(User).filter(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """异步通过邮箱获取用户"""
        result = await db.execute(
            select(User).filter(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_by_username(self, db: AsyncSession, username: str) -> Optional[User]:
        """异步通过用户名获取用户"""
        result = await db.execute(
            select(User).filter(User.username == username)
        )
        return result.scalar_one_or_none()
    
    async def get_multi(
        self, 
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[User]:
        """异步获取用户列表"""
        result = await db.execute(
            select(User)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def create(self, db: AsyncSession, obj_in: UserCreate) -> User:
        """异步创建用户"""
        db_obj = User(
            username=obj_in.username,
            email=obj_in.email,
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
        obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        """异步更新用户信息"""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
            
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])
                
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def update_password(
        self, 
        db: AsyncSession, 
        db_obj: User, 
        new_password: str
    ) -> User:
        """异步更新用户密码"""
        db_obj.password_hash = get_password_hash(new_password)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def update_last_login(
        self, 
        db: AsyncSession, 
        db_obj: User
    ) -> User:
        """异步更新最后登录时间"""
        db_obj.last_login = datetime.now()
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

crud_user = CRUDUser() 