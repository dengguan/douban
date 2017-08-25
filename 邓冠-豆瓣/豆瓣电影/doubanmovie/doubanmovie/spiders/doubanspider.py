# -*- coding: utf-8 -*-
#import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from doubanmovie.items import DoubanmovieItem

class Douban(CrawlSpider):
    name = "douban"
    redis_key = 'douban:start_urls'
    x=input("输入你要查找的电影名：")


    url = 'https://movie.douban.com/subject_search?search_text='+str(x)+'&cat=1002'
    start_urls = [url]


    def parse(self, response):
        item = DoubanmovieItem()
        selector = Selector(response)
        movies = selector.xpath('//div[@class="pl2"]')

        for each in movies:
            URL=each.xpath('a/@href').extract()

            title = each.xpath('a/text()').extract()
            title2=each.xpath('a/span/text()').extract()
            fullTitle = ''
            #//*[@id="content"]/div/div[1]/div[2]/table[1]/tbody/tr/td[2]/div/a/text()
            #//*[@id="content"]/div/div[1]/div[2]/table[1]/tbody/tr/td[2]/div/a/span
            for eachTitle in title:
                fullTitle +=eachTitle
            for eachTitle in title2:
                fullTitle +=eachTitle
            # print fullTitle

            movieInfo = each.xpath('p[@class="pl"]/text()').extract()
            # print movieInfo

            star = each.xpath('div[@class="star clearfix"]/span[@class="rating_nums"]/text()').extract()
            # print star

            #quote = each.xpath('div[@class="star clearfix"]/span[@class="rating_nums"]/text()').extract()
            #if quote:
                #quote = quote[0]
            #else:
                #quote = ''
            # print quote

            item['title'] = fullTitle
            item['movieInfo'] = ';'.join(movieInfo)
            item['star'] = star
            item['full_URL']=URL
            #item['quote'] = quote
            yield item
        nextLink = selector.xpath('//span[@class="next"]/link/@href').extract()
        if nextLink:
            nextLink = nextLink[0]
            print nextLink
            yield Request(nextLink, callback=self.parse)