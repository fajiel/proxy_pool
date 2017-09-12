# coding=utf-8
"""

Author : xietian@sansi.com

Date : 2017-08-16

"""
import re
import scrapy
from ProxyIP.util import verify_ip
from ProxyIP.items import ProxyipItem

class LiunianSpider(scrapy.Spider):
    name = "proxy_liunian"
    start_urls = [u"http://www.89ip.cn/tiqv.php?sxb=&tqsl=1000&ports=&ktip=&xl=on&submit=%CC%E1++%C8%A1"]

    custom_settings = {
        'RETRY_TIMES' : 5,
        'DOWNLOAD_DELAY' : 5
    }

    def parse(self, response):

        ip_list = response.xpath("/html/body/div/text()")[8 : -1]

        for one_ip in ip_list:
            ip = one_ip.extract().split(":")[0].strip()
            port = int(one_ip.extract().split(":")[-1])

            if (not ip) and (not port):
                continue
            if not re.match(r'^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$', ip):
                continue

            isvalid = verify_ip(ip, port)
            if not isvalid:
                continue

            print(u"恭喜恭喜，获取一条有效IP！")

            item = ProxyipItem()
            item['ip'] = ip
            item['port'] = int(port)
            item['addr'] = ''
            item['type'] = ''
            item['res_time'] = ''
            item['verify_time'] = ''
            item['anonymous'] = ''
            item['status'] = 1
            yield item