# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class StockItem(Item):
    title = Field()
    chg = Field()
    new_price = Field()
    volume = Field()
    turnover = Field()
    top = Field()
    btn = Field()
    pre = Field()
    open = Field()
    pe_ratio = Field()
