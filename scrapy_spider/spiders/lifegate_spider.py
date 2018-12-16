# -*- coding: utf-8 -*-
import scrapy
import time
import datetime
from selenium import webdriver
from scrapy_spider.items import MusicItem

class LifeGateSpider(scrapy.Spider):
    name = 'quotes_spider'
    #allowed_domains = ['www.lifegate.it']
    start_urls = ['https://www.lifegate.it/radio-sound']

    def __init__(self, *args, **kwargs):
        options = webdriver.ChromeOptions()
        #options.add_argument('headless')
        #options.binary_location = '/home/danilo/workspace/python/libraries/driver/chrome/chromedriver'
        #'/usr/bin/google-chrome-unstable'
        self.driver = webdriver.Chrome(executable_path='/home/danilo/workspace/python/libraries/driver/chrome/chromedriver',chrome_options=options)
        self.driver.implicitly_wait(10)
        super(LifeGateSpider, self).__init__(*args, **kwargs)

    def parse(self, response):

        self.driver.get(response.url)
        sel = scrapy.Selector(text=self.driver.page_source)
        iframes = self.driver.find_elements_by_tag_name('iframe')

        index = 0
        for iframe in sel.css('iframe'):
            if 'share.xdevel.com' in iframe.xpath('@src').extract_first():
                print("#####" + iframe.xpath('@src').extract_first())
                time.sleep(10)
                try:
                    while True:
                        self.driver.switch_to.frame(iframes[index])
                        sel = scrapy.Selector(text=self.driver.page_source)
                        item = self.parse_iframe(sel.css('body')[0])
                        self.driver.switch_to.default_content()
                        time.sleep(3 * 60)
                        yield item
                except KeyboardInterrupt:
                    print('Interrupted!')
            index = index + 1
                #yield item

        #next_page_url = response.xpath("//li[@class='next']//a/@href").extract_first()
        #if next_page_url:
            #absolute_next_page_url = response.urljoin(next_page_url)
            #yield scrapy.Request(absolute_next_page_url)

    def parse_iframe(self, iframe):
        songinfo = iframe.css('#songinfo')
        artist = songinfo.xpath(".//li[@id='artist']/text()").extract_first()
        title = songinfo.xpath(".//li[@id='title']/text()").extract_first()
        album = songinfo.xpath(".//li[@id='album']/text()").extract_first()
        item = MusicItem()
        item["title"] = title
        item["artist"] = artist
        item["last_updated"] = datetime.datetime.utcnow()
        print("####################################################")
        print("Artist: " + artist + " | Title: " + title)
        print("####################################################")
        return item
