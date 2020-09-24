# -*- coding: utf-8 -*-
# website: http://30daydo.com
# @Time : 2020/9/24 12:09
# @File : aio_spider.py
import asyncio
import aiohttp
import aiofiles
import os

import re

from config_file import START_URL, HEADERS, PROXY_STR,SIMPLE_HEADERS
from parsel import Selector


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url,
                               headers=HEADERS,
                               proxy=PROXY_STR,
                               ) as response:
            text = await response.text()
            resp = Selector(text=text)
            nodes = resp.xpath('//div[@class="kl1-2"]')
            for node in nodes:
                next_url = node.xpath('.//div[@class="kl1-2a2"]/a/@href').extract_first()
                title = node.xpath('.//div[@class="kl1-2a2"]/a/@title').extract_first()
                await detail(session=session, next_url=next_url, title=title)
                print('next page')


async def detail(**kwargs):
    session = kwargs['session']
    next_url = kwargs['next_url']
    title = kwargs['title']
    print(next_url)
    print(title)
    async with session.get(
            url=next_url,
            headers=HEADERS,
            proxy=PROXY_STR,
    ) as response:
        text = await response.text()
        resp = Selector(text=text)
        nodes = resp.xpath('//div[@class="kl2-1"]//img/@src').extract()
        nodes = list(set(nodes))
        for img in nodes:
            # print(img)
            await download_img(session=session,url=img,title=title)
            print('next image')

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def download_img(**kwargs):
    url= kwargs['url']
    title= kwargs['title']

    title = title.replace(' ','_')
    title = re.sub('[\/:*?"<>|]', '-', title)
    if not os.path.exists(title):
        os.mkdir(title)

    filename = url.split('/')[-1]
    if not filename.endswith(('png','jpg','jpeg')):
        return
    save_file = os.path.join(title,filename)

    if os.path.exists(save_file):
        return
    print('saving image - ')
    try:
        conn = aiohttp.TCPConnector(ssl=False)  # 防止ssl报错
        async with aiohttp.ClientSession(connector=conn, trust_env=True) as session:
            async with session.get(url=url, headers=SIMPLE_HEADERS, proxy=PROXY_STR) as response:

                if response.status>=200 and response.status<300:
                    f=await aiofiles.open(save_file,'wb')
                    await f.write(await response.read())
                    await f.close()

    except Exception as e:
        print(e)
        print(url)
        return

async def main():
    total_page = 3640
    for page in range(0,total_page,35):

        url = START_URL.format(page=page)
        await fetch(url)
        await asyncio.sleep(0)
        print(f'downing page {page}-')
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
