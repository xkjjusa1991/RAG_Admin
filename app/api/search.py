'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-03-05 15:32:24
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-03-06 14:55:56
FilePath: \RAG_Admin\app\api\search.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.crud.crud_search_request import search_request_crud
from app.crud.crud_search_result import search_result_crud
from app.schemas.search_request import SearchRequestCreate, SearchRequestSchema
from app.schemas.search_result import SearchResultSchema
from app.services.search_service import SearchService, search_service
from app.models.search_result import SearchResult
from typing import List, Optional

router = APIRouter()

@router.post("/requests/", response_model=SearchRequestSchema)
async def create_search_request(search_request: SearchRequestSchema, db: AsyncSession = Depends(get_db)):
    search_service = SearchService(db)
    return await search_service.process_search_request(search_request)

@router.get("/requests/{request_id}", response_model=SearchRequestSchema)
async def get_search_request(request_id: int, db: AsyncSession = Depends(get_db)):
    request = await search_request_crud.get(db=db, request_id=request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Search request not found")
    return request

@router.get("/requests/", response_model=List[SearchRequestSchema])
async def get_all_search_requests(db: AsyncSession = Depends(get_db)):
    return await search_request_crud.get_all(db=db)

@router.post("/results/", response_model=SearchResultSchema)
async def create_search_result(request_id: int, efile_id: Optional[int], label: str, db: AsyncSession = Depends(get_db)):
    return await search_result_crud.create(db=db, request_id=request_id, efile_id=efile_id, label=label)

@router.get("/results/{result_id}", response_model=SearchResultSchema)
async def get_search_result(result_id: int, db: AsyncSession = Depends(get_db)):
    result = await search_result_crud.get(db=db, result_id=result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Search result not found")
    return result

@router.get("/results/request/{request_id}", response_model=List[SearchResultSchema])
async def get_results_by_request_id(request_id: int, db: AsyncSession = Depends(get_db)):
    return await search_result_crud.get_all_by_request_id(db=db, request_id=request_id)

@router.post("/search/", response_model=List[SearchResultSchema])
async def search(search_request: SearchRequestCreate, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    search_service = SearchService(db)
    
    # 1. 保存搜索请求到数据库
    saved_request = await search_request_crud.create(
        db=db,
        user_id=search_request.user_id,
        query_text=search_request.query_text
    )
    
    # 2. 处理搜索请求
    processed_results = await search_service.process_search_request(saved_request)

    # 3. 将 processed_results 转换为 SearchResultSchema 对象列表
    search_results = [
        SearchResultSchema(
            request_id=saved_request.id,
            efile_id=int(result.get("efile_id")),
            ztm=result.get("metadata", {}).get("ztm", ""),
            nd=result.get("metadata", {}).get("nd", ""),
            table_cname1=result.get("metadata", {}).get("table_cname1", ""),
            table_cname2=result.get("metadata", {}).get("table_cname2", ""),
            label=result.get("metadata", {}).get("label", ""),
            relevance_score=float(result.get("score", 0.0)),
            clicks=0,
            temp_id=result["temp_id"],
        )
        for result in processed_results
    ]

    # 4. 将批量插入操作放入后台任务
    background_tasks.add_task(bulk_insert_search_results, db, search_results)

    return search_results  # 直接返回 SearchResultSchema 列表

async def bulk_insert_search_results(db: AsyncSession, results: List[SearchResultSchema]):
    # 将 SearchResultSchema 转换为 SearchResult
    search_results = [
        SearchResult(
            request_id=result.request_id,
            efile_id=result.efile_id,
            ztm=result.ztm,
            nd=result.nd,
            table_cname1=result.table_cname1,
            table_cname2=result.table_cname2,
            label=result.label,
            relevance_score=result.relevance_score,
            clicks=result.clicks,
            temp_id=result.temp_id,
        )
        for result in results
    ]
    
    await search_result_crud.bulk_create(db=db, results=search_results) 