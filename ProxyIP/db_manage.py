# coding=utf-8
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#  Create base for base
Base = declarative_base()
engine = create_engine('mysql+mysqlconnector://root:''@localhost:3306/Scrapy?charset=utf8', echo=False)


class ProxyIP(Base):
    __tablename__ = 'proxy_ip'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    # id = Column(Integer, primary_key=True, nullable=False)
    ip = Column(String(20), primary_key=True, nullable=False)
    port = Column(String(10), primary_key=True, nullable=False)
    addr = Column(String(50))
    type = Column(String(50))
    res_time = Column(String(20))
    verify_time = Column(String(20))
    status = Column(Integer, nullable=False)
    anonymous = Column(String(20))
    # create_time = Column(TIMESTAMP, nullable=False, default=str(datetime.now()))
    update_time = Column(TIMESTAMP, nullable=False, onupdate=str(datetime.now()))
