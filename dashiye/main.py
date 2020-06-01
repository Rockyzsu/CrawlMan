# -*-coding=utf-8-*-

# @Time : 2020/4/26 20:20
# @File : main.py

import requests
import numpy as np


code = input('请输入股票代码：')

cookies = {
    'PHPSESSID': 'jqb0q4h60h4bmtj5bkd9bjuv00',
    'Hm_lvt_210e7fd46c913658d1ca5581797c34e3': '1587903421',
    'Hm_lpvt_210e7fd46c913658d1ca5581797c34e3': '1587903461',
}

headers = {
    'Origin': 'http://www.dashiyetouzi.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'http://www.dashiyetouzi.com/tools/compare/historical_valuation.php',
}

data = {
  'report_type': 'totalValue',
  'report_stock_id': code,
  'from_date': '2015-04-26',
  'to_date': '2020-04-26'
}

response = requests.post('http://www.dashiyetouzi.com/tools/compare/historical_valuation_data.php', headers=headers, cookies=cookies, data=data, verify=False)
js=response.json()
data=js.get('list')
all_point=[]
for item in data:
    all_point.append(item[1])


np_data = np.array(all_point)
print(f'中值：{np.median(np_data)}')
print(f'最小值：{np.min(np_data)}')
