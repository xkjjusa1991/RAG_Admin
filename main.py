'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-02-04 01:27:27
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-06-18 14:23:09
FilePath: \RAG_Admin\main.py
Description: 应用入口文件
'''
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router
from app.core.exceptions import APIException
from app.schemas.response import ResponseBase
from app.core.logger import logger
from app.core.redis import init_redis_pool, redis_pool
from app.core.database import engine
from contextlib import asynccontextmanager
import time

LOG_PATH = "logs/app.log"  # 或你实际的日志路径

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行
    await init_redis_pool()
    logger.info("Redis pool initialized")
    
    yield
    
    # 关闭时执行
    if engine:
        await engine.dispose()
        logger.info("Database connection closed")
    
    if redis_pool:
        await redis_pool.close()
        logger.info("Redis connection closed")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 请求日志中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # 记录请求信息
    logger.info(f"Request: {request.method} {request.url}")
    
    response = await call_next(request)
    
    # 记录响应时间
    process_time = (time.time() - start_time) * 1000
    logger.info(f"Response: {response.status_code} - Took {process_time:.2f}ms")
    
    return response

# 全局异常处理
@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    logger.warning(f"API Exception: {exc.msg}")
    return JSONResponse(
        status_code=exc.status_code,
        content=ResponseBase(
            code=exc.code,
            msg=exc.msg
        ).model_dump()
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unexpected error occurred")  # 记录未捕获的异常
    return JSONResponse(
        status_code=500,
        content=ResponseBase(
            code=500,
            msg=str(exc)
        ).model_dump()
    )

# 包含API路由
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Application starting... Logs will be written to {LOG_PATH}")
    uvicorn.run(app, host="0.0.0.0", port=8001)