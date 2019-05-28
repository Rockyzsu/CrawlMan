import requests, re, os
from lxml import etree
import sys
headers = {
    "Accept": "text/plain, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh,en;q=0.9,en-US;q=0.8,zh-CN;q=0.7",
    "Cache-Control": "no-cache",
    # "Cookie": "Hm_lvt_74e11efe27096f6ef1745cd53f168168=1558946189; blk=1; __cfduid=d996f76d6c8f4b2ddaf74e4c8d0980f0e1558946190; Hm_lpvt_74e11efe27096f6ef1745cd53f168168=1558948519",
    "Host": "www.htqyy.com",
    "Pragma": "no-cache",
    # "Proxy-Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}


def saveToFile(r, filename):
    if os.path.exists(filename):
        return False
    if not r:
        return False
    filename=re.sub('[\/:*?"<>|]', '-', filename)
    with open(filename, 'wb') as f:
        f.write(r.content)
        return True



def download(url, retry=3):
    try:
        r = requests.get(url=url, headers=headers, timeout=60 * 10)
        if r.status_code == 200:
            return r
        else:
            print("Not able to download, status_code is :", r.status_code)
            if retry > 0:
                print('retry')
                download(url, retry - 1)
            else:
                return None
    except Exception as e:
        print('exception happend!')
        print(e)
        if retry > 0:
            download(url, retry - 1)

        else:
            return None


def download_mp3(url):
    headers_temp = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh,en;q=0.9,en-US;q=0.8,zh-CN;q=0.7",
        "Cache-Control": "no-cache",
        # "Connection": "keep-alive",
        # "Cookie": "__cfduid=d996f76d6c8f4b2ddaf74e4c8d0980f0e1558946190; Hm_lvt_74e11efe27096f6ef1745cd53f168168=1558946189,1559005340; blk=0; Hm_lpvt_74e11efe27096f6ef1745cd53f168168=1559005649",
        "Host": "f2.htqyy.com",
        "Pragma": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    }
    try:
        r = requests.get(url=url,headers=headers_temp)
    except Exception as e:
        return None

    else:
        return r


def getUrl(url):
    r = download(url)
    if not r:
        return None

    content = r.text

    try:
        fileHost = re.findall('var fileHost="(.*?)";', content)[0]
    except Exception as e:
        return None

    try:
        mp3 = re.findall('var mp3="(.*?)";', content)[0]
    except Exception as e:
        return None

    url = fileHost + mp3
    print(url)
    filename = re.findall('var bdText = "(.*?)";', content)[0]
    filename = re.sub('/', '_', filename)
    post_fix = re.findall('format = "(.*?)"', content)[0]
    music_file = filename.replace(' ', '_') + '.' + post_fix
    if os.path.exists(music_file):
        print('文件已经存在')
        return None

    r_music = download_mp3(url)
    if r_music:
        saveToFile(r_music, music_file)


def htqyy(music_type,start=1, end=11):
    base_url = 'http://www.htqyy.com/play/'

    # 修改下面的url
    # music_type = 3
    url_new = 'http://www.htqyy.com/genre/musicList/{}?pageIndex={}&pageSize=20&order=hot'
    for page in range(start, end):
        print('page {} is downloading'.format(page))
        r = download(url_new.format(music_type, page))

        if not r:
            print("Exit! Been block")
            continue
        tree = etree.HTML(r.text, parser=etree.HTMLParser(encoding='utf-8'))
        music_num = tree.xpath('//li[@class="mItem"]/input/@value')

        for i in music_num:
            url = base_url + i
            print(url)
            getUrl(url)


def main(music_type):
    htqyy(music_type)


if __name__ == '__main__':
    music_type = sys.argv[1]

    data_path = os.path.join(os.path.dirname(__file__), 'data')
    if not os.path.exists(data_path):
        os.mkdir(data_path)
    os.chdir(data_path)
    main(music_type)
    print('End')
