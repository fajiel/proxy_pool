# coding=utf-8
import re
import scrapy
from ProxyIP.util import verify_ip
from ProxyIP.items import ProxyipItem

class LiuliuipSpider(scrapy.Spider):
    name = u"proxy_66ip"
    start_urls = [u"http://www.66ip.cn/nmtq.php?"
                  u"getnum=800"
                  u"&isp=0"
                  u"&anonymoustype={}"
                  u"&start="
                  u"&ports="
                  u"&export="
                  u"&ipaddress="
                  u"&area=0"
                  u"&proxytype={}"
                  u"&api=66ip".format(anonymoustype, proxytype) for anonymoustype in range(3,5) for proxytype in range(0,2)]

    custom_settings = {
        'RETRY_TIMES' : 5,
        'DOWNLOAD_DELAY' : 5
    }

    def parse(self, response):
        url = response.url
        http_type = u"HTTPS" if u"proxytype=1" in url else u"HTTP"
        anonymous = u"高匿名" if u"anonymoustype=3" in url else u"超级匿名"
        content = response.text
        reip = re.compile(r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d{1,7}')
        ip_list = reip.findall(content)

        for ip_port in ip_list:
            ip = ip_port.split(":")[0]
            port = int(ip_port.split(":")[1])

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
            item['type'] = http_type
            item['res_time'] = ''
            item['verify_time'] = ''
            item['anonymous'] = anonymous
            item['status'] = 1
            yield item