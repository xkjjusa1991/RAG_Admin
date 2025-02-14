'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-02-10 10:42:48
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-02-14 15:40:30
FilePath: \RAG_Admin\app\api\auth.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import create_access_token
from app.services.user import user_service
from app.core.config import settings
from app.schemas.response import ResponseBase
from app.schemas.auth import LoginSchema
from app.schemas.user import UserResponse
from app.core.exceptions import AuthFailedException
from loguru import logger

router = APIRouter()

@router.post("/login", response_model=ResponseBase)
async def login(
    login_data: LoginSchema,
    db: AsyncSession = Depends(get_db)
):
    """用户登录"""
    logger.info(f"Login attempt for user: {login_data.username}")
    
    user = await user_service.authenticate_user(
        db, login_data.username, login_data.password
    )
    if not user:
        logger.warning(f"Failed login attempt for user: {login_data.username}")
        raise AuthFailedException("Incorrect username or password")
    
    logger.info(f"User logged in successfully: {login_data.username}")
    
    # 创建访问令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    # 将 User 模型转换为 UserResponse schema
    user_response = UserResponse.model_validate(user)
    
    return ResponseBase(data={
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_response,
        "last_login": user.last_login
    })
