# import scrapy
# import json
# import w3lib.html

# class QiitaCrawlSpider(scrapy.Spider):
#     name = "excite_crawl"
#     allowed_domains = ["www.exblog.jp"]
#     start_urls = ["https://yunyuns.exblog.jp/33189638/", "https://www.exblog.jp/"]

#     def parse(self, response):
#         texts = response.xpath('//*[@id="main-contents"]/div/div/div/div/div/div')
#         texts2 = response.xpath('//*[@id="main-contents"]/div/div/div/div/div/center')
#         # texts3 = response.xpath('//*[@id="main-contents"]/div/div/div/div/div/div')
#         # print(texts,texts2,texts3)
#         texts += texts2
#         for text in texts:
#             items = {}
#             items['url'] = response.url
#             items['text'] = w3lib.html.remove_tags(text.extract())
#             with open('output.jsonl', 'a', encoding='utf-8') as writer:
#                 json.dump(items, writer, ensure_ascii=False)
#                 writer.write('\n')

#         next_pages = response.xpath('//*[contains(@href,"qiita.com")]/@href')

#         for next_page in next_pages:
#             yield response.follow(url=next_page, callback=self.parse)

import scrapy
from datetime import datetime

from scrapy.spiders.sitemap import SitemapSpider
import json
import w3lib.html

# conslut with https://orangain.hatenablog.com/entry/scrapy
class QiitaCrawlSpider(SitemapSpider):
    name = "excite_crawl"
    allowed_domains = ["www.exblog.jp"]
    start_urls = ["https://www.exblog.jp/"]

    sitemap_urls = ["http://www.exblog.jp/sitemap.xml"]
        
    print('sitemap_urls', sitemap_urls)
    # sitemap_rules = [
    #     # 正規表現 '/items/' にマッチするページをparseメソッドでパースする
    #     (r'/items/', 'parse'),
    # ]


    def parse(self, response):
        texts = response.xpath('//*[@id="main-contents"]/div/div/div/div/div/div')
        texts2 = response.xpath('//*[@id="main-contents"]/div/div/div/div/div/center')
        # print('texts',texts)
        texts += texts2
        for text in texts:
            items = {}
            items['url'] = response.url
            items['text'] = w3lib.html.remove_tags(text.extract())
            with open('output_from_sitemap.jsonl', 'a', encoding='utf-8') as writer:
                json.dump(items, writer, ensure_ascii=False)
                writer.write('\n')