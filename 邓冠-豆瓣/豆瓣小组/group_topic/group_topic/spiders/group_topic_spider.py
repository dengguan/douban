# -*- coding: utf-8 -*-
#import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from group_topic.items import GroupTopicItem

class Douban(CrawlSpider):
    name = "group_topic"
    redis_key = 'group_topic:start_urls'
    start_urls = ['https://www.douban.com/group/explore']

    url = 'https://www.douban.com/group/explore'


    def parse(self, response):
        item = GroupTopicItem()
        selector = Selector(response)
        topic_list_page = selector.xpath('//div[@class="channel-item"]')
        topic_content_page=selector.xpath('//div[@class="topic-content"]')

        for each in topic_list_page:
               topic_name=each.xpath('div[@class="bd"]/h3/a/text()').extract()
               topic_url=each.xpath('div[@class="bd"]/h3/a/@href').extract()

               group_url=each.xpath('div[@class="bd"]/div[@class="source"]/span[@class="from"]/a/@href').extract()
               group_name = each.xpath('div[@class="bd"]/div[@class="source"]/span[@class="from"]/a/text()').extract()
            #//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/h3/a
            #//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/div[2]/span[1]/a
               #//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/h3/a
               #topic_urls=topic_list_page.xpath('//div[@class="channel-item"]/div[@class="bd"]/h3/a/@href').extract()
               item['group_url']=group_url
               item['topic_url']=topic_url
               item['topic_name']=topic_name
               item['group_name']=group_name

               yield item

               nextLink = selector.xpath('//span[@class="next"]/link/@href').extract()
               if nextLink:
                  nextLink = nextLink[0]
                  print nextLink
                  yield Request('https://www.douban.com/group/explore'+nextLink, callback=self.parse)




        # if topic_content_page:
        #     author=topic_content_page.xpath('//div[@class="topic-doc"]/h3/span[@class="from"]/a/text()').extract()
        #
        #     time=topic_content_page.xpath('//div[@class="topic-doc"]/h3/span[@class="color-green"]/text()').extract()
        #     title=topic_content_page.xpath('//table[@class="infobox"]/tbody/tr/td[@class="tablecc"]/text()').extract()
        #     like=topic_content_page.xpath('//div[@class="sns-bar-fav"]/span[@class="fav-num"]/a/text()').extract()
        #     group_name=topic_content_page.xpath('//div[@class="info"]/div[@class="title"]/a/text()').extract()
        #
        #     item['author'] = author
        #
        #
        #     item['time'] = time
        #     item['title'] = title
        #     item['like'] = like
        #     item['group_name'] = group_name
        #
        #     #item['quote'] = quote
        #     yield item
        # # nextLink = selector.xpath('//span[@class="next"]/link/@href').extract()
        # # if nextLink:
        # #     nextLink = nextLink[0]
        # #     print nextLink
        # #     yield Request('https://www.douban.com/group/explore'+nextLink, callback=self.parse)