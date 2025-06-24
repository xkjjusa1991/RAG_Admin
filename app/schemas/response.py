from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar('T')

class ResponseBase(BaseModel, Generic[T]):
    code: int = 200
    msg: str = "success"
    data: Optional[T] = None

    class Config:
        json_schema_extra = {
            "example": {
                "code": 200,
                "msg": "success",
                "data": None
            }
        }


class PageInfo(BaseModel):
    total_pages: int = 1
    page: int = 1
    size: int = 10
    count: int = 0


class PageResponse(ResponseBase[T]):
    data: Optional[T] = None
    page_info: PageInfo = PageInfo()

    class Config:
        json_schema_extra = {
            "example": {
                "code": 200,
                "msg": "success",
                "data": [],
                "page_info": {
                    "total": 0,
                    "page": 1,
                    "size": 10
                }
            }
        } 