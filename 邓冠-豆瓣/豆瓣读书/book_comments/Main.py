from scrapy import cmdline
cmdline.execute("scrapy crawl book_comments".split())
# cmdline.execute("scrapy crawl comment -o comment.csv".split())