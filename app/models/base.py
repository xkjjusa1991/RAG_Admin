'''
Author: xiakaijia xkjjusa1991@qq.com
Date: 2025-02-10 09:03:26
LastEditors: xiakaijia xkjjusa1991@qq.com
LastEditTime: 2025-02-10 09:03:32
FilePath: \RAG_Admin\app\models\base.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
"""
基础模型模块
"""
from app.core.database import Base

# 导出 Base 类供其他模型使用
__all__ = ['Base'] 