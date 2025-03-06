'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-03-05 16:03:24
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-03-06 13:48:08
FilePath: \RAG_Admin\app\services\search_service.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.crud_search_request import search_request_crud
from app.crud.crud_search_result import search_result_crud
from app.schemas.search_request import SearchRequestSchema
from app.schemas.search_result import SearchResultSchema
from typing import List, Dict, Any, Optional
import httpx  # 用于向算法端发送请求
import asyncio  # 用于并行处理
from pydantic import Field
from app.core.config import settings  # 导入配置中的 SEARCH_URL
import logging

logger = logging.getLogger(__name__)

class SearchService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def fetch_algorithm_result(
        self,
        query: str,
        question_id: str,
        user_id: str,
        search_type: str = "hybrid",
        category_l1: Optional[str] = None,
        category_l2: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None
    ) -> Dict[str, Any]:
        """向算法端请求数据"""
        algorithm_url = "http://172.16.0.122:8803/api/search"  # 使用配置中的 SEARCH_URL
        payload = {
            "query": query,
            "question_id": str(question_id),
            "user_id": user_id,
            "search_type": search_type,
            "category_l1": category_l1,
            "category_l2": category_l2,
            "start_time": start_time,
            "end_time": end_time,
        }

        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(360.0)) as client:
                response = await client.post(algorithm_url, json=payload)
                response.raise_for_status()  # 如果响应状态码不是 200，将引发异常
                return response.json()  # 返回原始响应数据
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            raise

    async def process_algorithm_results(self, response_data: Dict[str, Any], search_request: SearchRequestSchema) -> List[Dict[str, Any]]:
        """处理算法端返回的数据并更新搜索请求"""
        # 更新搜索请求的总数
        total = int(response_data.get("total", 0))
        search_request.result_count = total  # 更新 result_count 字段
        await search_request_crud.update(self.db, search_request.id, result_count=total)  # 更新数据库中的记录

        search_results = response_data.get('results', [])
        if not search_results:
            return []

        count = 0
        for tmp_result in search_results:
            tmp_result["temp_id"] = f"{search_request.id}_{count}"
            count += 1

        return search_results

    async def process_search_request(self, search_request: SearchRequestSchema) -> List[Dict[str, Any]]:

        # 1. 向算法端发送请求
        response_data = await self.fetch_algorithm_result(
            query=search_request.query_text,
            question_id=search_request.id,  # 这里需要根据实际情况传入问题ID
            user_id=search_request.user_id
        )

        # 2. 处理算法返回的数据并更新搜索请求
        processed_results = await self.process_algorithm_results(response_data, search_request)
        print(processed_results)

        # 3. 返回处理后的结果
        return processed_results

# 实例化搜索服务
search_service = SearchService(db=None)  # db 需要在调用时传入 