'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-03-04 12:24:10
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-03-04 13:51:34
FilePath: \RAG_Admin\app\api\chat.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.chat import ChatRequest, ChatResponse, ChatCreate
from app.services.chat import chat_service
from app.core.logger import logger
import json
from app.crud.chat import chat_crud

router = APIRouter()

@router.post("/")
async def create_chat(
    chat_request: ChatRequest,
    # current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建聊天记录并与算法端交互"""
    # logger.info(f"User {current_user.username} sending question: {chat_request.query}")

    model_input = {
        "query": chat_request.query,
        "session_id": chat_request.session_id,
    }
    print(chat_request)

    # 根据 stream 字段判断是否流式返回
    if chat_request.stream:
        async def streamer():
            async for item in chat_service.fetch_streaming_data_from_model(chat_request.dict()):
                yield f"data:{json.dumps(item, ensure_ascii=False)}\n\n"  # 注意这里用\0作为分隔符
        headers = {
            "Content-Type": "text/event-stream; charset=utf-8",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
        return StreamingResponse(streamer(), headers=headers)
    else:
        # 如果不需要流式返回，直接获取完整的响应
        response_data = await chat_service.get_chat_response(model_input)
        answer = response_data.get("response", "未返回答案")

        # 创建聊天记录
        chat = await chat_crud.create(db=db, obj_in=ChatCreate(
            question=chat_request.query,
            answer=answer,
            session_id=chat_request.session_id
        ))

        return ChatResponse(
            chat_id=chat.chat_id,
            user_id=chat.user_id,
            question=chat.question,
            answer=answer,
            created_at=chat.created_at
        )
