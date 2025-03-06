'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-03-05 15:32:09
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-03-05 16:31:41
FilePath: \RAG_Admin\app\crud\crud_search_request.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.search_request import SearchRequest
from app.schemas.search_request import SearchRequestSchema

class CRUDSearchRequest:
    async def create(self, db: AsyncSession, user_id: str, query_text: str) -> SearchRequestSchema:
        db_obj = SearchRequest(user_id=user_id, query_text=query_text)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return SearchRequestSchema.from_orm(db_obj)

    async def get(self, db: AsyncSession, request_id: int) -> Optional[SearchRequestSchema]:
        result = await db.execute(select(SearchRequest).filter(SearchRequest.id == request_id))
        return result.scalar_one_or_none()

    async def get_all(self, db: AsyncSession) -> List[SearchRequestSchema]:
        result = await db.execute(select(SearchRequest))
        return [SearchRequestSchema.from_orm(req) for req in result.scalars().all()]

    async def update(self, db: AsyncSession, request_id: int, **kwargs) -> Optional[SearchRequestSchema]:
        request = await self.get(db, request_id)
        if request:
            for key, value in kwargs.items():
                setattr(request, key, value)
            await db.commit()
            await db.refresh(request)
            return SearchRequestSchema.from_orm(request)
        return None

    async def delete(self, db: AsyncSession, request_id: int) -> None:
        request = await self.get(db, request_id)
        if request:
            await db.delete(request)
            await db.commit()

search_request_crud = CRUDSearchRequest() 