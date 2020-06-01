# coding: utf-8
import codecs
import json
import re
import requests
import time
from lxml import etree

headers = {
    'Host': 'm.lianjia.com',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Pragma': 'no-cache',
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
    'User-Agent': 'UCWEB/2.0 (Linux; U; Adr 2.3; zh-CN; MI-ONEPlus) U2/1.0.0 UCBrowser/8.6.0.199 U2/1.0.0 Mobile',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie': 'lj-ss=5bd2bc45dbdf0644d704777dc2075366; lianjia_uuid=c6a7836e-cf96-45ae-96e5-6fdb2def9fb7; UM_distinctid=15e17d9bbf960c-08e33a5d4e4891-4d015463-1fa400-15e17d9bbfa300; select_city=440300; select_nation=1; _gat=1; _gat_past=1; _gat_new=1; _gat_global=1; _gat_new_global=1; CNZZDATA1254525948=145009446-1503633660-%7C1503908541; CNZZDATA1253491255=851767322-1503638199-%7C1503907203; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1503638699; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1503909560; _ga=GA1.2.331020171.1503638699; _gid=GA1.2.2040440312.1503909104; lianjia_ssid=9e199cf4-48f2-4fac-ba8b-bf64c69a5901'
}


def getCityLink():
    fp = open('lianjia_city.txt').read()
    tree = etree.HTML(fp)
    op = open('lianjia_city_link.txt', 'w')
    for i in tree.xpath('//li/a/@href'):
        print('\'https://m.lianjia.com' + i + 'xiaoqu\',')
        op.write('https://m.lianjia.com' + i + 'xiaoqu' + '\n')


def getCount(url):
    request_url = url + 'pg1/?_t=1'

    r = requests.get(url=request_url, headers=headers)
    print(r.text)
    xiaoqu_count = re.findall(r'\\"total\\":(\d+)}', r.text)[0]
    print(xiaoqu_count)


# url='https://m.lianjia.com/hz/xiaoqu/pg1/?_t=1'
# getCount(url)

def getAccess():
    # url='https://m.lianjia.com/sz/xiaoqu'
    url = 'https://m.lianjia.com/sz/xiaoqu/pg2/?_t=1'
    s = requests.get(url=url, headers=headers)
    print(s.text)


def show_body():
    # with open('lianjia_body.txt','r') as fp:
    with open('cq_error.txt', 'r') as fp:
        content = json.loads(fp.read())['body']
    # print(content)
    tree = etree.HTML(content)
    nodes = tree.xpath('//li[@class="pictext"]')
    for node in nodes:
        xiaoqu_url = node.xpath('.//a[@class="flexbox post_ulog"]/@href')[0]
        name = node.xpath('.//div[@class="item_list"]/div[@class="item_main"]/text()')[0]
        desc = node.xpath('.//div[@class="item_list"]/div[@class="item_other text_cut"]/text()')[0]
        details = desc.split()
        price = node.xpath('.//div[@class="item_list"]/div[@class="item_minor"]/span/em/text()')[0]
        print(xiaoqu_url)
        print(name)
        print(len(details))
        # print(details)
        for i in details:
            print(i)
            print
            # print(details[0],details[1],details[2])
            # print(price)


def get_city_link():
    headers = {'Host': 'm.lianjia.com',
               'User-Agent': 'UCWEB/2.0 (Linux; U; Adr 2.3; zh-CN; MI-ONEPlus) U2/1.0.0 UCBrowser/8.6.0.199 U2/1.0.0 Mobile'}
    url = 'https://m.lianjia.com/city/'
    r = requests.get(url=url, headers=headers)
    contnet = r.text
    # print(contnet)
    tree = etree.HTML(contnet)
    t1 = tree.xpath('//ul[@class="item_lists"]')[1]
    city_list = []
    for city in t1:
        link = city.xpath('.//a/@href')[0]
        if link == '/sh/':
            continue
        if link == '/su/':
            continue
        if link == '/xsbn/':
            continue

        city_list.append('https://m.lianjia.com' + link)
    return city_list


