# -*- coding: utf-8 -*-

import re
import scrapy
from ProxyIP.util import verify_ip
from ProxyIP.items import ProxyipItem

class XiciSpider(scrapy.Spider):
    name = "proxy_xici"
    # start_urls = [u"http://www.xicidaili.com/nn/1"]
    start_urls = [u"http://www.xicidaili.com/nn/{}".format(i) for i in range(1, 20)]

    custom_settings = {
        'RETRY_TIMES': 5,
        'DOWNLOAD_DELAY': 5,
    }

    def parse(self, response):
        item_list = response.css("#ip_list").xpath(".//tr")
        for item in item_list:
            sip_list = item.xpath('.//td')
            if len(sip_list) == 0:
                continue
            ip = sip_list[1].xpath("text()").extract_first()
            port = sip_list[2].xpath("text()").extract_first()
            addr = sip_list[3].xpath("./a/text()").extract_first()
            anonymous = sip_list[4].xpath("text()").extract_first()
            http_type = sip_list[5].xpath("text()").extract_first()
            res_time = sip_list[6].xpath("./div/@title").extract_first()
            verify_time = sip_list[9].xpath("text()").extract_first()

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
