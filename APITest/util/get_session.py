"""
获取数据库连接
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASES


def get_session():
    engine = create_engine(DATABASES, echo=True)
    session_maker = sessionmaker(bind=engine)
    return session_maker()
