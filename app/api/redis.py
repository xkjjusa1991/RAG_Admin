'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-03-04 14:18:08
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-06-26 14:02:03
FilePath: \RAG_Admin\app\api\redis.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
# app/api/redis.py

from fastapi import APIRouter, Depends, HTTPException
from app.core.cache import RedisCache
from app.core.logger import logger
from app.core.redis import get_redis
from typing import Any, Dict, Optional
import json

router = APIRouter()

@router.post("/url", response_model=dict)
async def save_url(url: str):
    """保存 URL 到 Redis"""
    model_url = {"url": url}
    await RedisCache.set("llm_model_url", model_url)
    return {"message": "URL saved successfully"}

@router.get("/url", response_model=dict)
async def get_url():
    """从 Redis 获取 URL"""
    url = await RedisCache.get("llm_model_url")
    if url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return url

@router.post("/session/{session_id}", response_model=str)
async def store_session_data(session_id: str, session_data: Dict[str, Any]):
    """存储会话数据到 Redis"""
    await RedisCache.set(f"session:{session_id}", session_data)
    return {"message": "Session data stored successfully"}

@router.get("/session/{session_id}", response_model=Dict[str, Any])
async def retrieve_session_data(session_id: str):
    """从 Redis 中检索会话数据"""
    session_data = await RedisCache.get(f"session:{session_id}")
    if session_data is None:
        raise HTTPException(status_code=404, detail="Session data not found")
    return session_data

@router.delete("/session/{session_id}", response_model=str)
async def delete_session_data(session_id: str):
    """删除 Redis 中指定的会话数据"""
    await RedisCache.delete(f"session:{session_id}")
    return {"message": "Session data deleted successfully"}

@router.post("/search/{request_id}", response_model=str)
async def store_search_result(request_id: str, search_result: list):
    """存储搜索结果到 Redis"""
    await RedisCache.set(f"search:{request_id}", search_result)
    return {"message": "Search result stored successfully"}

@router.get("/search/{request_id}", response_model=list)
async def get_search_result(request_id: str):
    """从 Redis 获取搜索结果"""
    search_result = await RedisCache.get(f"search:{request_id}")
    if search_result is None:
        raise HTTPException(status_code=404, detail="Search result not found")
    return search_result

@router.get("/health")
async def health_check():
    """检查 Redis 连接状态"""
    redis = await get_redis()
    try:
        await redis.ping()  # 测试连接
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Redis connection failed")

@staticmethod
async def get(key: str) -> Optional[Any]:
    """获取缓存"""
    redis = await get_redis()
    try:
        data = await redis.get(key)
        logger.info(f"Get key: {key} returned: {data}")

        if data is None or data == "":
            logger.warning(f"No data found for key: {key}")
            return None

        # 尝试解析 JSON，如果失败则返回原始字符串
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            logger.warning(f"Data for key: {key} is not valid JSON, returning as string.")
            return data  # 返回原始字符串

    except Exception as e:
        logger.error(f"Redis get error: {str(e)}")
        return None