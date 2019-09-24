import requests, os
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import hashlib
import threading
import queue
def get_html(url):
    headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Host':'edu.51cto.com',
    }
    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'
    return r.text
def parse_couse_id(url):
    content = get_html(url)
    bsobj = BeautifulSoup(content, 'lxml')
    lesson_lists = bsobj.find("div", {"class":"lessonList"}).ul.findAll("li", {"class":"lesson"})
    lesson_id_list = []
    name_list = []
    for item in lesson_lists:
        name = item.a["title"]
        lesson_id = item.a["href"].split('?id=')[1]
        lesson_id_list.append(lesson_id)
        name_list.append(name)
    return lesson_id_list, name_list
def get_m3u8_url(vid):
    sign = "eDu_51Cto_siyuanTlw"
    auth_md5 = (vid + sign).encode("utf-8")
    # print(auth_md5)
    auth_str = hashlib.md5(auth_md5).hexdigest()
    # print(auth_str)
    headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3',
    'Host':'edu.51cto.com',
    'Refer':'http://edu.51cto.com/center/course/lesson/index?id='+vid,
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    }
    parms = {
        'type':'course',
        'lesson_type':'course',
        'sign':'auth_str',
        'lesson_id':vid,
    }
    url = 'http://edu.51cto.com/center/player/play/get-lesson-info'
    r = requests.get(url, headers=headers, params=parms)
    r.encoding = 'utf-8'
    # print(r.json())
    return (r.json()['dispatch'][0]['url'])
def m3u8_list(m3u8_url, title):
    urlretrieve(m3u8_url, title)
    m3u8_url_list = []
    with open(title, 'rt') as fout:
        # print(fout.read())
        flag = False
        for f in fout.readlines():
            if f.startswith('#EXTINF'):
                flag = True
            elif flag:
                # print(f)
                m3u8_url_list.append(f[0:-1])
                flag = False
            else:
                pass
    if os.path.exists(title):
        os.remove(title)
    return m3u8_url_list
def down(url, path):
    def Schedule(a,b,c):
        '''''
        a:已经下载的数据块
        b:数据块的大小
        c:远程文件的大小
        '''
        per = 100.0 * a * b / c
        if per > 100 :
            per = 100
        print('%.2f%%' % per)
    urlretrieve(url, path)
def down_ts(m3u8_url_list, path='', title=''):
    for index, url in enumerate(m3u8_url_list):
        # print(url)
        path_name = path + '\\' + str(index) + '.ts'
        down(url, path_name)
        print('[%d/%d]\t\tNow Downing %s_%d.ts' %(index, len(m3u8_url_list)-1, title, index))
'''
# 使用多线程下载视频
def down_ts(m3u8_url_list, path='', title=''):
    url_lists = []
    for index, url in enumerate(m3u8_url_list):
        # print(url)
        path_name = path + '\\' + str(index) + '.ts'
        url_lists.append((url, path_name))
    def consumer(url_lists, url_que):
        for urls in url_lists:
            url_que.put(urls)
    def producter(url_que):
        while True:
            urls = url_que.get()
            urlretrieve(*urls)
            print("Downing:", urls[1])
            url_que.task_done()
    url_que = queue.Queue()
    for n in range(4):
        down_thread = threading.Thread(target=producter, args=(url_que,))
        down_thread.start()
    consumer(url_lists, url_que)
    url_que.join()
'''
def write_confile(path, ts_len):
    txt = ''
    for i in range(ts_len):
        txt += 'file \'%s/%d.ts\'\n' %(path, i)
    with open('confile.txt', 'w') as fout:
        fout.write(txt[0:-1])
def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print('ERROR : Path not exist [%s]' %file_path)
# 合并ts视频文件
def merge_ts_video(title, v_type='.mp4'):
    cmd = 'ffmpeg -f concat -i confile.txt -c copy %s%s' %(title, v_type)
    print(cmd)
    p = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    print(str(out, 'utf-8'))
    print(str(err, 'utf-8'))
def usage():
    print()
    print('Usage: down_51cto_video.py url')
    print('Example: down_51cto_video.py http://edu.51cto.com/center/course/lesson/index?id=98717')
    print()
def main(url):
    lesson_id_list, name_list = parse_couse_id(url)
    for index, url_id in enumerate(lesson_id_list):
        m3u8_url = get_m3u8_url(url_id)
        v_name = name_list[index]   
        m3u8_url_list = m3u8_list(m3u8_url, url_id)
        ts_len = len(m3u8_url_list)
        if os.path.exists(url_id):
            os.removedirs(url_id)
        os.mkdir(url_id)
        down_ts(m3u8_url_list, path=url_id, title=test_name)
        write_confile(url_id, ts_len)
        try:
            merge_ts_video(url_id)
            os.rename(url_id+'.mp4', title+'.mp4')
            # 删除临时文件
            delList = os.listdir(v_key)
            for item in delList:
                del_path = os.path.join(v_key, item)
                os.remove(del_path)
            os.removedirs(v_key)
            os.remove('confile.txt')
            os.remove(title+'.m3u8')
        except Exception as e:
            print(e)

import requests
def demo_validate():
    url='http://v22.51cto.com/2018/12/19/338483/e899/high/loco_video_323000_{}.ts'
    for i in range(112):
        r=requests.get(url.format(i))
        with open('loco_video_323000_{}.ts'.format(i),'wb') as f:
            f.write(r.content)

if __name__ == '__main__':
    try:
        url = sys.argv[1]
    except Exception as e:
        # print(e)
        usage()
    else:
        main(url)