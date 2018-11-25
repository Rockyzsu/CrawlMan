import requests
import hashlib
import config

username = ''
password=''
s = bytes(password, encoding='utf8')
m = hashlib.md5()
m.update(s)
first_md5 = m.hexdigest()
headers = {'Referer': 'https://www.szlib.org.cn/MyLibrary/Reader-Access.jsp?infomistake=0&eventsite=WWW-044005',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
           'X-Requested-With': 'XMLHttpRequest'}

url = 'https://www.szlib.org.cn/MyLibrary/readerLoginM.jsp'
data = {'rand': '',
        'username': username,
        'password': first_md5,

        }
print(data)

def login_session():
    session = requests.Session()

    r = session.post(url=url, headers=headers, data=data, timeout=15)
    print(r.text)
    if '<message>OK</message>' in r.text:
        print('Crash !!!')
        print(username)
        print(password)

    return session
