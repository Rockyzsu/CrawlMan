# coding: utf-8
import re

import requests
from lxml import etree
import pandas as pd

class Yinyongbao():
    def __init__(self):
        self.user_agent = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
        self.headers = {"User-Agent": self.user_agent}


    def getData(self):
        base_url='http://sj.qq.com/myapp/category.htm'
        parent_url='http://sj.qq.com/myapp/category.htm?orgame=1'
        s=requests.get(url=parent_url,headers=self.headers)
        print(s.status_code)
        #print(s.text)
        tree=etree.HTML(s.text)
        menu=tree.xpath('//ul[@class="menu-junior"]')[0]
        print(type(menu))

        link= menu.xpath('.//li[@id]/a/@href')
        catelog=[]
        for i in link:
            print(i)
            p=re.compile('categoryId=(-?\d+)')
            #x=base_url+i
            x=p.findall(i)[0]
            #print(x)
            catelog.append(x)
        return catelog

    def testcase(self):
        catelog=self.getData()
        print(catelog)
        for i in catelog:
            print("Catelog : ", i)
            self.each_page(int(i),0)

    #抓取某一个分类的
    def each_page(self,categoryId,pageContext):

        url='http://sj.qq.com/myapp/cate/appList.htm?orgame=1&categoryId=%d&pageSize=20&pageContext=%d' %(categoryId,pageContext)
        para={'orgame':1,'categoryId':categoryId,'pageSize':20,'pageContext':pageContext}
        s=requests.get(url=url,params=para,headers=self.headers)
        js= s.json()
        name=[]
        df=pd.DataFrame(js['obj'])
        print(df)
        for i in js['obj']:
            #需要的数据都在这里面
            x= i['appName']
            print(x,' ---download count: ', i['appDownCount'])

            name.append(x)
        print(len(name))
        try:
            pageContext=int(js['pageContext'])
            self.each_page(categoryId,pageContext)
        except Exception as e:
            return

def main():
    obj=Yinyongbao()
    #obj.getData()
    #obj.each_page('',0)
    obj.testcase()
    '''
    for i in range(0,200,38):
        obj.each_page('',i)
    '''
main()