def getXiaoquCount():
    headers = {
        'Host': 'm.lianjia.com',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
        'User-Agent': 'UCWEB/2.0 (Linux; U; Adr 2.3; zh-CN; MI-ONEPlus) U2/1.0.0 UCBrowser/8.6.0.199 U2/1.0.0 Mobile',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': 'lj-ss=5bd2bc45dbdf0644d704777dc2075366; lianjia_uuid=c6a7836e-cf96-45ae-96e5-6fdb2def9fb7; UM_distinctid=15e17d9bbf960c-08e33a5d4e4891-4d015463-1fa400-15e17d9bbfa300; select_nation=1; gr_user_id=4571568e-96d5-467c-ad95-9dd1f55471e1; ubt_load_interval_b=1503971694981; ubta=3154866423.3241223259.1503971686808.1503971686808.1503971695039.2; ubtc=3154866423.3241223259.1503971695041.0EF45810F9672DC3BD68868B080BCCEE; ubtd=2; __xsptplus696=696.1.1503971687.1503971695.2%234%7C%7C%7C%7C%7C%23%23fcZh1fCVH7j7doKzh4kC96wk_XE7Y965%23; _gat=1; _gat_past=1; _gat_new=1; _gat_global=1; _gat_new_global=1; select_city=510100; gr_session_id_a1a50f141657a94e=1b628432-7a95-4993-91b4-c9d304b67fe6; CNZZDATA1254525948=145009446-1503633660-%7C1503984153; CNZZDATA1253491255=851767322-1503638199-%7C1503987040; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1503638699; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1503987947; _ga=GA1.2.331020171.1503638699; _gid=GA1.2.2040440312.1503909104; lianjia_ssid=343c0faf-c443-4673-b900-5c05298bd28a'
        # 'Proxy-Authorization': self.authHeader
    }

    city_count = {}
    city_link = get_city_link()
    for city in city_link:
        print(city)
        city_code = city.split('/')[3]
        request_url = city + 'xiaoqu/pg1/?_t=1'
        r = requests.get(url=request_url, headers=headers)
        print(r)
        xiaoqu_count = re.findall(r'\\"total\\":(\d+)}', r.text)[0]
        print("xiaoqu count", xiaoqu_count)
        city_count[city_code] = int(xiaoqu_count)
    return city_count


def getSZXiaoqu():
    headers = {
        'Host': 'm.lianjia.com',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
        'User-Agent': 'UCWEB/2.0 (Linux; U; Adr 2.3; zh-CN; MI-ONEPlus) U2/1.0.0 UCBrowser/8.6.0.199 U2/1.0.0 Mobile',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': 'lj-ss=5bd2bc45dbdf0644d704777dc2075366; lianjia_uuid=c6a7836e-cf96-45ae-96e5-6fdb2def9fb7; UM_distinctid=15e17d9bbf960c-08e33a5d4e4891-4d015463-1fa400-15e17d9bbfa300; gr_user_id=4571568e-96d5-467c-ad95-9dd1f55471e1; select_nation=1; lj-api=9111950472618e41591b6800072ddacb; _jzqx=1.1504062784.1504062784.1.jzqsr=sz%2Efang%2Elianjia%2Ecom|jzqct=/.-; _jzqckmp=1; ubt_load_interval_b=1504076659297; ubta=3154866423.3241223259.1503971686808.1504062380059.1504076659413.19; ubtc=3154866423.3241223259.1504076659416.04775B09D4A0751F8665A61B54987A68; ubtd=19; __xsptplus696=696.5.1504076659.1504076659.1%234%7C%7C%7C%7C%7C%23%230CIWTVwbBidFOpEsVtab9KgnY2MeVIYe%23; select_city=440300; _smt_uid=59a62d3f.3df2aef3; _jzqa=1.1378702697002941000.1504062784.1504062784.1504077919.2; _jzqc=1; _jzqb=1.19.10.1504077919.1; _gat=1; _gat_past=1; _gat_new=1; _gat_global=1; _gat_new_global=1; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1503638699; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1504080215; _ga=GA1.2.331020171.1503638699; _gid=GA1.2.2040440312.1503909104; CNZZDATA1254525948=145009446-1503633660-%7C1504076453; CNZZDATA1253491255=851767322-1503638199-%7C1504076896; sample_traffic_test=guide_card; lianjia_ssid=e2c7fbe0-e781-46da-8a9b-29633c6549b5'
    }
    for i in range(300, 400):
        access_url = 'https://m.lianjia.com/sz/xiaoqu/pg%d/?_t=1' % i
        print(access_url)
        r = requests.get(url=access_url, headers=headers)
        print(r.status_code)
        parse_body(r.text)


