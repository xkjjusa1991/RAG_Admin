'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-02-18 11:22:27
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-02-18 11:25:25
FilePath: \RAG_Admin\app\api\sessions.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import desc
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.session import session_service
from app.schemas.session import SessionCreate, SessionUpdate, SessionResponse, SessionRename
from app.schemas.response import ResponseBase, PageResponse
from app.core.exceptions import NotFoundException
from app.core.logger import logger

router = APIRouter()

@router.post("/", response_model=ResponseBase[SessionResponse])
async def create_session(
    session_in: SessionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建新的聊天会话"""
    logger.info(f"User {current_user.username} creating new chat session")
    session = await session_service.create_session(
        db=db,
        obj_in=session_in,
        user_id=current_user.user_id
    )
    return ResponseBase(data=session)

@router.get("/", response_model=ResponseBase[List[SessionResponse]])
async def get_sessions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取用户的所有会话列表"""
    sessions = await session_service.get_user_sessions(
        db=db,
        user_id=current_user.user_id
    )
    return ResponseBase(data=sessions)

@router.get("/detail", response_model=ResponseBase[SessionResponse])
async def get_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取会话详情"""
    session = await session_service.get_session(db=db, session_id=session_id)
    if not session or session.user_id != current_user.user_id:
        raise NotFoundException("Session not found")
    return ResponseBase(data=session)

@router.put("/rename", response_model=ResponseBase[SessionResponse])
async def rename_session(
    session_id: str,
    rename_in: SessionRename,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """重命名会话"""
    session = await session_service.get_session(db=db, session_id=session_id)
    if not session or session.user_id != current_user.user_id:
        raise NotFoundException("Session not found")
        
    updated_session = await session_service.rename_session(
        db=db,
        session_id=session_id,
        new_name=rename_in.session_name
    )
    return ResponseBase(data=updated_session)

@router.delete("/delete", response_model=ResponseBase)
async def delete_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除会话"""
    session = await session_service.get_session(db=db, session_id=session_id)
    if not session or session.user_id != current_user.user_id:
        raise NotFoundException("Session not found")
        
    await session_service.delete_session(db=db, session_id=session_id)
    return ResponseBase(msg="Session deleted successfully") 