# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from group_info.items import GroupInfoItem
import time
import csv

class Douban(CrawlSpider):

    name = "group_info"
    redis_key = 'group_info:start_urls'
    start_urls = []


    #start_urls=['https://movie.douban.com/subject/26260853/comments?start=20&limit=20&sort=new_score&status=P']

    #url = 'https://movie.douban.com/subject/26260853/comments?start=20&limit=20&sort=new_score&status=P'
    def start_requests(self):
        with open('D:/group_topic_list.csv', 'rb') as csvfile:
            reader= csv.DictReader(csvfile)
            column=[row['group_url'] for row in reader]
            print column
            for i in range(0,len(column)-1):

                self.start_urls.append(column[i])

            for url in self.start_urls:
                yield self.make_requests_from_url(url)



    def parse(self,response):
        # print response.body
        item = GroupInfoItem()
        selector = Selector(response)

        # movie_list = selector.xpath('//div[@class="star clearfix"]')
        # print movie_list
        #urls2 = selector.xpath('//*[@id="gaia"]/div[4]/div/a[1]/@href').extract()
        group_name = selector.xpath('//div[@id="content"]/div[@id="group-info"]/h1/text()').extract()
        print group_name


        time = selector.xpath('//div[@class="group-board"]/p/text()').extract()
        grouper=selector.xpath('//div[@class="group-board"]/p/a/text()').extract()

        group_info=selector.xpath('//div[@class="group-board"]/div[@class="group-intro"]/text()').extract()
        tags=selector.xpath('//div[@class="group-tags"]/a/text()').extract()
        table=''
        for each in tags:
            table+=each

        item['group_name'] = group_name
        item['grouper']=grouper
        item['group_info'] = group_info
        item['table'] = ';'.join(table)
        item['time'] = time
            #item['quote'] = quote
        yield item
