# -*- coding: utf-8 -*-
from sqlalchemy import Column, String , DateTime, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
import db_config
import datetime

Base = declarative_base()

class Fraud(Base):
    __tablename__ = 'frauds'

    id = Column(Integer, primary_key=True)
    executed_name = Column(String(50))
    gender = Column(String(10))
    age = Column(String(10))
    identity_number = Column(String(50))
    court = Column(String(200))
    province = Column(String(50))
    case_number = Column(String(100))
    performance = Column(String(100))  # 被执行人的履行情况
    disrupt_type_name = Column(Text)  # 失信被执行人行为具体情形
    duty = Column(Text)  # 生效法律文书确定的义务
    release_time = Column(String(50))
    crawl_time = Column(DateTime, default=datetime.datetime.now())
    data_resource = Column(String(50), default='baidu_api')

Base.metadata.create_all(db_config.engine)
