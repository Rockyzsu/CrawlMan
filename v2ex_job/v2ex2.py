import requests
from lxml import etree
from scrapy import Selector
from twisted.internet import defer
from twisted.internet import reactor
from twisted.web.client import getPage


class V2exJob:
    def __init__(self):
        pass

    def get_page(self):
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
        return all_page

    @defer.inlineCallbacks
    def get_html(self, each_page):
        """
        进行网站信息的获取，并进行返回。
        :param each_page: 
        :return: 
        """
        each_urls = 'https://www.v2ex.com/go/jobs?p=%s' % str(each_page) 
        res = getPage(bytes(each_urls, encoding="utf-8"))  # 获取页面，发送http请求,是使用select池将所有socket请求保存，依据此进行计数。
        # print( type(res))  # <class 'twisted.internet.defer.Deferred'>
        res.addCallback(self.parse_infos)  # 对每一个请求都添加一个回调方法
        yield res  # 返回他

    def parse_infos(self, parse_infos):
        parse_infos = parse_infos.decode('utf-8')
        parse_infos = etree.HTML(parse_infos)
        infos = parse_infos.xpath('//span[@class="item_title"]/a/text()')
        print(infos)

    def run(self):
        """
        程序的启动开始采集数据
        :return:
        """
        all_page = self.get_page()
        defer_list = []
        for each_page in range(1, 10):  # 禁忌务要一次性访问过多的请求。不然别人会禁掉你的。
            v = self.get_html(each_page)  # 发送请求后立即返回，不等待返回，v是一个特殊对象，标志你发送到那个请求
            defer_list.append(v)
        d = defer.DeferredList(defer_list)  # 将上面的特殊对象列表一起放入DeferredList
        d.addBoth(self.all_done)  # 为所有对象添加回调
        reactor.run()  # 会一直循环，我们需要在任务执行完毕后关闭。含有计数器，执行一个任务，会执行一次get_html,计数减一。单任务执行完毕，计数为0，执行all_done

    def all_done(self, arg):
        print("all done")
        reactor.stop()


if __name__ == '__main__':
    v2ex_job = V2exJob()
    v2ex_job.run()

