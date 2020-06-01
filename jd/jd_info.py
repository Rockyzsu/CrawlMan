# -*-coding=utf-8-*-

# @Time : 2020/3/29 21:49
# @File : chrome_jd.py
import datetime
import random
import time
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import config
from scrapy import Selector
import pandas as pd
from config import TIMEOUT,RETRY
from switch_ip import ADSL

current = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
output_filename = 'output-{}.csv'.format(current)


def main():
    adsl = ADSL()
    result=[]
    df_input=pd.read_excel('sku.xlsx')
    sku_list = df_input['sku'].values
    start=0
    length=len(sku_list)

    while 1:

        if start==length:
            break
        print('正在爬取第{}条'.format(start+1))
        sku=sku_list[start]
        options = webdriver.ChromeOptions()
        options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 999999.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36')

        options.add_argument('--headless')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-gpu')

        driver = webdriver.Chrome(executable_path=r'chromedriver.exe',
                                  chrome_options=options)
        wait = WebDriverWait(driver, TIMEOUT)  # 等待加载最长时间

        url='https://item.jd.com/{}.html'.format(sku)
        try:
            driver.get(url)
        except Exception as e:
            print(e)
            start+=1
            continue

        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//a[@id="InitCartUrl"]')))
        except:
            print('访问超时,重试')
            start+=1
            continue

        text=driver.page_source
        resp=Selector(text=text)
        title=resp.xpath('//div[@class="sku-name"]/text()').extract()
        if len(title)>1:
            title=title[1].strip()
        else:
            title=title[0].strip()
        price=resp.xpath('//span[@class="p-price"]/span[2]/text()').extract_first()
        comment=resp.xpath('//div[@id="comment-count"]/a/text()').extract_first()

        try:
            activity_type=resp.xpath('//div[@class="activity-type"]/strong/text()').extract_first()
        except:
            activity_type=None

        area=resp.xpath('//div[@class="ui-area-text"]/text()').extract_first()
        store=resp.xpath('//div[@id="store-prompt"]/strong/text()').extract_first()
        d={}

        d['title']=title
        d['price']=price
        d['comment']=comment
        d['activity_type']=activity_type
        d['area']=area
        d['store']=store
        d['sku']=str(sku)
        d['url']=url

        result.append(d)
        time.sleep(2*random.randint(2,6))
        driver.close()
        start+=1

        adsl.reconnect()

        df=pd.DataFrame(result)
        df.to_csv(output_filename,encoding='gbk',mode='a',header=False)

    print('爬取结束，共爬取了{}条'.format(length))

if __name__=='__main__':
    main()
