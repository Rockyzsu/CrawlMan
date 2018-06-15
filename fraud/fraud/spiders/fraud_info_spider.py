# coding: utf-8
import scrapy
from scrapy import Request
from scrapy.spiders import Spider
from fraud.items import FraudItem
from fraud.model.db_config import RedisPool
import json
import re


class FraudInfoSpider(Spider):
    name = 'fraud_info'
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    # }
    headers = {'Accept-Language': 'zh-CN,zh;q=0.9', 'Accept-Encoding': 'gzip,deflate,br', 'Host': 'sp0.baidu.com',
               'Accept': '*/*',
               'User-Agent': 'Mozilla/5.0(WindowsNT6.1;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/65.0.3325.162Safari/537.36',
               'Connection': 'keep-alive',
               'Cookie': 'BAIDUID=807FDFD8452E0BBE9D4E90BE4ACA3E48:FG=1;BIDUPSID=807FDFD8452E0BBE9D4E90BE4ACA3E48;PSTM=1510554299;MCITY=-340%3A;pgv_pvi=5560071168;H_PS_PSSID=1437_21116_18560_26350_26578_20929;PSINO=6',
               'Pragma': 'no-cache', 'Cache-Control': 'no-cache',
               'Referer': 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd=%E5%A4%B1%E4%BF%A1%E4%BA%BA&rsv_pq=ba070cee00021d68&rsv_t=af202PtBAFQNGpj0I7C5T4usPJQM4XwFNcLDD7LLLYIzLiejH%2Br66BFrgCg&rqlang=cn&rsv_enter=1&rsv_sug3=11&rsv_sug1=11&rsv_sug7=100&rsv_sug2=0&inputT=2625&rsv_sug4=2625'}

    def start_requests(self):
        pool = RedisPool(client_db=1)
        r = pool.redis_pool()
        last_name_lst = r.keys()
        for item in last_name_lst:
            url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=失信被执行人&cardNum=&iname={0}&areaName=&pn=0'.format(item)
            yield scrapy.Request(url=url, headers=self.headers)

    def parse(self, response):
        item = FraudItem()
        page_num = re.search(r'pn=(\d+)', response.url).group(1)
        json_data = json.loads(response.body_as_unicode())
        if json_data['data']:
            disp_num = json_data['data'][0]['dispNum']
            if int(page_num) > int(disp_num):
                print '该姓氏已经全部爬完'
                return
            else:

                fraud_info_list = json_data['data'][0]['result']
                for fraud_info in fraud_info_list:
                    if fraud_info['sexy']:
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

                page_num = 'pn=' + str(int(page_num) + 50)
                next_url = re.sub(r'pn=\d+', page_num, response.url)
                print next_url
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
        print last_names
        for sel in last_names:
            last_name = sel.xpath('text()').extract()[0]
            print last_name
            pool = RedisPool(client_db=1)
            r = pool.redis_pool()
            r.set(last_name, 1)