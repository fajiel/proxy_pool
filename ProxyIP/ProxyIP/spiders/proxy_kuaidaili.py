# -*- coding: utf-8 -*-
"""
Author:lifajie@sansi.com

Date:2017-08-16

"""
import re
import scrapy
from ProxyIP.util import verify_ip
from ProxyIP.items import ProxyipItem

class KuaiSpider(scrapy.Spider):
    name = "proxy_kuai"
    # start_urls = [u"http://www.kuaidaili.com/free/inha/1/",]
    start_urls = [u"http://www.kuaidaili.com/free/inha/{}/".format(i) for i in range(1, 20)]

    headers = {
        'Host': 'www.kuaidaili.com',
        'Referer': 'http://www.kuaidaili.com/free/inha/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'
    }
    custom_settings = {
        'RETRY_TIMES': 5,
        'DOWNLOAD_DELAY': 5,
    }


    def parse(self, response):
        item_list = response.css("#list").xpath("table/tbody/tr")
        for item in item_list:
            sip_list = item.xpath('.//td')
            if len(sip_list) == 0:
                continue
            ip = sip_list[0].xpath("text()").extract_first()
            port = sip_list[1].xpath("text()").extract_first()
            anonymous = sip_list[2].xpath("text()").extract_first()
            http_type = sip_list[3].xpath("text()").extract_first()
            addr = sip_list[4].xpath("text()").extract_first()
            res_time = sip_list[5].xpath("text()").extract_first()
            verify_time = sip_list[6].xpath("text()").extract_first()

            if (not ip) and (not port):
                continue
            if not re.match('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$', ip):
                continue

            port = int(port)
            isvalid = verify_ip(ip, port)
            if not isvalid:
                continue

            print (u"恭喜恭喜，获取一条有效IP！")

            item = ProxyipItem()
            item['ip'] = ip
            item['port'] = port
            item['addr'] = addr
            item['type'] = http_type.upper()
            item['res_time'] = res_time
            item['verify_time'] = verify_time
            item['anonymous'] = anonymous
            item['status'] = 1
            yield item
