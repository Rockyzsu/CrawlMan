import requests,re,os
from lxml import etree
headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.120 Chrome/37.0.2062.120 Safari/537.36'}

def saveToFile(r,filename):
	if os.path.exists(filename):
		return False
	if not r:
		return False
	with open(filename,'wb') as f:
		f.write(r.content)
		return True

def download(url,retry=3):
	
	try:
		r=requests.get(url=url,headers=headers,timeout=60*10)
		if r.status_code ==200:
			return r
		else:
			print "Not able to download, status_code is :",r.status_code
			if retry >0 :
				download(url,retry-1)
			else:
				return None
	except Exception,e:
		print 'exception happend!'
		print e
		if retry >0:
			download(url,retry-1)

		else:
			return None

def getUrl(url):
	r=download(url)
	if not r:
		return None

	content = r.text

	# url='http://f1.htqyy.com/play6/187/m4a/2'
	# download(url)	

	# with open('source.html','r') as f:
	# 	content=f.read()
	# 	tree= etree.HTML(content,parser=etree.HTMLParser(encoding='utf-8'))
	# print tree.xpath('//title/text()')[0]
	fileHost=re.findall('var fileHost="(.*?)";',content)[0]
	mp3=re.findall('var mp3="(.*?)";',content)[0]
	# print fileHost
	# print mp3
	url=fileHost+mp3
	print url
	filename=re.findall('var bdText = "(.*?)";',content)[0]
	filename=re.sub('/','_',filename)
	post_fix=re.findall('format = "(.*?)"',content)[0]
	music_file =  filename.replace(' ','_')+'.'+post_fix
	# print music_file
	
	r_music=download(url)
	if (not os.path.exists(music_file)) or (not r_music):
		saveToFile(r_music,music_file)

def htqyy():
	base_url='http://www.htqyy.com/play/'
	url_new='http://www.htqyy.com/genre/musicList/9?pageIndex={}&pageSize=20&order=hot'
	for page in range(5,7):
		print 'page {} is downloading'.format(page)
		r=download(url_new.format(page))
		# print r.text
		if not r:
			print "Exit! Been block"
			continue
		tree=etree.HTML(r.text,parser=etree.HTMLParser(encoding='utf-8'))
		music_num=tree.xpath('//li[@class="mItem"]/input/@value')
		# print len(music_num)
	# # getUrl(url)
	# seed_url='http://www.htqyy.com/genre/9'
	# # r=download(seed_url)

	# tree=etree.HTML(r.text,parser=etree.HTMLParser(encoding='utf-8'))
	# music_num=tree.xpath('//input[(@type="checkbox") and @name="checked" and (@checked="checked")]/@value')
	# # print len(music_num)
		for i in music_num:
			url=base_url+i
			print url
			getUrl(url)

def main():
	htqyy()
	# getUrl()
	# download()


if __name__ == '__main__':
	main()
	print 'End'