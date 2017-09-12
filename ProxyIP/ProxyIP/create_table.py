# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, String, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlalchemy.engine.url import URL
import logging
from datetime import datetime

DB_SETTING = {
    'drivername': 'mysql+mysqlconnector',
    'host': '127.0.0.1',
    'port': '3306',
    'database': 'Proxy',
    'username': 'root',
    'password': '',
    'query': {
        'charset': 'utf8'
    }
	}
	
Base = declarative_base()

class Tmp(Base):
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


def db_connect():
    return create_engine(URL(**DB_SETTING), pool_size=10, pool_recycle=3600, max_overflow=20)

if __name__ =='__main__':

    logger = logging.getLogger('')
    hdlr = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)

    try:
        Base.metadata.create_all(db_connect())
    except Exception:
        logging.exception('create failed')
    else:
        logging.info('created')
