# coding: utf-8
import scrapy
# from scrapy import Request
from scrapy.spiders import Spider
from fraud.items import FraudItem
from fraud.model.db_config import RedisPool
import json
import re
import logging

class FraudInfoSpider(Spider):
    name = 'fraud_info'
    logging.basicConfig(
        filename='log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )

    def __init__(self):
        self.headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip,deflate,br',
                        'Accept-Language': 'zh,en;q=0.9,en-US;q=0.8', 'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'Cookie': 'BAIDUID=C459F789B96EDC64D968698B40CF0EB2:FG=1; BIDUPSID=C459F789B96EDC64D968698B40CF0EB2; PSTM=1529375614; H_PS_PSSID=1435_21098_18560_26430_20929; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; PSINO=3',
                        'Host': 'sp0.baidu.com', 'Pragma': 'no-cache',
                        'Referer': 'ttps://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd=%E5%A4%B1%E4%BF%A1%E4%BA%BA&rsv_pq=d59937df00036f4c&rsv_t=4819Blu7uUUxtecozaNKH4aarApHleQjx4Q7ab%2FgApuJ5IG2WDeF3uuZxJo&rqlang=cn&rsv_enter=1&rsv_sug3=10&rsv_sug1=13&rsv_sug7=101&rsv_sug2=0&inputT=2166&rsv_sug4=2166&rsv_sug=1',
                        'User-Agent': 'Mozilla/5.0(WindowsNT6.1;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/67.0.3396.87Safari/537.36'}

    def start_requests(self):
        pool = RedisPool(client_db=1)
        r = pool.redis_pool()
        last_name_lst = r.keys()
        for item in last_name_lst:
            print(item)
            url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=失信被执行人&cardNum=&iname={0}&areaName=&pn=0'.format(
                item)
            print(url)
            yield scrapy.Request(url=url, headers=self.headers)

    def parse(self, response):

        page_num = re.search(r'pn=(\d+)', response.url).group(1)
        json_data = json.loads(response.body_as_unicode())
        if json_data['data']:
            disp_num = json_data['data'][0]['dispNum']
            if int(page_num) > int(disp_num)/5:
                print('该姓氏已经全部爬完')
                return
            else:

                fraud_info_list = json_data['data'][0]['result']
                print('len of fraud{}'.format(len(fraud_info_list)))

                for fraud_info in fraud_info_list:
                    print(fraud_info)
                    try:
                        # print()
                    # if fraud_info['sexy']:
                        item = FraudItem()
                        # print(fraud_info['iname'])
                        item['executed_name'] = fraud_info['iname']
                        item['gender'] = fraud_info['sexy']
                        item['age'] = fraud_info['age']
                        item['identity_number'] = fraud_info['cardNum']
                        item['court'] = fraud_info['courtName']
                        item['province'] = fraud_info['areaName']
                        item['case_number'] = fraud_info['caseCode']
                        item['performance'] = fraud_info['performance']
                        item['disrupt_type_name'] = fraud_info['disruptTypeName']
                        item['duty'] = fraud_info['duty']
                        item['release_time'] = fraud_info['publishDate']

                        yield item
                    except Exception as e:
                        print('Error Here')
                        print(e)
                        continue

                page_num = 'pn=' + str(int(page_num) + 10)
                next_url = re.sub(r'pn=\d+', page_num, response.url)
                print('next url : {}'.format(next_url))
                yield scrapy.Request(url=next_url, headers=self.headers)


class BaiJiaXingSpider(Spider):
    name = 'baijiaxing'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        url = 'http://xing.911cha.com/'
        yield scrapy.Request(url=url, headers=self.headers)

    def parse(self, response):
        last_names = response.xpath('//p[@id="baijiaxing"]/a')
        print(last_names)
        for sel in last_names:
            last_name = sel.xpath('text()').extract()[0]
            print(last_name)
            pool = RedisPool(client_db=1)
            r = pool.redis_pool()
            r.set(last_name, 1)
