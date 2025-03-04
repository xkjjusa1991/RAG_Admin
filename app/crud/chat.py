from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.chat import Chat
from app.schemas.chat import ChatCreate
import uuid

class CRUDChat:
    async def create(self, db: AsyncSession, *, obj_in: ChatCreate) -> Chat:
        db_obj = Chat(
            chat_id=uuid.uuid4().hex,
            **obj_in.model_dump()
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get(self, db: AsyncSession, chat_id: str) -> Optional[Chat]:
        result = await db.execute(
            select(Chat).filter(Chat.chat_id == chat_id)
        )
        return result.scalar_one_or_none()

chat_crud = CRUDChat() 