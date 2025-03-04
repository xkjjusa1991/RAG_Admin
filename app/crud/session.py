from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models.session import Session
from app.schemas.session import SessionCreate, SessionUpdate
import uuid

class CRUDSession:
    async def create(self, db: AsyncSession, *, obj_in: SessionCreate, user_id: str) -> Session:
        db_obj = Session(
            session_id=uuid.uuid4().hex,
            user_id=user_id,
            **obj_in.model_dump()
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get(self, db: AsyncSession, session_id: str) -> Optional[Session]:
        result = await db.execute(
            select(Session).filter(Session.session_id == session_id)
        )
        return result.scalar_one_or_none()

    async def get_user_sessions(
        self, 
        db: AsyncSession, 
        user_id: str
    ) -> List[Session]:
        query = select(Session).filter(Session.user_id == user_id)
        # 按最后更新时间倒序排序
        query = query.order_by(desc(Session.last_update_time))
        result = await db.execute(query)
        return result.scalars().all()

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: Session,
        obj_in: SessionUpdate
    ) -> Session:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, session_id: str) -> None:
        """删除会话"""
        session = await self.get(db=db, session_id=session_id)
        if session:
            await db.delete(session)
            await db.commit()

session_crud = CRUDSession() 