'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-06-26 17:32:14
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-06-27 14:25:36
FilePath: \RAG_Admin\app\api\document_parse.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.mineru_service import MinerUService
from app.crud.crud_file import crud_file
from app.core.database import get_db
import os

router = APIRouter()

@router.post('/parse', summary="文档解析", description="根据file_id解析文档，返回解析内容")
async def parse_document(
    file_id: int,
    method: str = Query("auto", description="解析方式，可选值: auto/ocr/txt"),
    lang: str = Query(None, description="OCR语言，如ch/en等"),
    db: AsyncSession = Depends(get_db)
):
    # 获取文件路径
    file_obj = await crud_file.get(db, file_id)
    if not file_obj or not hasattr(file_obj, 'file_path'):
        raise HTTPException(status_code=404, detail="文件不存在")
    file_path = file_obj.file_path
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件路径无效")
    # 调用MinerUService解析
    mineru_service = MinerUService()
    try:
        md_content = mineru_service.parse_pdf(file_path, method=method, lang=lang)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"解析失败: {str(e)}")
    return {
        "markdown": md_content
    } 