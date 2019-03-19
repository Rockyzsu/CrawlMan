# -*-coding=utf-8-*-
__author__ = 'xda'
import requests
#url=http://passport.hupu.com/register
#pic=http://passport.hupu.com/pc/verifyimg?1486702998324
class Bomb():
    def getCode(self):
        url = 'http://passport.hupu.com/pc/verifyimg?1486702998324'
        rsp = requests.get(url)
        print(rsp.status_code)

    def send(self, call_num):
        url = 'http://passport.hupu.com/m/2/sendmobilecode.action'


def main():
    obj = Bomb()
    obj.getCode()