'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-03-05 15:40:09
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-03-06 14:39:55
FilePath: \RAG_Admin\app\schemas\search_result.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from pydantic import BaseModel
from typing import Optional

class SearchResultSchema(BaseModel):
    # id: Optional[int]  # 去除 id 字段
    request_id: int
    efile_id: Optional[int] = None
    nd: Optional[str] = None
    ztm: Optional[str] = None
    table_cname1: Optional[str] = None
    table_cname2: Optional[str] = None
    label: str
    relevance_score: float = 0.0
    clicks: int = 0
    relevant_chunks: Optional[dict] = None
    temp_id: Optional[str] = None

    class Config:
        orm_mode = True  # 允许从 ORM 模型转换
        from_attributes = True  # 允许从 ORM 模型的属性创建 Pydantic 模型 