def parse_body(data):
    fp = codecs.open('lianjia_data.txt', 'a', encoding='utf-8')
    price_month = '2017-07'
    crawl_date = '2017-08-30'
    js = json.loads(data)
    arg = json.loads(js['args'])
    print("No more data: ", arg['no_more_data'])
    body = js['body']
    p = re.compile('"cur_city_name":"(.*?)"')
    city_name = p.findall(js['args'])[0].decode('unicode_escape')
    tree = etree.HTML(body)
    nodes = tree.xpath('//li[@class="pictext"]')
    # log.msg(len(nodes), level=log.INFO)
    print("number: ", len(nodes))
    for node in nodes:
        items = {}
        # xiaoqu_url =node.xpath('.//a[@class="flexbox post_ulog"]/@href')[0]
        # items['xiaoqu_link']=xiaoqu_url
        name = node.xpath('.//div[@class="item_list"]/div[@class="item_main"]/text()')[0]
        items['name'] = name
        desc = node.xpath('.//div[@class="item_list"]/div[@class="item_other text_cut"]/text()')[0]
        items['city_name'] = city_name
        details = desc.split()
        if len(details) == 3:
            # for detail in details:
            items['location'] = details[0]
            items['building_type'] = details[1]
            items['building_date'] = details[2]
        elif len(details) == 2:
            items['location'] = details[0]
            items['building_type'] = "NA"
            items['building_date'] = details[1]
        elif len(details) == 1:
            items['location'] = details[0]
            items['building_type'] = "NA"
            items['building_date'] = 'NA'
        else:
            items['location'] = 'NA'
            items['building_type'] = "NA"
            items['building_date'] = 'NA'
        price_t = node.xpath('.//div[@class="item_list"]/div[@class="item_minor"]/span/em/text()')[0]
        p = re.findall('\d+', price_t)
        if len(p) != 0:
            price = int(price_t)
        else:
            price = '均价未知'
        # items['scrapy_date'] = scrapy_date
        # items['origin']='LJ'
        price_detail = {'price': price, 'origin': 'LJ', 'crawl_date': crawl_date}

        price_list = []
        price_list.append(price_detail)
        price_dict = {price_month: price_list}
        items['price'] = price_dict

        str = json.dumps(items)
        fp.write(str)
        fp.write('\n')

        # print('type of items : ',type(items))
        # log.msg(items, level=log.INFO)
        # yield items


