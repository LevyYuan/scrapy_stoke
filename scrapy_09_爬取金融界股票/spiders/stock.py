# -*- coding: utf-8 -*-
import time
from urllib.parse import urlencode
from scrapy import Request, Spider
from scrapy_09_爬取金融界股票.items import StockItem
import json
import re


class StockSpider(Spider):
    name = 'stock'
    allowed_domains = ['q.jrjimg.cn','stb.hqquery.jrj.com.cn']
    start_urls = ['http://q.jrjimg.cn/']
    begin_url = "http://q.jrjimg.cn/?"
    new_url = "http://stb.hqquery.jrj.com.cn/stbhq.do?vname=stbhq_xsbqb&ABType=n&page={page}&size=50&order=desc&sort=pl&_dc={time}"

    def get_timestampt(self):
        t = time.time()
        timestamp = int(round(t * 1000))
        return timestamp

    def start_requests(self):
        page = 1050
        data = {'q': 'cn|s|sa', 'c': 'm', 'n': 'hqa', 'o': 'pl,d', 'p': page, '_dc': self.get_timestampt()}

        # yield Request(self.begin_url + urlencode(data), callback=self.parse, meta={'page': page})
        yield Request(self.new_url.format(page=1, time=self.get_timestampt()), callback=self.parse_new,
                      meta={'page': 1})

    # 解析深沪指
    def parse(self, response):
        # print(response.url)
        res = response.text[8:-2]
        wrap = re.search(r'HqData:([^}]*)', res).group(1)
        msg_lists = eval(wrap)

        for msg_list in msg_lists:
            item = StockItem()
            item['title'] = msg_list[2]
            item['chg'] = msg_list[12]
            item['new_price'] = msg_list[8]
            item['volume'] = msg_list[9]
            item['turnover'] = msg_list[10]
            item['top'] = msg_list[6]
            item['btn'] = msg_list[7]
            item['pre'] = msg_list[3]
            item['open'] = msg_list[5]
            item['pe_ratio'] = msg_list[-1]

            # print(item)
            yield item

        page = response.meta.get('page') + 1000
        data = {'q': 'cn|s|sa', 'c': 'm', 'n': 'hqa', 'o': 'pl,d', 'p': page, '_dc': self.get_timestampt()}
        url = self.begin_url + urlencode(data)

        yield Request(url, callback=self.parse, meta={'page': page})

    # 解析新三板
    def parse_new(self, response):
        print(response.url)

        # 数据清洗
        res = response.text[16:]
        # print(type(res))
        msg = re.search(r'"StockHq":([^}]*)', res).group(1)
        msg_lists = eval(msg)

        for msg_list in msg_lists:
            # print(msg_list)
            item = {}
            item['title'] = msg_list[1]
            # 最新价
            item['new_price'] = msg_list[4]
            # 涨跌幅
            item['chg'] = msg_list[5]
            # 涨跌额
            item['cha'] = msg_list[6]
            # 成交量
            item['volume'] = msg_list[7]
            # 成交额
            item['turnover'] = msg_list[8]
            # 最高
            item['top'] = msg_list[11]
            # 最低
            item['btn'] = msg_list[12]
            # 昨收
            item['pre'] = msg_list[10]
            # 今开
            item['open'] = msg_list[9]
            print(item)

        page = response.meta.get('page') + 1
        print(page)
        print(self.new_url.format(page=page, time=self.get_timestampt()))

        yield Request(self.new_url.format(page=page, time=self.get_timestampt()), callback=self.parse_new,
                      meta={'page': page})


