# -*- coding: utf-8 -*-
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey, Float
from sqlalchemy import event
from sqlalchemy import DDL

engine = create_engine('mysql+pymysql://root:@localhost:3306/db_parker?charset=utf8')
DBSession = sessionmaker(bind=engine)
Base = declarative_base()


class Apps(Base):
    __tablename__ = 'tb_apps3'
    id = Column(Integer, primary_key=True)
    app_rank = Column(Integer, index=True)
    appName = Column(String(150), index=True)
    developCompanyFullName = Column(String(180),index=True)
    second_cateName = Column(String(150))
    first_cateName = Column(String(150))
    appId = Column(String(150))
    activeNums = Column(Float)
    activeAvgDay = Column(Float)
    runtimeAvgDay = Column(Float)
    runtimeAvgPersonRatio = Column(Float)
    activeAvgDayRatio = Column(Float)
    runtimeNums = Column(Float)
    launchNums = Column(Float)
    runtimeNumsRatio = Column(Float)
    launchAvgDayRatio = Column(Float)
    statDate = Column(DateTime)
    developCompanyAbbr = Column(String(180))


Base.metadata.create_all(engine)
