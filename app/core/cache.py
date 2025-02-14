import json
from typing import Optional, Any
from app.core.redis import get_redis
from app.core.logger import logger

class RedisCache:
    @staticmethod
    async def set(key: str, value: Any, expire: int = 3600):
        """设置缓存"""
        redis = await get_redis()
        try:
            await redis.set(
                key,
                json.dumps(value) if not isinstance(value, str) else value,
                ex=expire
            )
        except Exception as e:
            logger.error(f"Redis set error: {str(e)}")
            
    @staticmethod
    async def get(key: str) -> Optional[Any]:
        """获取缓存"""
        redis = await get_redis()
        try:
            data = await redis.get(key)
            return json.loads(data) if data else None
        except Exception as e:
            logger.error(f"Redis get error: {str(e)}")
            return None
            
    @staticmethod
    async def delete(key: str):
        """删除缓存"""
        redis = await get_redis()
        try:
            await redis.delete(key)
        except Exception as e:
            logger.error(f"Redis delete error: {str(e)}")

    @staticmethod
    async def clear_user_cache(user_id: str):
        """清除用户相关的所有缓存"""
        redis = await get_redis()
        try:
            pattern = f"user:{user_id}:*"
            keys = await redis.keys(pattern)
            if keys:
                await redis.delete(*keys)
        except Exception as e:
            logger.error(f"Redis clear cache error: {str(e)}") 