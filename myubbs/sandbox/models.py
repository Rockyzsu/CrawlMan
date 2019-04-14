# -*-coding=utf-8-*-

# @Time : 2018/9/26 9:25
# @File : models.py

from sqlalchemy import Column, String, DateTime, Integer, Text, create_engine, DATE
from sqlalchemy.ext.declarative import declarative_base
import datetime
from sqlalchemy.orm import sessionmaker
from sandbox import config

Base = declarative_base()
engine = create_engine('mysql+pymysql://{}:{}@{}:3306/spider?charset=utf8'.format(config.username,config.password,config.mysql_ip))
DBSession = sessionmaker(bind=engine)

TABLE_NAME = 'tb_myubbs'

# ORM 模型，根据项目需求修改
class SpiderModels(Base):
    __tablename__ = TABLE_NAME


    # 根据项目修改字段
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(400))
    pubdate = Column(DateTime)
    content = Column(Text)
    author = Column(String(100))
    url = Column(String(200))
    crawltime = Column(DateTime, default=datetime.datetime.now(), comment='抓取时间')


Base.metadata.create_all(engine)