def getSZXiaoqu_WEB():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
        'Cookie': 'lianjia_uuid=c6a7836e-cf96-45ae-96e5-6fdb2def9fb7; UM_distinctid=15e17d9bbf960c-08e33a5d4e4891-4d015463-1fa400-15e17d9bbfa300; gr_user_id=4571568e-96d5-467c-ad95-9dd1f55471e1; select_nation=1; all-lj=6341ae6e32895385b04aae0cf3d794b0; _jzqckmp=1; ubt_load_interval_b=1504076659297; ubta=3154866423.3241223259.1503971686808.1504062380059.1504076659413.19; ubtc=3154866423.3241223259.1504076659416.04775B09D4A0751F8665A61B54987A68; ubtd=19; __xsptplus696=696.5.1504076659.1504076659.1%234%7C%7C%7C%7C%7C%23%230CIWTVwbBidFOpEsVtab9KgnY2MeVIYe%23; select_city=440300; _smt_uid=59a62d3f.3df2aef3; CNZZDATA1255849469=590735468-1504057966-null%7C1504079730; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1503638699; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1504083754; _jzqa=1.1378702697002941000.1504062784.1504077919.1504083754.3; _jzqc=1; _jzqx=1.1504062784.1504083754.2.jzqsr=sz%2Efang%2Elianjia%2Ecom|jzqct=/.jzqsr=sz%2Elianjia%2Ecom|jzqct=/xiaoqu/cro11/; CNZZDATA1254525948=1531358740-1504060252-null%7C1504080168; CNZZDATA1255633284=355134272-1504060008-null%7C1504081609; CNZZDATA1255604082=1601457208-1504060276-null%7C1504081886; _qzja=1.218613373.1504062783783.1504077918805.1504083754402.1504079911341.1504083754402.0.0.0.21.3; _qzjb=1.1504083754402.1.0.0.0; _qzjc=1; _qzjto=21.3.0; _jzqb=1.1.10.1504083754.1; _gat=1; _gat_global=1; _gat_new_global=1; _ga=GA1.2.331020171.1503638699; _gid=GA1.2.2040440312.1503909104; _gat_dianpu_agent=1; lianjia_ssid=e2c7fbe0-e781-46da-8a9b-29633c6549b5'}

    for i in range(1,3):
        #url = 'https://bj.lianjia.com/xiaoqu/pg%dcro21/' % i
        url = 'http://bj.lianjia.com/xiaoqu/d2s11'

        headers['Referer'] = url
        r = requests.get(url=url, headers=headers)
        print(r.status_code)
        parse_bj(r.text)

def parse_bj(content):
    #content = response.body
    tree = etree.HTML(content)
    nodes = tree.xpath('//ul[@class="listContent"]/li')
    for node in nodes:
        name = node.xpath('.//div[@class="title"]/a/text()')[0]
        print('name: ',name)
        try:
            position = node.xpath('.//div[@class="positionInfo"]/a/text()')
            address = position[0] + position[1]
        except:
            address = 'NA'
        print('address: ', address)
        try:
            text_content = node.xpath('.//div[@class="positionInfo"]/text()')
            # print(len(build_date))

            detail = text_content[3].split('/')
            # 除去北京，北京的页面会多一个小区结构
            building_date = detail[-1].strip()
            building_type = detail[1].strip()
            if len(building_type) == 0:
                building_type = 'NA'
            '''
            for k, i in enumerate(detail):
                print(k, i)

            if len(detail) == 4:
                buiding_type = detail[1].strip() + detail[3].strip()
                build_date = detail[3].strip()
            elif len(detail) == 3:
                buiding_type = detail[1].strip()

                build_date = detail[2].strip()
            '''
        except:
            building_date = '未知年建成'
            building_type = 'NA'
        print('building type: ',building_type)
        print('building_date:',building_date)
        price_t = node.xpath('.//div[@class="totalPrice"]/span/text()')[0]

        p = re.findall('\d+', price_t)
        if len(p) != 0:
            price = int(price_t)
        else:
            price = 0
        print('price:',price)

def parse_lianjia_web(data):
    fp = open('web_lianjia.txt', 'a')
    tree = etree.HTML(data)
    nodes = tree.xpath('//ul[@class="house-lst"]/li')
    print( "len : ", len(nodes))
    for node in nodes:
        name = node.xpath('.//div[@class="info-panel"]/h2/a/text()')[0]
        try:
            position = node.xpath('.//div[@class="con"]/a/text()')
            address = position[0] + position[1]
        except:
            address = 'NA'
        print(address)
        try:
            text_content = node.xpath('.//div[@class="con"]/text()')
            '''
            for i in text_content:
                print(i.strip())
            '''
            print(text_content[3].strip())
            price_t = node.xpath('.//div[@class="price"]/span/text()')[0]
            print(price_t.strip())
            '''
            for i in detail:
                print(i.strip())
            '''
            #buiding_type=detail[1].strip()
            #print(buiding_type)
            #build_date= detail[-1].strip()
            '''
            for k, i in enumerate(detail):
                print(k, i)
            '''
            '''
            if len(detail)==4:
                buiding_type=detail[1].strip()+detail[3].strip()
                build_date=detail[3].strip()
            elif len(detail)==3:
                buiding_type=detail[1].strip()
                build_date=detail[2].strip()
            '''
        except:
            build_date='NA'
            buiding_type='NA'
        #detail=build_date[3].split('/')
        #print(len(detail))

        #items['name'] = name
        #print(name)
        #print(build_date)
        #print(buiding_type)
        #str1 = json.dumps(items)
        #fp.write(str1)
        #fp.write('\n')


