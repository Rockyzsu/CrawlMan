# coding: utf-8
import re

import requests
from lxml import etree
headers = {
    'accept': 'text/html',
    'accept-encoding': 'gzip, deflate, sdch',
    'accept-language': 'zh-CN,zh;q=0.8',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'User-Agent': 'UCWEB/2.0 (Linux; U; Adr 2.3; zh-CN; MI-ONEPlus)U2/1.0.0 UCBrowser/8.6.0.199 U2/1.0.0 Mobile',
    'x-requested-with': 'XMLHttpRequest',
    'cookie': 'als=0; isp=true; Hm_lvt_c5899c8768ebee272710c9c5f365a6d8=1502856226; sessid=1551E6AF-1AA9-2526-E4E9-D494551F4A2F; search_words361=%E9%98%B3%E5%85%89%E5%B0%8F%E5%8C%BA; search_words24=%E9%9D%96%E6%B1%9F%E9%9B%85%E5%9B%AD11%E5%8F%B7%E6%A5%BC%7C%E6%9C%88%E6%A1%82%E8%A5%BF%E5%9B%AD; search_words14=%E8%B6%85%E6%98%8E%E5%9B%AD; search_words25=%E6%96%B0%E6%83%A0%E5%AE%B6%E5%9B%AD; browse_comm_ids13=95393; seo_source_type=0; search_words13=%E6%AC%A7%E9%99%86%E7%BB%8F%E5%85%B8%7C%E5%8D%97%E6%96%B9%E6%98%8E%E7%8F%A0%E8%8A%B1%E5%9B%AD%7C%E5%8D%97%E6%96%B9%E6%98%8E%E7%8F%A0%E8%8A%B1%E5%9B%AD%E4%BA%8C%E6%9C%9F1%E6%A0%8B; twe=2; __xsptplus8=8.43.1504789824.1504790391.8%233%7C123.sogou.com%7C%7C%7C%7C%23%23hvhL5eg3_ejnK-ngxJE-qwbIXXbQIk81%23%3B%20aQQ_a; _ga=GA1.2.1188068084.1502419352; _gid=GA1.2.1082371756.1504696715; lps="/cityList/|"; aQQ_ajkguid=B97BFB26-048C-2797-947E-7543B95A2D8A; ctid=13; 58tj_uuid=a4461385-7d0d-4e1a-9e94-85fa7b69f6aa; new_session=0; init_refer=; new_uv=61'
}

start_url = 'https://m.anjuke.com/gu/community/?from=anjuke_home&p=1'
r = requests.get(url=start_url, headers=headers)
if  r.json()['data']:
    print('not empty')
else:
    print('empty')


price_case='https://m.anjuke.com/gz/community/112952/'
content=requests.get(url=price_case,headers=headers).text
tree=etree.HTML(content)
price=tree.xpath('//a[@data-soj="community_topprice"]/div[@class="txt-c"]/p[@class="price"]/text()')[0]
print(price)
name=tree.xpath('//div[@class="comm-tit"]/h1/text()')[0]
print(name)
address=tree.xpath('//div[@class="comm-tit"]/div[@class="comm-ad"]/p/text()')[0]
print(address)
building_type=tree.xpath('//div[@class="header-field"]/span')[0].xpath('./text()')[0]
building_date=tree.xpath('//div[@class="header-field"]/span')[2].xpath('./text()')[0]
print(building_date)
print(building_type)
pattern = 'data-center="(.*?)"'
data = re.findall(pattern, content)
t= data[0].split(',')
print(t[0])
print(t[1])
#longitude = data[0]
#latitude = data[1]