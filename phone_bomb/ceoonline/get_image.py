import requests
import os
url ='https://login.ceconline.com/Captchastr.do?n=0.7553109359098311'

os.chdir('images')
for i in range(5000):
    print('Downing {} pic'.format(i))
    r = requests.get(url,timeout=20)
    with open('{}.jpg'.format(i),'wb') as f:
        f.write(r.content)
