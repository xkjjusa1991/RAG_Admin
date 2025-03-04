'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-03-04 16:25:38
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-03-04 16:35:28
FilePath: \\RAG_Admin\\app\\api\\user_logs.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_user_logs_crud
from app.schemas.user_logs import UserLogsCreate, UserLogs
from app.crud.user_logs import user_logs_crud
from app.core.database import get_db

router = APIRouter()

@router.post("/", response_model=UserLogs, summary="创建用户日志", description="创建一个新的用户日志记录。")
async def create_user_log(user_log: UserLogsCreate, db: AsyncSession = Depends(get_db)):
    """
    创建用户日志记录。

    - **session_id**: 会话ID
    - **user_id**: 用户ID
    - **query**: 用户提问内容
    - **answer**: 系统回答内容
    - **response_segment**: 响应片段
    - **score**: 分数
    - **prompt**: 提示内容
    - **like**: 点赞状态
    - **question_time**: 提问时间
    - **dislike_suggestion**: 点踩建议
    """
    print(user_log)  # 打印请求体内容
    return await user_logs_crud.create(db=db, obj_in=user_log)

@router.get("/{question_id}", response_model=UserLogs, summary="获取用户日志", description="根据问题ID获取用户日志记录。")
async def get_user_log(question_id: int, db: AsyncSession = Depends(get_db)):
    """
    获取用户日志记录。

    - **question_id**: 问题ID
    """
    user_log = await user_logs_crud.get(db=db, question_id=question_id)
    if not user_log:
        raise HTTPException(status_code=404, detail="User log not found")
    return user_log 