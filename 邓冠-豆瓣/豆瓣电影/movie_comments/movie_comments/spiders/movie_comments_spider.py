# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from movie_comments.items import MovieCommentsItem
import time
import csv

class Douban(CrawlSpider):

    name = "movie_comments"
    redis_key = 'movie_comments:start_urls'
    start_urls = []


    #start_urls=['https://movie.douban.com/subject/26260853/comments?start=20&limit=20&sort=new_score&status=P']

    #url = 'https://movie.douban.com/subject/26260853/comments?start=20&limit=20&sort=new_score&status=P'
    def start_requests(self):
        with open('D:/movie_list.csv', 'rb') as csvfile:
            reader= csv.reader(csvfile)
            column=[row[2] for row in reader]
            print column
            for i in range(1,len(column)-1):
                for a in range(1,10):
                  self.start_urls.append(column[i]+"/comments?start="+str(a*20)+"&limit=20&sort=new_score&status=P"or column[i]+"/comments?status=P")

            for url in self.start_urls:
                yield self.make_requests_from_url(url)



    def parse(self,response):
        # print response.body
        item = MovieCommentsItem()
        selector = Selector(response)

        # movie_list = selector.xpath('//div[@class="star clearfix"]')
        # print movie_list
        #urls2 = selector.xpath('//*[@id="gaia"]/div[4]/div/a[1]/@href').extract()
        movie_comment_1 = selector.xpath('//div[@class="article"]/div[@class="mod-bd"]')
        print movie_comment_1
        #movie_comment_2 = selector.xpath('//div[@class="main page-sa Fix"]')
        #nextLink = selector.xpath('//*[@id="paginator"]/a[3]/@href').extract()

        # if movie_list:
        #
        #     #urls2 = selector.xpath('//*[@id="gaia"]/div[4]/div/a[1]').extract()
        #     urls = movie_list.xpath('//td[@valign="top"]/div[@class="pl2"]/a/@href').extract()
        #     print urls
            # moive_name=movie_list.xpath('//table[@width="100%"]/tbody/td[@valign="top"]/div[@class="pl2"]/span/text()')
            # #//*[@id="content"]/div/div[1]/div[2]/table[2]/tbody/tr/td[2]/div/a
            # full_title=''
            # for each in moive_name:
            #     full_title+=each
            #     item['full_title']=full_title
            #     yield item
            # for each in urls:
            #     #https://movie.douban.com/subject/26260853/comments?start=20&limit=20&sort=new_score&status=P
            #     next = each+"comments?start=20&limit=20&sort=new_score&status=P"
            #     yield Request(next, callback=self.parse)
            # nextLink = selector.xpath('//div[@class="paginator"]/span[@class="next"]/a/@href').extract()
            # if nextLink:
            #     print nextLink[0]
            #     yield Request(nextLink[0], callback=self.parse)


        if movie_comment_1:

         Comments = selector.xpath('//div[@class="comment-item"]')
         for eachMoive in Comments:
              usename = eachMoive.xpath('div[@class="comment"]/h3/span[@class="comment-info"]/a/text()').extract()

              comment = eachMoive.xpath('div[@class="comment"]/p/text()').extract()
              user_url=eachMoive.xpath('div[@class="comment"]/h3/span[@class="comment-info"]/a/@href').extract()
              #//*[@id="comments"]/div[1]/div[2]/h3/span[2]/a
              votes=eachMoive.xpath('div[@class="comment"]/h3/span[@class="comment-vote"]/span[@class="votes"]/text()').extract()
              time = eachMoive.xpath('div[@class="comment"]/h3/span[@class="comment-info"]/span[@class="comment-time "]/text()').extract()
            #quote = eachMoive.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            #quote可能为空，因此需要先进行判断
            #if quote:
                #quote = quote[0]
            #else:
                #quote = ''
              item['usename'] = usename
              item['user_url']=user_url
              item['votes'] = votes
              item['comment'] = ';'.join(comment)
              item['time'] = time
            #item['quote'] = quote
              yield item
        nextLink = selector.xpath('//*[@id="paginator"]/a[@class="next"]/@href').extract()
        #第10页是最后一页，没有下一页的链接
        #//*[@id="paginator"]/a
        #//*[@id="paginator"]/a[3]
        #https://movie.douban.com/subject/26260853/comments?status=P
        #https://movie.douban.com/subject/26260853/comments?start=20&limit=20&sort=new_score&status=P


        # if nextLink:
        #        nextLink = nextLink[0]
        #        print nextLink
        #        yield Request('https://movie.douban.com/subject/26260853/comments' + nextLink,callback=self.parse)