def get_lianjia_m():
    headers = {'X-Requested-With': 'XMLHttpRequest',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
               'Cookie': 'lj-ss=5bd2bc45dbdf0644d704777dc2075366; lianjia_uuid=c6a7836e-cf96-45ae-96e5-6fdb2def9fb7; UM_distinctid=15e17d9bbf960c-08e33a5d4e4891-4d015463-1fa400-15e17d9bbfa300; gr_user_id=4571568e-96d5-467c-ad95-9dd1f55471e1; lj-api=9111950472618e41591b6800072ddacb; _jzqckmp=1; ubt_load_interval_b=1504076659297; ubta=3154866423.3241223259.1503971686808.1504062380059.1504076659413.19; ubtc=3154866423.3241223259.1504076659416.04775B09D4A0751F8665A61B54987A68; ubtd=19; __xsptplus696=696.5.1504076659.1504076659.1%234%7C%7C%7C%7C%7C%23%230CIWTVwbBidFOpEsVtab9KgnY2MeVIYe%23; select_nation=1; _jzqx=1.1504062784.1504090314.3.jzqsr=sz%2Efang%2Elianjia%2Ecom|jzqct=/.jzqsr=you%2Elianjia%2Ecom|jzqct=/hk; _smt_uid=59a62d3f.3df2aef3; _jzqa=1.1378702697002941000.1504062784.1504083754.1504090314.4; _jzqc=1; select_city=440300; sample_traffic_test=guide_card; CNZZDATA1254525948=145009446-1503633660-%7C1504146722; CNZZDATA1253491255=851767322-1503638199-%7C1504145699; _ga=GA1.2.331020171.1503638699; _gid=GA1.2.2040440312.1503909104; _gat=1; _gat_past=1; _gat_new=1; _gat_global=1; _gat_new_global=1; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1503638699; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1504147685; lianjia_ssid=d67c99a2-0840-71b3-baf9-e25816c0ed4b',
               'Host': 'm.lianjia.com',
               'Accept': 'application/json'
               }

    for i in range(100, 170):
        base_url = 'https://m.lianjia.com/sz/xiaoqu/cro21pg%d/' % i
        url = base_url + '?_t=1'
        headers['Referer'] = base_url
        r = requests.get(url=url, headers=headers)
        print(r.status_code)
        # print(r.text)
        parse_mobile_lj(r.text)


def parse_mobile_lj(data):
    fp = codecs.open('lianjia_data_2.txt', 'a', encoding='utf-8')
    price_month = '2017-07'
    crawl_date = '2017-08-30'
    js = json.loads(data)
    arg = json.loads(js['args'])
    print("No more data: ", arg['no_more_data'])
    body = js['body']
    # print(body)
    # time.sleep(2)
    tree = etree.HTML(body)

    nodes = tree.xpath('//li[@class="pictext"]')
    print("number: ", len(nodes))
    for node in nodes:
        items = {}
        # xiaoqu_url =node.xpath('.//a[@class="flexbox post_ulog"]/@href')[0]
        # items['xiaoqu_link']=xiaoqu_url
        name = node.xpath('.//div[@class="item_list"]/div[@class="item_main"]/text()')[0]
        items['name'] = name
        str = json.dumps(items)
        fp.write(str)
        fp.write('\n')


# getAccess()
# show_body()
# getXiaoquCount()
# getSZXiaoqu()
# getSZXiaoqu_WEB()

