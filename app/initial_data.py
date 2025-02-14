import asyncio
from app.core.database import AsyncSessionLocal
from app.services.user import user_service
from app.schemas.user import UserCreate

async def init_db():
    async with AsyncSessionLocal() as db:
        # 创建超级管理员
        try:
            admin = UserCreate(
                email="admin@example.com",
                username="admin",
                password="admin",
                full_name="Admin User"
            )
            user = await user_service.create_user(db, admin)
            # 设置为超级管理员
            user.is_superuser = True
            db.add(user)
            await db.commit()
            print("Admin user created successfully")
        except Exception as e:
            print(f"Error creating admin user: {e}")

if __name__ == "__main__":
    asyncio.run(init_db()) 