from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# 创建异步数据库引擎
engine = create_async_engine(settings.DATABASE_URL)

# 创建异步会话工厂
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# 创建基本模型类
Base = declarative_base()

async def get_db():
    """
    获取异步数据库会话的依赖函数
    
    Yields:
        AsyncSession: 异步数据库会话对象
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close() 