def mobile_case():
    headersx = {
        'Page-Schema': 'community%2Flist',
        'Referer': 'homepage%3Fcity_id%3D440300',
        'Cookie': 'lianjia_udid=990006203070023;lianjia_ssid=44d3bd0f-46b6-4d1f-814f-0d5551eb2382;lianjia_uuid=cf655e48-98ab-4269-bb23-a045b63054af',
        'User-Agent': 'HomeLink7.12.1;SMARTISAN SM801; Android 5.1.1',
        'Lianjia-Channel': 'Android_chuizi',
        'Lianjia-Device-Id': '990006203070023',
        'Lianjia-Version': '7.12.1',
        'Authorization': 'MjAxNzAzMjRfYW5kcm9pZDo1YTA1MzdlNDQ4NmYyZjA0Zjc5YTdhNjI5ZmQ1NzhkYmEzNTdjNWVk',
        'Lianjia-Im-Version': '2.2.0',
        'Host': 'app.api.lianjia.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'
    }
    headers2 = {
        'Page-Schema': 'community%2Flist',
        'Referer': 'homepage',
        'Cookie': 'lianjia_udid=990006203070023;lianjia_token=2.0069c1bfe11047ba4b786c96d04d08aa3f;lianjia_ssid=b9763c9b-1f7e-47fd-9c29-5d1332d84095;lianjia_uuid=cf655e48-98ab-4269-bb23-a045b63054af',
        'Lianjia-Access-Token': '2.0069c1bfe11047ba4b786c96d04d08aa3f',
        'User-Agent': 'HomeLink7.12.1;SMARTISAN SM801; Android 5.1.1',
        'Lianjia-Channel': 'Android_chuizi',
        'Lianjia-Device-Id': '990006203070023',
        'Lianjia-Version': '7.12.1',
        'Authorization': '',
        'Lianjia-Im-Version': '2.2.0',
        'Host': 'app.api.lianjia.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'
    }
    x='MjAxNzAzMjRfYW5kcm9pZDo5ZDY5YjU0M2ZkMzQ5MTczMjJiZDIyN2VkOTdmOWNlYmRjYzMxYWFj'
    print(len(x))
    print(headers2)
    t = int(time.time())
    base_auth='MjAxNzAzMjRfYW5kcm9pZD'
    print(len(base_auth))
    urlx = 'https://app.api.lianjia.com/house/community/search?limit_offset=80&city_id=440300&limit_count=20&request_ts=%s' % t
    print(urlx)
    r = requests.get(url=urlx, headers=headers2)
    js = r.json()
    for k, v in js.items():
        print(k, v)

