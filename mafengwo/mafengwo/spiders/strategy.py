import json
from lxml import etree

import scrapy
from scrapy import Request, Selector

from mafengwo.items import MafengwoItem


class MaFengWoSpider(scrapy.spiders.Spider):

    name = 'mafengwo'
    domain_url = 'http://www.mafengwo.cn'
    start_urls = {'http://www.mafengwo.cn/mdd/',}

    # def start_request(self):
    #     yield Request(url=self.start_mafengwo_url)

    def parse(self, response):
        sel = Selector(response)
        area_info = sel.xpath('//div[@class="hot-list clearfix"]/div/dl/dd/a')
        for area in area_info:
            if area.xpath('./text()'):
                area_href = area.xpath('./@href').extract()[0]
                area_name = area.xpath('./text()').extract()[0]
                ziyouxing_href = self.split_house_info(area_href)
                yield Request(self.domain_url + '/gonglve/ziyouxing/list/list_page?mddid='+ ziyouxing_href + '&page=1', callback=self.parse_area_info, meta={'area': area_name})

    def parse_area_info(self, response):
        res = json.loads(response.text)
        if res['ret']:
            href = res['html']
            html = etree.HTML(href)
            zyx_info = html.xpath('.//div[@class="item clearfix"]/a')
            for i in zyx_info:
                zyx_href = i.xpath('./@href')[0]
                title = i.xpath('./div[2]/h3/text()')[0]
                yield Request(self.domain_url + zyx_href, callback=self.parse_ziyouxing, meta={'title': title, 'area': response.meta.get('area'), 'href':self.domain_url + zyx_href})

    def parse_ziyouxing(self, response):
        content = response.text
        # sel = Selector(response)
        # content1 = sel.xpath('/html/body/div[2]/div[2]/div[1]').extract()[0]
        # sub_tit = sel.xpath('/html/body/div[2]/div[2]/div[1]/div[1]/div[1]').extract()[0]
        # user_list = sel.xpath('/html/body/div[2]/div[2]/div[1]/div[1]/div[2]').extract()[0]
        # product_box = sel.xpath('//*[class="product_box"]').extract()[0]
        items = MafengwoItem()
        items['area'] = response.meta.get('area')
        items['title'] = response.meta.get('title')
        items['href'] = response.meta.get('href')
        items['content'] = content
        yield items

    def split_house_info(self, info):
        a = [i for i in info.split('/')][-1]
        return a.split('.')[0]



