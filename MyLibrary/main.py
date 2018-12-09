# -*-coding=utf-8-*-
import json
import random
import re
import time

import requests
from lxml import etree
import pandas as pd
from collections import OrderedDict
from sqlalchemy import create_engine
from login import login_session
import config

engine = create_engine('mysql+pymysql://{}:{}@localhost:3306/db_rocky?charset=utf8'.format('root', config.mysql))


def getHistory(session, start, end, cardno):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip,deflate,br', 'Accept-Language': 'zh,en;q=0.9,en-US;q=0.8',
        'Cache-Control': 'no-cache', 'Connection': 'keep-alive',
        'Host': 'www.szlib.org.cn', 'Pragma': 'no-cache',
        'Referer': 'https://www.szlib.org.cn/MyLibrary/Loan-Status.jsp', 'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0(WindowsNT6.1;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/67.0.3396.99Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    # time.sleep(5)
    base = "https://www.szlib.org.cn/MyLibrary/LoanHistory.jsp?v_StartDate={}&v_EndDate={}&v_ServiceAddr=&CardOrBarcode=cardno&cardno={}&v_LoanType=Ea&curpage={}"
    url = base.format(start, end, cardno, 1)
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
        time.sleep(5 + random.random() * 5)
        r = session.get(url=base.format(start, end, cardno, page), headers=headers)
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
    df = pd.DataFrame(od)
    return df


def main():
    start = '20181130'
    end = ''
    s1 = login_session(config.username, config.password)
    df1 = getHistory(s1, start, end, config.cardno1)

    s2 = login_session(config.username2, config.password2)
    df2 = getHistory(s2, start, end, config.cardno2)
    df = pd.concat([df1, df2])
    # df['t']=' '
    df['Datetime'] = df['Date'] + ' ' + df['Time']
    df['Datetime'] = pd.to_datetime(df['Datetime'], format='%Y-%m-%d %H:%M:%S')
    # df=df.sort_values(by='Date')
    # df=df.reset_index(drop=True)
    df = df.set_index('Datetime', drop=True)
    del df['Date']
    del df['Time']
    # del df['t']
    print(df)
    df = df.sort_index(ascending=False)
    df.to_sql('tb_library', engine, if_exists='append')


if __name__ == '__main__':
    main()
