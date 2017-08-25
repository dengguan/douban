# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from topic_comments.items import TopicCommentsItem
import time
import csv

class Douban(CrawlSpider):

    name = "topic_comments"
    redis_key = 'topic_comments:start_urls'
    start_urls = []


    #start_urls=['https://movie.douban.com/subject/26260853/comments?start=20&limit=20&sort=new_score&status=P']

    #url = 'https://movie.douban.com/subject/26260853/comments?start=20&limit=20&sort=new_score&status=P'
    def start_requests(self):
        with open('D:/group_topic_list.csv', 'rb') as csvfile:
            reader= csv.reader(csvfile)
            column=[row[0] for row in reader]
            print column
            for i in range(1,len(column)-1):
                self.start_urls.append(column[i])

            for url in self.start_urls:
                yield self.make_requests_from_url(url)



    def parse(self,response):
        # print response.body
        item = TopicCommentsItem()
        selector = Selector(response)

        # movie_list = selector.xpath('//div[@class="star clearfix"]')
        # print movie_list
        #urls2 = selector.xpath('//*[@id="gaia"]/div[4]/div/a[1]/@href').extract()
        movie_comment_1 = selector.xpath('//div[@class="article"]/div[@class="comments-wrapper"]')
        print movie_comment_1





        Comments = selector.xpath('//li[@class="clearfix comment-item"]')
        for eachMoive in Comments:
              usename = eachMoive.xpath('div[@class="reply-doc content"]/div[@class="bg-img-green"]/h4/a/text()').extract()

              comment = eachMoive.xpath('div[@class="reply-doc content"]/p/text()').extract()
              user_url=eachMoive.xpath('div[@class="reply-doc content"]/div[@class="bg-img-green"]/h4/a/@href').extract()
              #//*[@id="comments"]/div[1]/div[2]/h3/span[2]/a
              #votes=eachMoive.xpath('div[@class="comment"]/h3/span[@class="comment-vote"]/span[@class="vote-count"]/text()').extract()
              time = eachMoive.xpath('div[@class="reply-doc content"]/div[@class="bg-img-green"]/h4/span[@class="pubtime"]/text()').extract()
            #quote = eachMoive.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            #quote可能为空，因此需要先进行判断
            #if quote:
                #quote = quote[0]
            #else:
                #quote = ''
              item['usename'] = usename
              item['user_url']=user_url

              item['comment'] = ';'.join(comment)
              item['time'] = time
            #item['quote'] = quote
              yield item

        #第10页是最后一页，没有下一页的链接
        #//*[@id="paginator"]/a
        #//*[@id="paginator"]/a[3]
        #https://movie.douban.com/subject/26260853/comments?status=P
        #https://movie.douban.com/subject/26260853/comments?start=20&limit=20&sort=new_score&status=P


        # if nextLink:
        #        nextLink = nextLink[0]
        #        print nextLink
        #        yield Request('https://movie.douban.com/subject/26260853/comments' + nextLink,callback=self.parse)
