# -*- coding: utf-8 -*-
#import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from douban_music.items import DoubanMusicItem

class Douban(CrawlSpider):
    name = "douban"
    redis_key = 'douban:start_urls'

    x=input("输入你要查找的歌曲：")
    url = "https://music.douban.com/subject_search?search_text="+str(x)+"&cat=1003"
    start_urls = [url]


    def parse(self, response):
        item = DoubanMusicItem()
        selector = Selector(response)
        musics = selector.xpath('//div[@class="pl2"]')

        for each in musics:
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

            musicInfo = each.xpath('p[@class="pl"]/text()').extract()
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
            item['musicInfo'] = ';'.join(musicInfo)
            item['star'] = star
            item['full_URL']=URL
            #item['quote'] = quote
            yield item
        nextLink = selector.xpath('//span[@class="next"]/a/@href').extract()
        if nextLink:
            nextLink = nextLink[0]
            print nextLink
            yield Request(nextLink, callback=self.parse)