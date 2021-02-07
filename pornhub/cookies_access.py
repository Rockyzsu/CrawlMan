import requests

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

params = (
    ('s', 'eyJrIjoiMDgxOTU1NjU4MGNjZjQyOTQ1ODVkZTdhNjM5NjkyMjQzNWE1NzdjYSIsInQiOjE2MDkyMTYwNDJ9'),
    ('v', 'ph5fe22b22c2a32'),
    ('e', '0'),
)

response = requests.get('https://cn.pornhub.com/video/get_media', headers=headers, params=params)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://cn.pornhub.com/video/get_media?s=eyJrIjoiM2JkNzk3OTc3MDYxNjdhN2NiZjg3ZjAxN2YxMDI3YTY3MjNkOWNmMyIsInQiOjE2MDkyMTE5MzJ9&v=ph5c7a39b625845&e=0', headers=headers)
print(response.json())