import asyncio
import logging
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.database import Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_db() -> None:
    """初始化数据库"""
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    
    async with engine.begin() as conn:
        # 创建所有表
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    # 创建超级管理员
    from app.crud.crud_user import crud_user
    from app.core.database import AsyncSessionLocal
    
    async with AsyncSessionLocal() as db:
        # 检查是否已存在超级管理员
        admin = await crud_user.get_by_email(db, "admin@example.com")
        if not admin:
            admin_data = {
                "email": "admin@example.com",
                "username": "admin",
                "password": "admin123",
                "full_name": "System Administrator"
            }
            await crud_user.create(db, admin_data)
            logger.info("Created admin user")

async def main() -> None:
    logger.info("Creating initial data")
    await init_db()
    logger.info("Initial data created")

if __name__ == "__main__":
    asyncio.run(main()) 