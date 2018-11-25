# -*-coding=utf-8-*-
import json
import re
import time

import requests
from lxml import etree
import pandas as pd
from collections import OrderedDict
from sqlalchemy import create_engine
from login import login_session

engine = create_engine('mysql+pymysql://{}:{}@localhost:3306/db_rocky?charset=utf8'.format('root', '123456z'))
session = login_session()


def getHistory(start, end):
    global session
    # with open('cookies', 'r') as f:
    #     # js = json.load(f)
    #     js=eval(f.read())
    # # cookie=js.get('Cookie','')
    # headers = js.get('headers', '')
    # url='https://www.szlib.org.cn/MyLibrary/LoanHistory.jsp?v_StartDate=20090123&v_EndDate=20180123&v_ServiceAddr=&CardOrBarcode=cardno&cardno=0440070074317&v_LoanType=E&curpage=2'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip,deflate,br', 'Accept-Language': 'zh,en;q=0.9,en-US;q=0.8',
        'Cache-Control': 'no-cache', 'Connection': 'keep-alive',
        'Host': 'www.szlib.org.cn', 'Pragma': 'no-cache',
        'Referer': 'https://www.szlib.org.cn/MyLibrary/Loan-Status.jsp', 'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0(WindowsNT6.1;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/67.0.3396.99Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    time.sleep(5)
    base = "https://www.szlib.org.cn/MyLibrary/LoanHistory.jsp?v_StartDate={}&v_EndDate={}&v_ServiceAddr=&CardOrBarcode=cardno&cardno=0440070074317&v_LoanType=Ea&curpage={}"
    url = base.format(start, end, 1)
    r = session.get(url=url, headers=headers)

    # df = {'date': date, 'time': borrow_time, 'Book': title, 'optime': optype, 'From Library': cirtype, 'Address': addr,
    #       'Barcode': barcode, 'callno': callno}
    # col_name={'date':}

    total = re.findall(r'<totalno>(\d+)</totalno>', r.text)[0]
    date = []
    borrow_time = []
    optype = []
    cirtype = []
    title = []
    addr = []
    barcode = []
    callno = []

    for page in range(1, (int(total) + 20) // 20 + 1):
        time.sleep(5)
        r = session.get(url=base.format(start, end, page), headers=headers)
        tree = etree.HTML(r.text)
        for item in tree.xpath('//record'):
            if item.xpath('.//title/text()'):
                title.append(item.xpath('.//title/text()')[0])
                date.append(item.xpath('.//date/text()')[0])
                borrow_time.append(item.xpath('.//time/text()')[0])
                optype.append(item.xpath('.//optype/text()')[0])
                cirtype.append(item.xpath('.//cirtype/text()')[0])
                # title.append(item.xpath('.//title/text()')[0])
                addr.append(item.xpath('.//addr/text()')[0])
                barcode.append(item.xpath('.//barcode/text()')[0])
                callno.append(item.xpath('.//callno/text()')[0])

    od = OrderedDict(
        [('Date', date), ('Time', borrow_time), ('Book', title), ('Optime', optype), ('From Library', cirtype),
         ('Address', addr), ('Barcode', barcode), ('Callno', callno)])
    print(od)
    df = pd.DataFrame(od)
    print(df)
    df.to_sql('tb_library', engine)


def main():
    getHistory('20100101', '20181030')


if __name__ == '__main__':
    main()
