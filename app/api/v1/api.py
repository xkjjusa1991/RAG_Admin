'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-02-10 18:03:02
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-03-04 12:24:06
FilePath: \RAG_Admin\app\api\v1\api.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from fastapi import APIRouter
from app.api.users import router as users_router
from app.api.auth import router as auth_router
from app.api.sessions import router as sessions_router
from app.api.chat import router as chat_router

api_router = APIRouter()

# 注册子路由
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(sessions_router, prefix="/sessions", tags=["sessions"])
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])
