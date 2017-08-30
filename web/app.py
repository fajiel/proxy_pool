# -*- coding: utf-8 -*-
import random
import json
from flask import Flask, request
from ProxyIP.db_manage import sessionmaker, engine, ProxyIP

app = Flask(__name__)

@app.route('/api/proxy/get_one/', methods=['POST','GET'])
def get_one():
    """
    获取一个代理ip
    """
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    query = session.query(ProxyIP)
    query_obj_list = query.filter_by(status=1).all()
    query_obj = query_obj_list[random.randint(0, len(query_obj_list) - 1)]
    proxy_ip = "{}:{}".format(query_obj.ip, query_obj.port)
    session.close()
    return proxy_ip

@app.route('/api/proxy/get_ip/', methods=['POST', 'GET'])
def get_ip():
    """
    获取多个代理ip
    """

    if request.method == 'POST':
        num = request.form['num']
    else:
        num = request.args.get('num')
    if not num:
        num = 1
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    query = session.query(ProxyIP)
    query_obj_list = query.filter_by(status=1).all()
    proxy_list = []
    count = len(query_obj_list) - 1
    for i in range(int(num)):
        query_obj = query_obj_list[random.randint(0, count)]
        proxy_ip = "{}:{}".format(query_obj.ip, query_obj.port)
        if proxy_ip in proxy_list:
            continue
        proxy_list.append(proxy_ip)

    result = json.dumps(proxy_list)
    return result

if __name__ == "__main__":
    app.run(host='0.0.0.0')