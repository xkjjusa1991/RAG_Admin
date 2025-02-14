"""
数据库初始化模块
"""
import asyncio
from app.core.database import Base, engine
from app.models import user, knowledge, file  # 导入所有模型

async def init_db():
    """
    初始化数据库表结构
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_db():
    """
    删除所有数据库表
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

if __name__ == "__main__":
    asyncio.run(init_db())