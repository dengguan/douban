# -*- coding:utf-8 -*-
import scrapy
import re
from scrapy.selector import Selector
from book_comments.items import BookCommentsItem
from scrapy.http import Request


class DmozSpider(scrapy.Spider):
    name = "book_comments"
    redis_key = 'book_comments:start_urls'
    # x = input("输入要爬信息:")
    # y = input("输入要爬城市id:")
    url = "https://book.douban.com"
    x=input("输入你要查找的书名：")
    s_u = "https://book.douban.com/subject_search?search_text="+str(x)+"&cat=1001"
    start_urls = [s_u]

    def parse(self, response):
        item = BookCommentsItem()
        selector = Selector(response)
        book_list = selector.xpath('//ul[@class="subject-list"]')
        #shop_comment_1 = selector.xpath('//div[@class="comments-wrapper"]')
        shop_comment_2 = selector.xpath('//div[@class="comments-wrapper"]')

        if book_list:
            urls = book_list.xpath('//div[@class="info"]/h2/a/@href').extract()
            for each in urls:
                for i in range(1,10):
                  next = each+"comments/hot?p="+str (i)
                  yield Request(next, callback=self.parse)
            nextLink = selector.xpath('//div[@class="paginator"]/span[@class="next"]/a/@href').extract()
            if nextLink:
                yield Request("https://book.douban.com"+nextLink[0], callback=self.parse)

        if shop_comment_2:
            title=selector.xpath('//div[@id="content"]/h1/text()').extract()
            item['title']=title
            yield item
            Comments = selector.xpath('//li[@class="comment-item"]')
            for eachComment in Comments:
              usename = eachComment.xpath('div[@class="comment"]/h3/span[@class="comment-info"]/a/text()').extract()

              comment = eachComment.xpath('div[@class="comment"]/p[@class="comment-content"]/text()').extract()
              user_url=eachComment.xpath('div[@class="comment"]/h3/span[@class="comment-info"]/a/@href').extract()
              #//*[@id="comments"]/div[1]/div[2]/h3/span[2]/a
              votes=eachComment.xpath('div[@class="comment"]/h3/span[@class="comment-vote"]/span[@class="vote-count"]/text()').extract()
              time = eachComment.xpath('div[@class="comment"]/h3/span[@class="comment-info"]/span/text()').extract()
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
            #//*[@id="content"]/div/div[1]/div/div[3]/ul/ul/li[3]/a
            # nextLink = shop_comment_2.xpath('//*[@id="content"]/div/div[1]/div/div[3]/ul/ul/li[3]/a').extract()
            #
            # if nextLink:
            #      nextLink = nextLink[0]
            #      print nextLink
            #      print urls
            #      yield Request(urls + nextLink,callback=self.parse)
            #
