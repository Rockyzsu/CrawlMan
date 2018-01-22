# -*-coding=utf-8-*-
import json
import re
import requests
from lxml import etree
import pandas as pd
from collections import OrderedDict
from sqlalchemy import create_engine
engine=create_engine('mysql+pymysql://{}:{}@localhost:3306/db_rocky?charset=utf8'.format('',''))
def getHistory(start, end):
    with open('cookies', 'r') as f:
        js = json.load(f)
    # cookie=js.get('Cookie','')
    headers = js.get('headers', '')
    # url='https://www.szlib.org.cn/MyLibrary/LoanHistory.jsp?v_StartDate=20090123&v_EndDate=20180123&v_ServiceAddr=&CardOrBarcode=cardno&cardno=0440070074317&v_LoanType=E&curpage=2'
    base = "https://www.szlib.org.cn/MyLibrary/LoanHistory.jsp?v_StartDate={}&v_EndDate={}&v_ServiceAddr=&CardOrBarcode=cardno&cardno=0440070074317&v_LoanType=Ea&curpage={}"
    url = base.format(start, end, 1)
    r = requests.get(url=url, headers=headers)

    # df = {'date': date, 'time': borrow_time, 'Book': title, 'optime': optype, 'From Library': cirtype, 'Address': addr,
    #       'Barcode': barcode, 'callno': callno}
    # col_name={'date':}


    total=re.findall(r'<totalno>(\d+)</totalno>',r.text)[0]
    date=[]
    borrow_time=[]
    optype=[]
    cirtype=[]
    title=[]
    addr=[]
    barcode=[]
    callno=[]

    for page in range(1,(int(total)+20)/20+1):
        r=requests.get(url=base.format(start,end,page),headers=headers)
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


    od=OrderedDict([('Date',date),('Time',borrow_time),('Book',title),('Optime',optype),('From Library',cirtype),('Address',addr),('Barcode',barcode),('Callno',callno)])
    print od
    df=pd.DataFrame(od)
    df.to_sql('library',engine)

def main():
    getHistory('20100101', '20180122')


if __name__ == '__main__':
    main()
