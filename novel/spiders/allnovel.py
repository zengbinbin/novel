import scrapy
from novel.items import NovelItem

class AllNovel(scrapy.Spider):
    name = "allnovel"
    start_urls = ["https://www.booktxt.net/xiaoshuodaquan/"]

    # 解析
    # def parse(self, response):
    #    for quote in response.css("div#list dd a"):
    #        next_page = quote.css("a::attr(href)").get()
    #        yield {
    #            "url:": next_page,
    #            "name:": quote.css("a::text").get()
    #        }

    def parse(self, response):
        # 获取页面所有小说名称和url
        for quote in response.css(".novellist ul li a"):
            next_page = quote.css("a::attr(href)").get()
            if next_page is not None: 
                yield response.follow(next_page, self.parse_item)
                # yield {
                #    "url": next_page,
                #    "name": quote.css("a::text").get()
                # }

    # 获取小说的每个章节和页面
    def parse_item(self, response):
        # 获取所有字页面
        for quote in response.css("div#list dd a"):
            next_page = quote.css("a::attr(href)").get()
            if next_page is not None:
                yield response.follow(next_page, self.parse_content)

    # 抽取每个页面的标题和内容           
    def parse_content(self, response):
        item = NovelItem()
        item['name'] = response.css("div.bookname h1::text").get()
        item['content'] = response.css("div#content::text").getall()
        yield item     


        