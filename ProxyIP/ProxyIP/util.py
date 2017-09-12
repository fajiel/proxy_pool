# -*- coding: utf-8 -*-

import re
import time
import requests
from selenium import webdriver

def get_profile(ip, port):
    profile = webdriver.FirefoxProfile()
    profile.set_preference(u"network.proxy.type", 1)
    profile.set_preference(u"network.proxy.http", ip)
    profile.set_preference(u"network.proxy.http_port", port)
    profile.update_preferences()
    return profile

def verify_ip(ip, port):
    ip_proxy = "https://{}:{}".format(ip, port)
    proxies = {"https": ip_proxy}
    print(u"正在验证的IP及端口号为{}:{}".format(ip, port))
    isvalid = False
    try:
        resp = requests.get('https://www.baidu.com', proxies=proxies, timeout=20)
        if resp.status_code == 200:
            isvalid = True
    except Exception as e:
        print(e)
    return isvalid

def query_ip():
    from ProxyIP.ProxyIP.db_manage import sessionmaker, engine, ProxyIP
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    query = session.query(ProxyIP)
    query_obj_list = query.filter_by(status=1).all()
    ip_list = [(query_obj.ip, int(query_obj.port)) for query_obj in query_obj_list]
    session.close()
    return ip_list

def del_ip(ip, port):
    from ProxyIP.ProxyIP.db_manage import sessionmaker, engine, ProxyIP
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    query = session.query(ProxyIP)
    query_obj_list = query.filter_by(ip = ip, port = port).all()
    if len(query_obj_list) == 0:
        print (u"数据库中不存在该IP及端口号：{}:{}".format(ip, port))
    for query_obj in query_obj_list:
        print (u"已删除:{}:{}".format(query_obj.ip, query_obj.port))
        session.delete(query_obj)
    session.commit()
    session.close()
