import logging
import sys
import os
from pathlib import Path
from loguru import logger
from app.core.config import settings

# 获取项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# 日志文件路径
LOG_PATH = BASE_DIR / "logs"
LOG_PATH.mkdir(exist_ok=True)

print(f"Log directory created at: {LOG_PATH}")  # 添加这行来调试

# 日志格式
LOG_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

# 移除默认的 logger
logger.remove()

# 添加控制台输出
logger.add(
    sys.stdout,
    format=LOG_FORMAT,
    level="DEBUG" if settings.DEBUG else "INFO",
    colorize=True
)

# 添加文件输出
logger.add(
    LOG_PATH / "app.log",
    rotation="00:00",  # 每天零点创建新文件
    retention="30 days",  # 保留30天的日志
    format=LOG_FORMAT,
    level="INFO",
    encoding="utf-8"
)

# 异常日志
logger.add(
    LOG_PATH / "error.log",
    rotation="100 MB",  # 文件大小超过100M时创建新文件
    retention="30 days",
    format=LOG_FORMAT,
    level="ERROR",
    encoding="utf-8",
    backtrace=True,  # 显示完整的异常堆栈
    diagnose=True    # 显示变量值
) 