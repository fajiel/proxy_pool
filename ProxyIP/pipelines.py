# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from ProxyIP.db_manage import sessionmaker, ProxyIP, engine
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

class ProxyipPipeline(object):
    def process_item(self, item, spider):

        query = session.query(ProxyIP)
        query_obj = query.filter_by(ip=item['ip'], port=item['port']).first()
        if query_obj is None:
            result = ProxyIP(**item)
            session.add(result)
        else:
            query_obj.status = item["status"]
            query_obj.verify_time = item["verify_time"]
            query_obj.type = item["type"]
            query_obj.addr = item["addr"]
            session.merge(query_obj)

        try:
            session.commit()
        except Exception as e:
            logging.exception('==== error in ProxyipPipeline ====')
            session.rollback()
        session.close()
        return item