'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-02-18 11:22:16
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-02-18 12:02:27
FilePath: \RAG_Admin\app\services\session.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.session import session_crud
from app.schemas.session import SessionCreate, SessionUpdate
from app.models.session import Session
from app.core.logger import logger

class SessionService:
    async def create_session(
        self,
        db: AsyncSession,
        *,
        obj_in: SessionCreate,
        user_id: str
    ) -> Session:
        """创建新会话"""
        logger.info(f"Creating new session for user {user_id}")
        return await session_crud.create(db=db, obj_in=obj_in, user_id=user_id)

    async def get_session(
        self,
        db: AsyncSession,
        session_id: str
    ) -> Optional[Session]:
        """获取会话详情"""
        return await session_crud.get(db=db, session_id=session_id)

    async def get_user_sessions(
        self,
        db: AsyncSession,
        user_id: str
    ) -> List[Session]:
        """获取用户的所有会话列表，按最后更新时间倒序排序"""
        return await session_crud.get_user_sessions(
            db=db,
            user_id=user_id
        )

    async def update_session(
        self,
        db: AsyncSession,
        *,
        session_id: str,
        obj_in: SessionUpdate
    ) -> Optional[Session]:
        """更新会话信息"""
        session = await session_crud.get(db=db, session_id=session_id)
        if not session:
            return None
        return await session_crud.update(db=db, db_obj=session, obj_in=obj_in)

    async def end_session(
        self,
        db: AsyncSession,
        session_id: str
    ) -> Optional[Session]:
        """结束会话"""
        session = await session_crud.get(db=db, session_id=session_id)
        if not session:
            return None
            
        update_data = SessionUpdate(
            end_time=datetime.now(),
            session_status=2  # 非活跃
        )
        return await session_crud.update(db=db, db_obj=session, obj_in=update_data)

    async def delete_session(
        self,
        db: AsyncSession,
        session_id: str
    ) -> None:
        """删除会话"""
        await session_crud.delete(db=db, session_id=session_id)

    async def rename_session(
        self,
        db: AsyncSession,
        session_id: str,
        new_name: str
    ) -> Optional[Session]:
        """重命名会话"""
        session = await session_crud.get(db=db, session_id=session_id)
        if not session:
            return None
        
        session.session_name = new_name  # 只更新会话名称
        db.add(session)
        await db.commit()
        await db.refresh(session)
        return session

    async def init_chat_session(
        self,
        db: AsyncSession,
        user_id: str,
        session_name: str,
        context: Optional[str] = None,
        session_type: int = 0
    ) -> Session:
        """
        初始化聊天会话
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            session_name: 会话名称
            context: 会话上下文
            session_type: 会话类型(档案：1、个人：2、其他：0)
            
        Returns:
            Session: 创建的会话对象
        """
        logger.info(f"Initializing chat session for user {user_id}")
        
        session_data = SessionCreate(
            session_name=session_name,
            context=context,
            session_type=session_type
        )
        
        return await self.create_session(
            db=db,
            obj_in=session_data,
            user_id=user_id
        )

session_service = SessionService() 