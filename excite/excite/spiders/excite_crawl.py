# import scrapy
# import json
# import w3lib.html

# class QiitaCrawlSpider(scrapy.Spider):
#     name = "excite_crawl"
#     # allowed_domains = [".+.exblog"]
#     # start_urls = ["https://www.exblog.jp/"]
#     start_urls = ["https://zeiss8514.exblog.jp/27754533/"]

#     # sitemap_urls = ["http://www.exblog.jp/sitemap.xml"]
        
#     # print('sitemap_urls', sitemap_urls)
#     sitemap_rules = [
#         # 正規表現 '/items/' にマッチするページをparseメソッドでパースする
#         (r'exblog', 'parse'),
#     ]


#     def parse(self, response):
#         # ワイルドカードとか使うと良さそう
#         flag = 0
#         for txt in response.url.split('/'):
#             if txt.isdigit():
#                 flag = 1
#         if flag == 0:
#             return
#         texts = response.xpath('//*[@id="main-contents"]//*')
#         # texts = response.xpath('//*[@id="main-contents"]/div/div/div/div/div/div')
#         # texts2 = response.xpath('//*[@id="main-contents"]/div/div/div/div/div/center')
#         # texts3 = response.xpath('//*[@id="main-contents"]/div/div/div/div/div/text()')
#         # texts4 = response.xpath('//*[@id="MainConts"]/div/div/div/center')
#         # texts5 = response.xpath('//*[@id="MainConts"]/div/div/div/div')
#         # texts6 = response.xpath('//*[@id="LEFT"]/div/div/div')
#         # tects7 = response.xpath('//*[@id="main-contents"]/div/div/div/div/div')
#         # texts8 = response.xpath('//*[@id="main-contents"]/div/div/div/div/center')
#         # texts9 = response.xpath('//*[@id="postSection"]/text()')
#         # texts += texts2 + texts3 + texts4 + texts5 + texts6 + tects7 + texts8 + texts9
#         for text in texts:
#             text = text.extract()
#             text = text.replace('\n','')
#             text = text.replace('\t','')
#             text = text.replace('\r','')
#             text = text.replace(' ','')
#             items = {}
#             items['url'] = response.url
#             items['text'] = w3lib.html.remove_tags(text)
#             if items['text'] == '':
#                 continue
#             if items['text'][:2] == 'タグ':
#                 break
#             with open('output_debug2.jsonl', 'a', encoding='utf-8') as writer:
#                 json.dump(items, writer, ensure_ascii=False)
#                 writer.write('\n')

import scrapy
from datetime import datetime

from scrapy.spiders.sitemap import SitemapSpider
import json
import w3lib.html
import re

# conslut with https://orangain.hatenablog.com/entry/scrapy
class QiitaCrawlSpider(SitemapSpider):
    name = "excite_crawl"
    # allowed_domains = [".+.exblog"]
    start_urls = ["https://www.exblog.jp/"]

    sitemap_urls = ["http://www.exblog.jp/sitemap.xml"]
        
    print('sitemap_urls', sitemap_urls)
    sitemap_rules = [
        # 正規表現 '/items/' にマッチするページをparseメソッドでパースする
        (r'exblog', 'parse'),
    ]


    def parse(self, response):
        flag = 0
        for txt in response.url.split('/'):
            if txt.isdigit():
                flag = 1
        if flag != 0:
            texts = response.xpath('//*[@id="main-contents"]//*')
            # texts = response.xpath('//*[@id="main-contents"]/div/div/div/div/div/div')
            # texts2 = response.xpath('//*[@id="main-contents"]/div/div/div/div/div/center')
            # texts3 = response.xpath('//*[@id="main-contents"]/div/div/div/div/div/text()')
            # texts4 = response.xpath('//*[@id="MainConts"]/div/div/div/center')
            # texts5 = response.xpath('//*[@id="MainConts"]/div/div/div/div')
            # texts6 = response.xpath('//*[@id="LEFT"]/div/div/div')
            # tects7 = response.xpath('//*[@id="main-contents"]/div/div/div/div/div')
            # texts8 = response.xpath('//*[@id="main-contents"]/div/div/div/div/center')
            # texts9 = response.xpath('//*[@id="postSection"]/text()')
            # texts += texts2 + texts3 + texts4 + texts5 + texts6 + tects7 + texts8 + texts9
            for text in texts:
                text = text.extract()
                text = text.replace('\n','')
                text = text.replace('\t','')
                text = text.replace('\r','')
                text = text.replace(' ','')
                items = {}
                items['url'] = response.url
                items['text'] = w3lib.html.remove_tags(text)
                if items['text'] == '':
                    continue
                if items['text'][:2] == 'タグ':
                    break
                with open('output_debug3.jsonl', 'a', encoding='utf-8') as writer:
                    json.dump(items, writer, ensure_ascii=False)
                    writer.write('\n')

        next_pages = response.xpath('//*[contains(@href,"exblog")]/@href')
        for next_page in next_pages:
            if not 'https://ssl2.excite.co.jp/' in next_page.__str__() and '/push/settings/' not in next_page.__str__() and '.jpg' not in next_page.__str__():
                yield response.follow(url=next_page, callback=self.parse)