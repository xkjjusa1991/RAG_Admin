from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

class SearchRequestSchema(BaseModel):
    id: Optional[int]  # 添加自增主键字段
    user_id: str
    query_text: str
    search_time: datetime = datetime.now()
    result_count: int = 0
    is_satisfied: int = 0
    query_duration: float = 0.0
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    source: str = 'web'
    search_conditions: Optional[dict] = None

    class Config:
        orm_mode = True  # 允许从 ORM 模型转换
        from_attributes = True  # 允许从 ORM 模型的属性创建 Pydantic 模型

class SearchRequestCreate(BaseModel):
    user_id: Optional[str] = None
    query_text: str
    result_count: Optional[int] = 0
    is_satisfied: Optional[bool] = False
    query_duration: Optional[float] = 0.0
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    source: str = "web"
    search_conditions: Optional[dict] = None

    @validator('query_text')
    def query_text_not_empty(cls, value):
        if not value or not value.strip():
            raise ValueError('query_text cannot be empty')
        return value

    class Config:
        orm_mode = True  # 允许从 ORM 模型转换
        from_attributes = True  # 允许从 ORM 模型的属性创建 Pydantic 模型 