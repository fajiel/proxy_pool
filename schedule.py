# -*- coding: utf-8 -*-

import os
import time
from apscheduler.schedulers.background import BackgroundScheduler

TIME_DAY_XICI = 2.5
TIME_DAY_KUAI = 2
TIME_DAY_LLIP = 1.5
TIME_DAY_CHECK = 0.25

def schedule_xici():
    print (os.path.realpath(__file__))
    # schedule_xici = os.popen("curl http://localhost:6800/schedule.json -d project=ProxyIP -d spider=proxy_xici")
    sche_xici = os.popen("scrapy crawl proxy_xici")
    result = sche_xici.read()
    print(result)

def schedule_kuai():
    print (os.path.realpath(__file__))
    # schedule_xici = os.popen("curl http://localhost:6800/schedule.json -d project=ProxyIP -d spider=proxy_kuai")
    sche_kuai = os.popen("scrapy crawl proxy_kuai")
    result = sche_kuai.read()
    print(result)

def schedule_66ip():
    print (os.path.realpath(__file__))
    # schedule_xici = os.popen("curl http://localhost:6800/schedule.json -d project=ProxyIP -d spider=proxy_66ip")
    sched_66ip = os.popen("scrapy crawl proxy_66ip")
    result = sched_66ip.read()
    print(result)

def schedule_check():
    from ProxyIP.util import query_ip, verify_ip, del_ip
    ip_list = query_ip()
    for ip, port in ip_list:
        if verify_ip(ip, port):
            continue
        del_ip(ip, port)

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(schedule_check, 'interval', seconds=TIME_DAY_CHECK * 24*60*60)
    scheduler.add_job(schedule_xici, 'interval', seconds=TIME_DAY_XICI * 24*60*60)
    scheduler.add_job(schedule_kuai, 'interval', seconds=TIME_DAY_KUAI * 24*60*60)
    scheduler.add_job(schedule_66ip, 'interval', seconds=TIME_DAY_LLIP * 24*60*60)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        while True:
            time.sleep(60)
            print('sleep!')
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print('Exit The Job!')