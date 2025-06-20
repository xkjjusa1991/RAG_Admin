'''
Author: 自动生成
Description: 归档记录表ORM模型
'''
from sqlalchemy import Column, BigInteger, String, Date, Integer
from app.models.base import Base

class ArchiveRecord(Base):
    __tablename__ = 'v_ai_arichive_record'

    record_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='档案数据表id')
    nd = Column(String(50), comment='年度')
    dh = Column(String(50), comment='档号')
    ztm = Column(String(2000), comment='题名')
    wh = Column(String(200), comment='文号')
    zrz = Column(String(200), comment='责任者')
    bgqx = Column(String(10), comment='保管期限')
    mj = Column(String(10), comment='密级')
    gddw = Column(String(200), comment='归档单位')
    gdsj = Column(Date, comment='归档时间')
    lrsj = Column(Date, comment='录入时间')
    sry = Column(String(50), comment='立卷人')
    table_cname1 = Column(String(50), comment='档案分类名（一级）')
    table_cname2 = Column(String(50), comment='档案分类名（二级）')
    kb_id = Column(String(40), comment='知识库id') 