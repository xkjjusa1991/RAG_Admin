'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-03-05 15:32:14
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-03-05 20:44:46
FilePath: \RAG_Admin\app\crud\crud_search_result.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.search_result import SearchResult
from app.schemas.search_result import SearchResultSchema

class CRUDSearchResult:
    async def create(
        self,
        db: AsyncSession,
        request_id: int,
        efile_id: int,
        ztm: str,
        nd: str,
        table_cname1: str,
        table_cname2: str,
        label: str,
        relevance_score: float,
        clicks: int,
        temp_id: str
    ) -> SearchResultSchema:
        db_obj = SearchResult(
            request_id=request_id,
            efile_id=efile_id,
            ztm=ztm,
            nd=nd,
            table_cname1=table_cname1,
            table_cname2=table_cname2,
            label=label,
            relevance_score=relevance_score,
            clicks=clicks,
            temp_id=temp_id
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return SearchResultSchema.from_orm(db_obj)

    async def get(self, db: AsyncSession, result_id: int) -> Optional[SearchResultSchema]:
        result = await db.execute(select(SearchResult).filter(SearchResult.id == result_id))
        return result.scalar_one_or_none()

    async def get_all_by_request_id(self, db: AsyncSession, request_id: int) -> List[SearchResultSchema]:
        result = await db.execute(select(SearchResult).filter(SearchResult.request_id == request_id))
        return [SearchResultSchema.from_orm(res) for res in result.scalars().all()]

    async def delete(self, db: AsyncSession, result_id: int) -> None:
        result = await self.get(db, result_id)
        if result:
            await db.delete(result)
            await db.commit()

    async def bulk_create(
        self,
        db: AsyncSession,
        results: List[SearchResult]
    ) -> List[SearchResultSchema]:
        db.add_all(results)
        await db.commit()
        return [SearchResultSchema.from_orm(result) for result in results]

search_result_crud = CRUDSearchResult() 