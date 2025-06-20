'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-06-20 13:35:44
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-06-20 13:36:04
FilePath: \RAG_Admin\app\models\archive_file.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
'''
Author: 自动生成
Description: 归档文件表ORM模型
'''
from sqlalchemy import Column, BigInteger, String, Integer, Text, DateTime
from app.models.base import Base

class ArchiveFile(Base):
    __tablename__ = 'v_ai_arichive_efile'

    efile_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='文件表id')
    record_id = Column(BigInteger, comment='档案数据表编号')
    label = Column(String(500), comment='标签')
    file_type = Column(String(64), comment='文件类型')
    order_num = Column(Integer, comment='排序号')
    content = Column(Text, comment='内容')
    last_update_time = Column(DateTime, comment='最后更新时间') 