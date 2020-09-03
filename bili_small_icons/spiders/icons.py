# -*- coding: utf-8 -*-
import scrapy
import time
import re
import json

from bili_small_icons.items import BiliSmallIconsItem


def GetTimeStamp():
    return str(round(time.time() * 1000))

class IconsSpider(scrapy.Spider):
    name = 'icons'
    allowed_domains = ['api.bilibili.com']
    start_urls = ['http://api.bilibili.com/']
    base_url = "https://api.bilibili.com/x/web-interface/index/icon?callback=jqueryCallback_bili_32425813458563235&jsonp=jsonp&_="

    def start_requests(self):
        yield scrapy.Request(url=self.base_url+GetTimeStamp(), callback=self.parse)

    def parse(self, response):
        jsonp_comp = re.compile(r".+\(({.*})\)")
        item_json = json.loads(re.findall(jsonp_comp,response.text)[0])

        item = BiliSmallIconsItem()
        item['iconID'] = item_json['data']['id']
        item['iconTitle'] = item_json['data']['title']
        item['links'] = item_json['data']['links']
        item['icon'] = item_json['data']['icon']
        item['weight'] = item_json['data']['weight']
        yield item

        yield scrapy.Request(url=self.base_url+GetTimeStamp(), callback=self.parse)
