#-*-coding=utf-8-*-
import requests
from blacklist import phone
import random,time
def send(phone):
    session=requests.Session()
    session.get('https://login.kongfz.com')
    time.sleep(random.random()*5)
    # phone=
    url="https://login.kongfz.com/Pc/Ajax/sendMobileCheckCode"
    headers={'Origin': 'https://login.kongfz.com', 'Connection': 'keep-alive', 'Host': 'login.kongfz.com', 'Accept-Encoding': 'gzip,deflate,br', 'Cookie': 'acw_tc=7b39758515534429799065498e9570998d15404331cded92330568e8bd576d;PHPSESSID=9a240b541314679ebd9441210302876d0cbbcf9a;kfz_uuid=b52e16e4-98e6-44bd-aeee-76ef125a5cf4;kfz_trace=b52e16e4-98e6-44bd-aeee-76ef125a5cf4|0|28a65f13026de686|-', 'User-Agent': 'Mozilla/5.0(Linux;Android6.0;Nexus5Build/MRA58N)AppleWebKit/537.36(KHTML,likeGecko)Chrome/69.0.3497.81MobileSafari/537.36', 'Accept-Language': 'en-US,en;q=0.9', 'Pragma': 'no-cache', 'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json,text/javascript,*/*;q=0.01', 'Referer': 'https://login.kongfz.com/register/index.html?returnUrl=http%3A%2F%2Fuser.kongfz.com%2F&ph=13713465184', 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8', 'Cache-Control': 'no-cache'}

    # headers=getheader()
    # print(headers)
    # del headers['Cookie']
    data={'mobile':phone,'bizType':2}
    # headers1={}
    r=session.post(url=url,data=data,headers=headers)
    print(r.status_code)
    print(r.text)
    try:
        if r.json().get('status')=='true':
            print("work")
            return True
        if r.json().get('errInfo'):
            print(r.json().get('errInfo'))
            print("not work")
            time.sleep(random.random()*60*5)
            return False
    except Exception as e:
        print(e)
        return False

def main():
    while 1:
        send(phone)
        time.sleep(60)
if __name__ == '__main__':
    main()