import requests
from blacklist import phone
session = requests.Session()

headers = {
    "Accept": "text/plain, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Length": "128",
    "Content-Type": "application/x-www-form-urlencoded",
    # "Cookie":"NSC_dfdpm-ttm=ffffffffc3a0bbb845525d5f4f58455e445a4a42378b; NEW_VISIT_CECOL=000859110120190324; _ga=GA1.3.1561819432.1553357287; _gid=GA1.3.257200021.1553357287; JSESSIONID=A399AF7F9699C397D58B141EA1468807; _gat=1";
    "Host": "login.ceconline.com",
    "Origin": "https://login.ceconline.com",
    "Pragma": "no-cache",
    "Referer": "https://login.ceconline.com/pcMobileNumberRegister.do",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/69.0.3497.81 Chrome/69.0.3497.81 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}


def CEConline(phone):
    capcha_url = 'https://login.ceconline.com/Captchastr.do?n=0.8852169677673725'
    cap_sess = session.get(capcha_url)
    with open('test.jpg', 'wb') as f:
        f.write(cap_sess.content)
    code = input('请输入验证码')
    url = 'https://login.ceconline.com/thirdPartLogin.do'
    data = {
        'mobileNumber': phone,
        'method': 'getDynamicCode',
        'verifyType': 'MOBILE_NUM_REG',
        'kaptcha': code,
        'captcharType': 'verifyCode',
        'time': '1553403282377'
    }

    resp_sess = session.post(url=url, data=data, headers=headers)
    print(resp_sess.json())

CEConline(phone)