def getXiaoquDetail():
    url='https://m.lianjia.com/sz/xiaoqu/2411049901872/'
    header_xiaoqu = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                     'Accept-Encoding': 'gzip, deflate, sdch',
                     'Accept-Language': 'zh-CN,zh;q=0.8',
                     'Cache-Control': 'no-cache',
                     'Connection': 'keep-alive',
                     'Cookie': 'lianjia_uuid=c6a7836e-cf96-45ae-96e5-6fdb2def9fb7; UM_distinctid=15e17d9bbf960c-08e33a5d4e4891-4d015463-1fa400-15e17d9bbfa300; gr_user_id=4571568e-96d5-467c-ad95-9dd1f55471e1; cityCode=sh; lj-ss=1e5c8b6bb356c2aabadd162c97341948; lj-api=bdc2423978f089fb6b74ab39d5dac617; _jzqx=1.1504062784.1504852403.8.jzqsr=sz%2Efang%2Elianjia%2Ecom|jzqct=/.jzqsr=sz%2Elianjia%2Ecom|jzqct=/xiaoqu/; ubt_load_interval_b=1504876703908; ubtd=24; __xsptplus696=696.17.1504876704.1504876704.1%234%7C%7C%7C%7C%7C%23%23cg7Y55E7DbBs-leDZV_ej_nDvMHBKzZu%23; ubta=3154866423.3241223259.1503971686808.1504876703921.1504876712806.103; ubtc=3154866423.3241223259.1504876712808.13E3964C794E1E867DC6AA2BF1D1B81D; select_city=440300; select_nation=1; _jzqy=1.1504975260.1504975260.1.jzqsr=baidu.-; _jzqckmp=1; _smt_uid=59a62d3f.3df2aef3; _jzqa=1.1378702697002941000.1504062784.1504852403.1504975260.21; _jzqc=1; _ga=GA1.2.331020171.1503638699; _gid=GA1.2.882389161.1505006605; CNZZDATA1253491255=1590115228-1504765831-%7C1505006839; CNZZDATA1254525948=23895973-1504766359-%7C1505009618; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1503638699,1504258015,1504675657,1504975259; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1505009847; lianjia_ssid=2bafd2a3-3230-e197-e2cc-a74f98991c4c',
                     'Host': 'm.lianjia.com',
                     'Pragma': 'no-cache',
                     'Upgrade-Insecure-Requests': '1',
                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'}

    r=requests.get(url=url,headers=header_xiaoqu)
    tree=etree.HTML(r.text,parser=etree.HTMLParser(encoding='utf-8'))
    print(r.text)
    #x=tree.xpath('//meta[@class="location"]/@content')[0]
    #print(x)
    name = tree.xpath('//div[@class="xiaoqu_head_title"]/h1/text()')[0]
    print(name)
    # title=tree2.title
    #self.logger.info('name %s' % name)

    # head_tree=etree.HTML(head)

    #desc = tree.xpath('//meta[@class="location"]/@content')[0]
    #city_name = re.findall('city=(.*?);', desc)[0]
    #cooridinate = re.findall('coord=(.*?)')[0]
    #longitude = cooridinate.split(',')[0]
    #latitude = cooridinate.split(',')[1]
    #address = tree.xpath('//p[@class="xiaoqu_head_address"]/text()')[0]
    #print(address)
    #details = tree.xpath('//div[@class="mod_box jichuxinxi"]')
    #print(details)
    '''
    building_date = details.xpath('.//div[@class="value"]/text()')[0].strip()
    print(building_date)
    building_type = details.xpath('.//div[@class="value"]/text()')[0].strip()
    print(building_type)
    '''
    #price = tree.xpath('//div=[@class="mod_box zoushi"]/div[@class="box_col"]/h4/text()')[0]

    #print(latitude)
    #print(longitude)
    #print(price)
    #print(address)
    #print(building_type)
    #print(building_date)
    #print(city_name)
    #print(name)
    src_link=tree.xpath('//div[@class="mod_box loudong"]/div/a/img/@src')[0]
    point=re.findall('center=(.*?)&width',src_link)[0]
    print(point)
    longtitue,latitude=point.split(',')
    print(longtitue)
    print(latitude)


    address = tree.xpath('//p[@class="xiaoqu_head_address"]/text()')[0]
    print(address)
    details = tree.xpath('//div[@class="mod_box jichuxinxi"]/div[@class="mod_cont"]/div[@class="row"]')
    print(len(details))
    building_date = details[0].xpath('.//div[@class="value"]/text()')[0].strip()
    #time.sleep(20)
    #building_date
    print(building_date)
    building_type = details[1].xpath('.//div[@class="value"]/text()')[0].strip()
    print(building_type)
    price = tree.xpath('//div[@class="mod_box zoushi"]//div[@class="gridbox col_3"]//div[@class="box_col"]/h4/text()')[0].strip()
    print(price)
    #print(latitude)
    #print(longitude)
    print(price)
    print(address)
    print(building_type)
    print(building_date)
    desc = tree.xpath('//head/meta[@name="location"]/@content')[0].encode('utf-8').strip()
    print(desc)
    print(type(desc))
    city_name = re.findall('city=(.*?);', desc)[0]
    print(city_name)
    cooridinate = re.findall('coord=(.*)', desc)
    print(len(cooridinate))
    print(cooridinate)
    longitude = cooridinate[0].split(',')[0]
    latitude = cooridinate[0].split(',')[1]

    print(latitude)
    print(longitude)

# get_lianjia_m()
#mobile_case()
#getSZXiaoqu_WEB()
getXiaoquDetail()