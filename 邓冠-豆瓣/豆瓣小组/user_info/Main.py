from scrapy import cmdline
cmdline.execute("scrapy crawl user_info".split())
# cmdline.execute("scrapy crawl comment -o comment.csv".split())