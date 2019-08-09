# -*- coding: utf-8 -*-
# website: http://30daydo.com
# @Time : 2019/4/18 23:11
# @File : bbs.py
import datetime
import re
from bbssmth.items import BbssmthItem
from scrapy import Request, Spider, FormRequest


class BbsSMTH(Spider):
    name = 'bbssm'
    url = 'http://www.newsmth.net/nForum/board/{}?ajax'
    board='Career_Upgrade'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en,en-US;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        # 'Content-Length': '45'
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'NFORUM=rmg4r41gj6rraaulq8ipc75oq5; main[XWJOKE]=hoho; main[UTMPUSERID]=guest; main[UTMPNUM]=47430; Hm_lvt_bbac0322e6ee13093f98d5c4b5a10912=1544933168,1544933353,1544954402; Hm_lpvt_bbac0322e6ee13093f98d5c4b5a10912=1544954402; main[UTMPKEY]=37814499',
        'Host': 'www.newsmth.net',
        'Origin': 'http://www.newsmth.net',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://www.newsmth.net/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    formdata = {
        'id': 'q836754578',
        'passwd': 'wangqiang654321',
        'mode': '0',
        'CookieDate': '0',
    }
    log_url = 'http://www.newsmth.net/nForum/user/ajax_login.json'
    headers1 = {
        'Host': 'www.newsmth.net',
        'Upgrade-Insecure-Requests': '1',
        'DNT': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://www.newsmth.net/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cookie': 'Hm_lvt_bbac0322e6ee13093f98d5c4b5a10912=1544963456; Hm_lpvt_bbac0322e6ee13093f98d5c4b5a10912=1544964807; main[UTMPUSERID]=q836754578; main[UTMPKEY]=49445247; main[UTMPNUM]=9696',
        'If-Modified-Since': 'Sun, 16 Dec 2018 12:36:33 GMT'
    }
    headers2 = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en,en-US;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Cookie': ' NFORUM=rmg4r41gj6rraaulq8ipc75oq5; main[XWJOKE]=hoho; Hm_lvt_bbac0322e6ee13093f98d5c4b5a10912=1544933168,1544933353,1544954402; main[UTMPUSERID]=q836754578; main[UTMPKEY]=24609885; main[UTMPNUM]=12725; Hm_lpvt_bbac0322e6ee13093f98d5c4b5a10912=1545013513',
        'Host': 'www.newsmth.net',
        'If-Modified-Since': 'Mon, 17 Dec 2018 02:24:03 GMT',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://www.newsmth.net/nForum/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    def start_requests(self):
        yield FormRequest(self.log_url, formdata=self.formdata, headers=self.headers, callback=self.update_cookie)

    # def start_requests(self):
    #     url='http://www.newsmth.net/'
    #     yield Request(url=url,callback=self.guest_visit,meta={'cookiejar':1})

    def guest_visit(self, response):
        url = 'http://www.newsmth.net/nForum/#!mainpage'
        yield Request(url=url, callback=self.update_cookie,
                      # meta={'cookiejar': response.meta['cookiejar']}
                      )

    def update_cookie(self, response):
        board = self.board  # 量化交易
        yield Request(
            url=self.url.format(board),
            meta={'board': board,
                  # 'cookiejar':response.meta['cookiejar']
                  },
        )

    def parse(self, response):
        # print(response.text)

        if '过于频繁' in response.text:
            print('被封了')
            return

        board = response.meta['board']
        try:
            counts = int(re.search('主题数:<i>(\d+)</i>', response.text).group(1))
        except Exception as e:
            return
        pages = counts // 30 + 1
        print(pages)
        for i in range(1, pages + 1):
            yield Request(
                url=self.url.format(board) + '&p={}'.format(i),
                callback=self.parse_item,
                meta={'board': board,
                      # 'cookiejar': response.meta['cookiejar']
                      }
            )

    def parse_item(self, response):
        root = response.xpath('//table[@class="board-list tiz"]//tr')
        print(response.text)
        for item in root[1:]:
            url = item.xpath('.//td[@class="title_8"]/a/@href').extract_first()
            if url is None:
                continue
            full_url = 'http://www.newsmth.net' + url
            create_time = item.xpath('.//td[@class="title_10"]/text()').extract_first()
            title = item.xpath('.//td[@class="title_9"]/a/text()').extract_first()
            print(full_url)

            yield Request(url=full_url, callback=self.parse_content,
                          meta={'create_time': create_time, 'board': response.meta['board'],
                                'title': title,
                                # 'cookiejar': response.meta['cookiejar']
                                }
                          )

    def parse_content(self, response):
        title = response.meta['title']
        # title = response.xpath('//title/text()').extract_first()
        root = response.xpath('//table[@class="article"]')
        # root[0]
        create_time = response.meta['create_time']
        author_list = []
        content_list = []
        for node in root:
            author = self.pretty(node.xpath('.//td[@class="a-left"]/span/a/text()').extract_first())
            content = self.pretty(node.xpath('.//td[@class="a-content"]')[0].xpath('string(.)').extract()[0])
            author_list.append(author)
            content_list.append(content)

        content = content_list[0]
        author = author_list[0]
        category = response.meta['board']
        crawltime = datetime.datetime.now()
        reply = []
        url = response.url
        for index, item in enumerate(content_list):
            if index == 0:
                continue

            reply.append({'author': author_list[index], 'reply': content_list[index]})

        bbsItem = BbssmthItem()
        for field in bbsItem.fields:
            try:
                bbsItem[field] = eval(field)
            except Exception as e:
                pass
        print(bbsItem)
        yield bbsItem

    def pretty(self, content):

        if content:
            content = content.strip()
            content = content.replace('\xa0\xa0', '')

        return content
