# -*- coding:utf-8 -*-
import scrapy
import re
from scrapy.selector import Selector
from user_info.items import UserInfoItem
import csv
from scrapy.http import Request


class DmozSpider(scrapy.Spider):
    name = "user_info"
    redis_key = 'user_info:start_urls'
    start_urls = []
    #url = 'http://www.dianping.com/member/'

    def start_requests(self):
        with open('D:/topic_comments_list.csv', 'rb') as csvfile:
             reader= csv.DictReader(csvfile)
             column=[row['user_url'] for row in reader]
             print column
             for i in range(0,len(column)-1):

                self.start_urls.append(column[i]+'members')
             for url in self.start_urls:
                 yield self.make_requests_from_url(url)

    def parse(self, response):


        item = UserInfoItem()
        selector = Selector(response)
        member_list=selector.xpath('//div[@class="mod"]')
        user_info_page=selector.xpath('//div[@id="db-usr-profile"]')
        if member_list:
            members_urls = member_list.xpath('//div[@class="name"]/a/@href').extract()
            for each in members_urls:
                #next = "http://www.dianping.com"+each+"/review_more"
                yield Request(each, callback=self.parse)
            nextLink = selector.xpath('//span[@class="next"]/a/@href').extract()
            if nextLink:
                yield Request(nextLink[0], callback=self.parse)


        # movie_list = selector.xpath('//div[@class="star clearfix"]')
        # print movie_list
        #urls2 = selector.xpath('//*[@id="gaia"]/div[4]/div/a[1]/@href').extract()
        if user_info_page:

            user_info = selector.xpath('//div[@class="infobox"]/div[@class="bd"]')
            print user_info


            description=selector.xpath('//div[@id="edit_intro"]/span[@id="intro_display"]/text()').extract()
            usename=selector.xpath('//div[@class="info"]/h1/text()').extract()
            live_city=selector.xpath('//div[@class="basic-info"]/div[@class="user-info"]/a/text()').extract()
            user_info=selector.xpath('//div[@class="user-info"]/div[@class="pl"]/text()').extract()
        #//*[@id="intro_display"]/text()[2]
        #u_information=selector.xpath('//div[@class="user-intro"]/div[@id="edit_intro"]/div[@id="intro_display"]/text()[4]').extract()

            item['live_city'] = live_city
            item['user_info']=user_info
            item['usename']=usename
            item['description']=description

        #item['u_information'] = ';'.join(u_information)


            yield item



