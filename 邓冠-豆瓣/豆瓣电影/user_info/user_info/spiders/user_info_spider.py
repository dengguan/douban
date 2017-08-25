# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from user_info.items import UserInfoItem
import time
import csv

class Douban(CrawlSpider):

    name = "movie_comments"
    redis_key = 'movie_comments:start_urls'
    start_urls = []


    # start_urls=['https://www.douban.com/people/china-undead/']
    #
    # url = 'https://www.douban.com/people/china-undead/'

    def start_requests(self):
        with open('D:/110.csv', 'rb') as csvfile:
             reader= csv.reader(csvfile)
             column=[row[3] for row in reader]
             print column
             for i in range(20,len(column)-1):

                self.start_urls.append(column[i])
             for url in self.start_urls:
                 yield self.make_requests_from_url(url)



    def parse(self,response):
        # print response.body
        item = UserInfoItem()
        selector = Selector(response)

        # movie_list = selector.xpath('//div[@class="star clearfix"]')
        # print movie_list
        #urls2 = selector.xpath('//*[@id="gaia"]/div[4]/div/a[1]/@href').extract()
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
