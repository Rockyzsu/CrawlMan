# -*-coding=utf-8-*-

# @Time : 2020/3/30 21:50
# @File : switch_ip.py

import os
import time
from config import AD_PASSWORD, AD_USER

g_adsl_account = {"name": "adsl",  # 这个可以随意写 下面user和pwd 账号密码
                  "username": AD_USER,
                  "password": AD_PASSWORD}


class ADSL(object):

    def __init__(self):
        self.name = g_adsl_account["name"]
        self.username = g_adsl_account["username"]
        self.password = g_adsl_account["password"]

    # set_adsl : 修改adsl设置

    def set_adsl(self, account):
        self.name = account["name"]
        self.username = account["username"]
        self.password = account["password"]

        # connect : 宽带拨号

    def connect(self):
        cmd_str = "rasdial %s %s %s" % (self.name, self.username, self.password)
        os.system(cmd_str)
        time.sleep(5)

        # disconnect : 断开宽带连接

    def disconnect(self):
        cmd_str = "rasdial %s /disconnect" % self.name
        os.system(cmd_str)
        time.sleep(5)

        # reconnect : 重新进行拨号

    def reconnect(self):
        print('自动拨号')
        self.disconnect()
        self.connect()


if __name__ == '__main__':
    a = ADSL()
    a.reconnect()
