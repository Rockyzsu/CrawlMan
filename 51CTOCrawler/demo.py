import requests
import subprocess
def demo_validate():
    url='http://v22.51cto.com/2018/12/19/338483/e899/high/loco_video_323000_{}.ts'
    for i in range(112):
        r=requests.get(url.format(i))
        with open('loco_video_323000_{}.ts'.format(i),'wb') as f:
            f.write(r.content)

def write_confile(ts_len):
    txt = ''
    for i in range(ts_len):
        txt += "file 'C:\\git\\CrawlMan\\51CTOCrawler\\loco_video_323000_{}.ts'\n".format(i)
    with open('confile.txt', 'w') as fout:
        fout.write(txt)

def merge_ts_video(title, v_type='.mp4'):
    cmd = 'ffmpeg -f concat -safe 0 -i confile.txt  -c copy %s%s' %(title, v_type)
    print(cmd)
    p = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    print(str(out, 'utf-8'))
    print(str(err, 'utf-8'))

def run_cmd():
    import os
    name = 'loco_video_323000_{}.ts'
    args = '+'.join([name.format(i) for i in range(112)])
    cmd = 'copy /b '+args + ' test.ts'
    print(cmd)
    os.system(cmd)

# demo_validate()
write_confile(112)
merge_ts_video('wanttoplay')
#run_cmd()