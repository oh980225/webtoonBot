import scrapy
from scrapy.item import Item, Field

class WebtoonbotBotItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
