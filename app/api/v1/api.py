'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-02-10 18:03:02
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-03-04 16:31:07
FilePath: \RAG_Admin\app\api\v1\api.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from fastapi import APIRouter
from app.api.users import router as users_router
from app.api.auth import router as auth_router
from app.api.sessions import router as sessions_router
from app.api.chat import router as chat_router
from app.api.redis import router as redis_router
from app.api.user_logs import router as user_logs_router
from app.api.search import router as search_router

api_router = APIRouter()

# 注册子路由
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(sessions_router, prefix="/sessions", tags=["sessions"])
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])
api_router.include_router(redis_router, prefix="/redis", tags=["redis"])
api_router.include_router(user_logs_router, prefix="/user_logs", tags=["user_logs"])
api_router.include_router(search_router, prefix="/search", tags=["search"])