'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-02-04 01:27:29
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-03-04 14:05:44
FilePath: \RAG_Admin\app\core\config.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-02-04 01:27:29
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-03-04 12:39:19
FilePath: \RAG_Admin\app\core\config.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from dotenv import load_dotenv

load_dotenv()  # 加载环境变量

class Settings(BaseSettings):
    # 基本配置
    PROJECT_NAME: str = "RAG Admin"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "RAG Admin API"
    API_V1_STR: str = "/api/v1"
    
    # 数据库配置
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    
    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # 文件路径配置
    FILE_ROOT_PATH: str = r"C:\Users\xkjju\Desktop\tmp"
    
    # API URLs
    VITE_API_BASE_URL: str = "http://localhost:8001"
    MODEL_URL: str = "http://172.16.0.122:8803/api/rag/rag_server"
    PROCESS_URL: str = "http://js1.blockelite.cn:23279/api/file/process"
    SEARCH_URL: str = "http://js1.blockelite.cn:23279/api/search"
    
    # 安全配置
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS配置
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173"]
    
    # 调试模式
    DEBUG: bool = False
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    
    # 聊天接口配置
    CHAT_URL: str = MODEL_URL
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        env_file_encoding='utf-8',
        extra='allow'
    )

settings = Settings()
