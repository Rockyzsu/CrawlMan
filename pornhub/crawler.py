#!/usr/bin/env python
import warnings
warnings.filterwarnings("ignore")
import os
import re
import js2py
import requests
from lxml import etree
from clint.textui import progress
import fire
from loguru import logger

file='crawler'
logger.add(
    "logs/%s.log" % file,
    format="{time:MM-DD HH:mm:ss} {level} {message}",
)

headers = {
    'authority': 'cn.pornhub.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'document',
    'accept-language': 'zh,en;q=0.9,en-US;q=0.8,zh-CN;q=0.7',
    'cookie': 'FastPopSessionRequestNumber=11; bs=0hwo170h8b27c5b55tt3ux7b8xkukol0; ss=630427593672619545; bitmovin_analytics_uuid=48eeeda8-bcfe-47f6-84fb-dd172921281a; platform_cookie_reset=pc; fg_9d12f2b2865de2f8c67706feaa332230=56077.100000; fg_7133c455c2e877ecb0adfd7a6ec6d6fe=32682.100000; ats_jp_vkey=ph5f29d906ac970; il=v1yKrZvlyVIqstonKh7Cf8kS4JOEHaOX5I0jleVOp8p6sxNjE0NjQ3MTgwaExRdXp5LXY2QVV4dnhhZmV1NncydDhpam15N1NMamk2dFc5bENEXw..; expiredEnterModalShown=1; platform=pc; fg_a197b3a83beb75c5f0255dc465e9f2de=3629.100000; ua=dcc77110dea38e3cff8b12436648706c; fanClubInfoPop=1; FastPopSessionRequestNumber=9',
}
proxies = {}

s = requests.Session()

def task(url,key):
    resp = s.get(url, headers=headers, proxies=proxies, verify=False)
    html = etree.HTML(resp.content)

    title = "".join(html.xpath("//h1//text()")).strip()
    logger.info(title)

    js_temp = html.xpath("//script/text()")
    for j in js_temp:
        if "flashvars" in j:
            videoUrl = exeJs(j)
            if videoUrl is None:
                continue
            
            download(videoUrl, title, "mp4",key)
            continue

def get_url(url):
    r = s.get(url,headers)
    js= r.json()
    result = list(sorted(js,key=lambda x:x.get('quality'),reverse=True))
    return result[0]['videoUrl']

def exeJs(js):
    flashvars = re.findall("flashvars_\d+", js)[0]
    js = "\n\t".join(js.split("\n\t")[:-5]).strip()

    js = js.replace("// var nextVideoObject = flashvars_['nextVideo'];",'')
    js+=flashvars
    res = js2py.eval_js(js)
    result_list=[]
    
    for video in res['mediaDefinitions']:

        video_url = video.get('videoUrl')
        if 'validfrom' in video_url and 'urlset' not in video_url:
            result_list.append({'quality':video.get('quality'),'videoUrl':video_url})

        elif re.search('ttl=\d+&ri=\d+&rs=\d+',video_url):
            result_list.append({'quality':video.get('quality'),'videoUrl':video_url})

        elif video.get('remote')==True:
            url = get_url(video_url)
            return url

    if len(result_list)==0:
        return None
    try:
        result_list = list(sorted(result_list,key=lambda x:x.get('quality'),reverse=True))
    except Exception as e:
        print(result_list) # 待处理，[480,720]

    return result_list[0]['videoUrl']



def download(url, name, filetype,key):
    logger.info(f"{url} {name} {filetype}")
    name=name.replace('/','').replace('|','')
    filepath = "%s/%s.%s" % (filetype, name, filetype)
    if os.path.exists(filepath):

        logger.info("this file had been downloaded :: %s" % filepath)
        logger.info("this key :: %s" % key)
        return
    else:
        response = requests.get(url, headers=headers, proxies=proxies, stream=True)
        with open(filepath, "wb") as file:
            total_length = int(response.headers.get("content-length"))
            for ch in progress.bar(
                response.iter_content(chunk_size=2391975),
                expected_size=(total_length / 1024) + 1,
            ):
                if ch:
                    file.write(ch)

        logger.info("download success :: %s" % filepath)


def main():
    with open("download.txt", "r") as file:
        keys = list(set(file.readlines()))
    for key in keys:
        if not key.strip():
            continue
        url = "https://www.pornhub.com/view_video.php?viewkey=%s" % key.strip()
        logger.info("url: {}", url)
        task(url,key)
    

if __name__ == "__main__":
    fire.Fire(main)
