from redis import asyncio as aioredis
from app.core.config import settings
from app.core.logger import logger

# Redis 连接池
redis_pool = None

async def init_redis_pool():
    """初始化 Redis 连接池"""
    global redis_pool
    try:
        redis_pool = await aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )
        logger.info("Redis connection pool initialized")
    except Exception as e:
        logger.error(f"Failed to initialize Redis pool: {str(e)}")
        raise

async def get_redis():
    """获取 Redis 连接"""
    if redis_pool is None:
        await init_redis_pool()
    return redis_pool 