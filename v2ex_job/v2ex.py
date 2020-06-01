import requests
from lxml import etree
from scrapy import Selector
from twisted.internet import defer
from twisted.internet import reactor
from twisted.web.client import getPage
import pymongo

def get_page():
    """
    总共页码的获取
    :return:
    """
    index_url = 'https://www.v2ex.com/go/jobs'
    index_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
    }
    response = requests.get(url=index_url, headers=index_headers)
    selector = Selector(text=response.text)
    all_page = selector.xpath('//a[@class="page_normal"]/text()').extract()
    all_page = all_page[-1]
    print(all_page)

    return all_page

class V2exJob:
    def __init__(self):
        pass
        self.db = pymongo.MongoClient('10.18.6.46',27001)
        self.doc = self.db['db_parker']['v2ex_job']
        self.agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'


    @defer.inlineCallbacks
    def get_html(self, each_page):
        """
        进行网站信息的获取，并进行返回。
        :param each_page: 
        :return: 
        """
        each_urls = 'https://www.v2ex.com/go/jobs?p=%s' % str(each_page) 
        res = getPage(bytes(each_urls, encoding="utf-8"),agent=self.agent)  # 获取页面，发送http请求,是使用select池将所有socket请求保存，依据此进行计数。
        # print( type(res))  # <class 'twisted.internet.defer.Deferred'>
        res.addCallback(self.parse_infos)  # 对每一个请求都添加一个回调方法
        yield res  # 返回他

    def parse_infos(self, parse_infos):
        print('here')
        parse_infos = parse_infos.decode('utf-8')
        parse_infos = etree.HTML(parse_infos)
        infos = parse_infos.xpath('//span[@class="item_title"]/a/text()')
        url_info = parse_infos.xpath('//span[@class="item_title"]/a/@href')
        url_full_info = list(map(lambda x:'https://www.v2ex.com'+x,url_info))
        # contents = list(zip(url_full_info,infos))
        # print(contents)
        # [for i in infos]
        insert_list = []
        for index in range(len(infos)):
            d={}
            d['url']=url_full_info[index]
            d['title']=infos[index]
            insert_list.append(d)

        try:
            self.doc.insert_many(insert_list)
        except Exception as e:
            print(e)


    def run(self,start,end):
        """
        程序的启动开始采集数据
        :return:
        """
        # all_page = int(self.get_page())

        defer_list = []
        for each_page in range(start, end):  # 禁忌务要一次性访问过多的请求。不然别人会禁掉你的。
            v = self.get_html(each_page)  # 发送请求后立即返回，不等待返回，v是一个特殊对象，标志你发送到那个请求
            defer_list.append(v)
        d = defer.DeferredList(defer_list)  # 将上面的特殊对象列表一起放入DeferredList
        d.addBoth(self.all_done)  # 为所有对象添加回调
        reactor.run()  # 会一直循环，我们需要在任务执行完毕后关闭。含有计数器，执行一个任务，会执行一次get_html,计数减一。单任务执行完毕，计数为0，执行all_done

    def all_done(self, arg):
        print("all done")
        reactor.stop()


if __name__ == '__main__':
    
    # total = int(get_page())
    chunk_size = 3
    total =1770
    piece = total//chunk_size
    print(piece)
    i=2
    # for i in range(piece):
    v2ex_job = V2exJob()
    v2ex_job.run(i*chunk_size,(i+1)*chunk_size)

