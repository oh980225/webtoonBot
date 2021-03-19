import scrapy
from scrapy.spiders import Spider
from webtoonBot.items import WebtoonbotBotItem
from scrapy.http import Request
from datetime import datetime
from . import myWebtoon


class webtoonBotSpider(scrapy.Spider):
    name = "webtoonBot"  #spider 이름
    allowed_domains = ["https://comic.naver.com/webtoon/weekday.nhn"]  #최상위 도메인

    def __init__(self):
        self.weekIdx = 0
        self.days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

    #1번만 실행
    def start_requests(self):
        self.weekIdx = datetime.today().weekday();
        curHour = datetime.now().hour;
        if curHour >= 23:
            self.weekIdx += 1
            if self.weekIdx == 7:
                self.weekIdx = 0
        yield scrapy.Request("https://comic.naver.com/webtoon/weekdayList.nhn?week={}".format(self.days[self.weekIdx]),self.parse)
 
    #아이템 parse
    def parse(self, response):
        webtoons = myWebtoon.toonList[self.weekIdx]
        print(webtoons)
        for colum in  response.xpath('//div[@class="list_area daily_img"]/ul[@class="img_list"]/li') :
            item = WebtoonbotBotItem() 
            if colum.xpath('dl/dt/a/@title').extract_first() in webtoons and colum.xpath('div[@class="thumb"]/a/em[@class="ico_updt"]').extract_first():
                item['title'] = colum.xpath('dl/dt/a/@title').extract_first()
                item['content'] = "해당 웹툰이 업로드 되었습니다!"
            else:
                continue
            yield item