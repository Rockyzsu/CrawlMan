# -*-coding=utf-8-*-

# @Time : 2018/9/26 9:25
# @File : models.py

from sqlalchemy import Column, String, DateTime, Integer, Text, create_engine, DATE
from sqlalchemy.ext.declarative import declarative_base
import datetime
from sqlalchemy.orm import sessionmaker
from sandbox import config

Base = declarative_base()
engine = create_engine('mysql+pymysql://{}:{}@{}:3367/spider?charset=utf8'.format(config.username,config.password,config.mysql_ip))
DBSession = sessionmaker(bind=engine)

TABLE_NAME = 'card_bin_scrapy'

# ORM 模型，根据项目需求修改
class SpiderModels(Base):
    __tablename__ = TABLE_NAME


    # 根据项目修改字段
    id = Column(Integer, primary_key=True, autoincrement=True)
    card=Column(Text, comment='卡号')
    accountLength = Column(Text, comment='长度')
    cardName = Column(Text, comment='卡名')
    cardType = Column(Text, comment='卡类型')
    mainAccount = Column(Text, comment='主账号')
    mainValue = Column(Text, comment='主账号值')
    orgName = Column(Text, comment='发卡行')

    origin = Column(String(30), comment='来源')
    crawltime = Column(DateTime, default=datetime.datetime.now(), comment='抓取时间')


Base.metadata.create_all(engine)