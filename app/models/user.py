from datetime import datetime
from sqlalchemy import Column, String, DateTime
from app.core.database import Base

class User(Base):
    """用户数据模型
    
    属性:
        user_id: 用户ID，主键，UUID格式
        username: 用户名，唯一
        email: 邮箱，唯一
        password_hash: 密码哈希值
        full_name: 用户全名
        create_at: 创建时间
        last_login: 最后登录时间
    """
    __tablename__ = "users"

    user_id = Column(String(32), primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password_hash = Column(String(128))
    full_name = Column(String(100))
    create_at = Column(DateTime, default=datetime.now)
    last_login = Column(DateTime, nullable=True)