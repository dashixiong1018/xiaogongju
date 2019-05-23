# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import requests
from scrapy.selector import Selector
from xiaogongju.items import XiaogongjuItem


class DoubanbookSpider(scrapy.Spider):
    #
    # def get_tag(self):
    #
    #     response = requests.get("https://book.douban.com/tag/?view=type&icn=index-sorttags-all").text
    #     soup = BeautifulSoup(response, 'html5lib')
    #     html = soup.select('#content > div > div.article > div > div > table > tbody > tr > td > a')
    #     start_url = []
    #     for tag in html:
    #         start_url.append('https://book.douban.com/tag/'+tag.text)
    #
    #     return start_url

    name = 'doubanBook'
    allowed_domains = ['book.douban.com']
    # start_urls = get_tag(self=None)
    input_tag = '米兰·昆德拉'
    start_urls = ['https://book.douban.com/tag/'+input_tag]

    def parse(self, response):

        book = Selector(response)

        Info = book.xpath('//div[@class="info"]')

        for info in Info:
            item = XiaogongjuItem()

            item['title'] = ''.join(info.xpath('./h2/a/text()').extract())

            # 图书的价格、出版时间、作者、出版社等信息；如：[日] 东野圭吾 / 陈文娟 / 北京十月文艺出版社 / 2018-1 / 45
            pub = info.xpath('./div[@class="pub"]/text()').extract_first().strip()

            # 判断pub的长度，较精确地提取图书的价格，出版时间，出版社，作者，译者等信息
            if len(pub.split('/')) == 6:
                item['price'] = pub.strip().split('/')[-1]  # 图书价格
                item['pub_time'] = str(pub.split('/')[-4:-1]).replace(',','-').replace('[','').\
                    replace(']','').replace("'",'').replace(' ','')  # 图书出版时间，处理特殊格式的时间：1999/9/9
                item['publish'] = pub.strip().split('/')[-5]  # 图书出版社
                item['author'] = str(pub.strip().split('/')[0:2]).replace(',',' | 译者:').\
                    replace('[','').replace(']','').replace("'",'').replace(' ','')  # 作者、译者

            elif len(pub.split('/')) == 5:
                item['price'] = pub.strip().split('/')[-1]
                item['pub_time'] = pub.strip().split('/')[-2]
                item['publish'] = pub.strip().split('/')[-3]
                item['author'] = str(pub.strip().split('/')[0:2]).replace(',',' | 译者:').\
                    replace('[','').replace(']','').replace("'",'').replace(' ','')

            elif len(pub.split('/')) == 3:
                item['price'] = pub.strip().split('/')[-1]
                item['pub_time'] = pub.strip().split('/')[-2]
                item['publish'] = None
                item['author'] = str(pub.strip().split('/')[0])

            else:
                item['price'] = pub.strip().split('/')[-1]
                item['pub_time'] = pub.strip().split('/')[-2]
                item['publish'] = pub.strip().split('/')[-3]
                item['author'] = pub.strip().split('/')[0]

            item['star'] = ''.join(info.xpath('./div[@class="star clearfix"]/span/text()').extract())

            yield scrapy.Request( url=info.xpath('./h2[@class=""]/a/@href').extract_first(),
                                  callback=self.parse_book_info, meta={'item': item} )

        try:
            nextPage = book.xpath('//div[@id="subject_list"]/div[@class="paginator"]/'
                                  'span[@class="next"]/a/@href').extract_first().strip()
            if nextPage:
                next_url = "https://book.douban.com%s" %nextPage
                yield scrapy.http.Request(next_url, callback=self.parse)

        except:
            pass

    def parse_book_info(self, response):

        item = response.meta['item']

        jianjie = '\n'.join(response.xpath( '//div[@id="link-report"]/*'
                                          '/div[@class="intro"]/*/text()' ).extract())
        if len(jianjie) != 0:
            item['jianjie'] = jianjie
        else:
            item['jianjie'] = '未获取到书籍简介'

        return item
