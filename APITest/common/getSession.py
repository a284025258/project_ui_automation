from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASES

engine = create_engine(DATABASES, encoding="utf-8")
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
session = DBSession()
