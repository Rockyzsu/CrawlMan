# coding: utf-8
import datetime
import requests
from qianfan_models import DBSession, Apps
from mayidaili_tool import useproxy

session = DBSession()


def storedata(d):
    # print('in store')
    obj = Apps(
        app_rank=d['app_rank'],
        appName=d['appName'],
        developCompanyFullName=d['developCompanyFullName'],
        second_cateName=d['second_cateName'],
        first_cateName=d['first_cateName'],
        appId=d['appId'],
        activeNums=d['activeNums'],
        activeAvgDay=d['activeAvgDay'],
        runtimeAvgDay=d['runtimeAvgDay'],
        runtimeAvgPersonRatio=d['runtimeAvgPersonRatio'],
        activeAvgDayRatio=d['activeAvgDayRatio'],
        runtimeNums=d['runtimeNums'],
        launchNums=d['launchNums'],
        runtimeNumsRatio=d['runtimeNumsRatio'],
        launchAvgDayRatio=d['launchAvgDayRatio'],
        statDate=d['statDate'],
        developCompanyAbbr=d['developCompanyAbbr']
    )
    session.add(obj)
    try:
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()


def getprimarycatelogy():
    url = 'http://qianfan.analysys.cn//qianfan/category/primaryCateAppList'
    headers = {'Origin': 'http://qianfan.analysys.cn', 'Content-Length': '37',
               'Accept-Language': 'zh,en;q=0.8,en-US;q=0.6', 'Accept-Encoding': 'gzip, deflate',
               'X-Requested-With': 'XMLHttpRequest', 'Host': 'qianfan.analysys.cn', 'Accept': '*/*',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
               'Connection': 'keep-alive',
               'Cookie': 'referer=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3Ds1vGcLrFlTzWdgeR9Eb6oH2SHim6I-hq9_F_71Z798voFVykU6D1AM6RV4QBQsta%26wd%3D%26eqid%3Dad661995000071910000000659e41f8b; notice=1505724860000; gdxidpyhxdE=iT89tkVk5PnnVNx1k1l0YSj%2Fr4Z0vwV5P6Goz38E7poaP1RfeVNbgqdf2zwyOXdSyhItPR70y6LloitbiOcYSJGhDMxWImn3nNaPNjYaXzodyAxwSQJfOKIP0m%5CCjdTB5dxHfQCis%5CnYZIu2Gfds%2Fzgw0rG%5Ca7Y%2BMzBUYm5RoVYTde2L%3A1508123613312; _9755xjdesxxd_=31; algtipA3home-=true; algtipA3-=true; JSESSIONID=9EE2A7B29E2988256B328DD16F8FAE5C; Hm_lvt_abe5c65ffb860ebf053a859d05bee0ea=1508156428,1508159435,1508159448,1508205878; Hm_lpvt_abe5c65ffb860ebf053a859d05bee0ea=1508205987; cacheCookie=%5B%7B%22appIds%22%3A2601273%2C%22categoryIds%22%3A1011007%2C%22itemId%22%3A2601273%2C%22itemName%22%3A%22%E5%84%BF%E6%AD%8C%E5%A4%9A%E5%A4%9A%22%7D%5D',
               'Pragma': 'no-cache', 'Cache-Control': 'no-cache',
               'Referer': 'http://qianfan.analysys.cn/view/category/list.html',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

    data = {'rootCateId': '',
            '$reinitialize': 'undefined'}

    r = requests.post(url=url, data=data, headers=headers)
    # print(r.status_code)
    # print(r.text)
    js = r.json()
    primary_cates = js['datas']['primaryCateList']
    for primary_cate in primary_cates:
        d = dict()
        first_cate_id = primary_cate['cateId']
        first_cateName = primary_cate['cateName']
        d['first_cate_id'] = first_cate_id
        d['first_cateName'] = first_cateName
        print('first cate id', first_cate_id)
        print('first cate name ', first_cateName)
        getcatelogy(d)


def getcatelogy(d):
    url = 'http://qianfan.analysys.cn//qianfan/category/cateAppList'
    header = {'Origin': 'http://qianfan.analysys.cn', 'Content-Length': '52',
              'Accept-Language': 'zh,en;q=0.8,en-US;q=0.6', 'Accept-Encoding': 'gzip, deflate',
              'X-Requested-With': 'XMLHttpRequest', 'Host': 'qianfan.analysys.cn', 'Accept': '*/*',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
              'Connection': 'keep-alive',
              'Cookie': 'referer=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3Ds1vGcLrFlTzWdgeR9Eb6oH2SHim6I-hq9_F_71Z798voFVykU6D1AM6RV4QBQsta%26wd%3D%26eqid%3Dad661995000071910000000659e41f8b; notice=1505724860000; gdxidpyhxdE=iT89tkVk5PnnVNx1k1l0YSj%2Fr4Z0vwV5P6Goz38E7poaP1RfeVNbgqdf2zwyOXdSyhItPR70y6LloitbiOcYSJGhDMxWImn3nNaPNjYaXzodyAxwSQJfOKIP0m%5CCjdTB5dxHfQCis%5CnYZIu2Gfds%2Fzgw0rG%5Ca7Y%2BMzBUYm5RoVYTde2L%3A1508123613312; _9755xjdesxxd_=31; algtipA3home-=true; algtipA3-=true; cacheCookie=%5B%7B%22appIds%22%3A2601273%2C%22categoryIds%22%3A1011007%2C%22itemId%22%3A2601273%2C%22itemName%22%3A%22%E5%84%BF%E6%AD%8C%E5%A4%9A%E5%A4%9A%22%7D%5D; JSESSIONID=9EE2A7B29E2988256B328DD16F8FAE5C; Hm_lvt_abe5c65ffb860ebf053a859d05bee0ea=1508156428,1508159435,1508159448,1508205878; Hm_lpvt_abe5c65ffb860ebf053a859d05bee0ea=1508205878',
              'Pragma': 'no-cache', 'Cache-Control': 'no-cache',
              'Referer': 'http://qianfan.analysys.cn/view/category/list.html',
              'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

    data = {'parentCateId': d['first_cate_id'],
            'statDate': '2016/01/01',
            '$reinitialize': 'undefined'}

    r = requests.post(url=url, data=data, headers=header)
    # print(r.status_code)
    # print(r.text)
    js = r.json()
    cates = js['datas']['cateInfoList']
    # print(len(cates))
    for cate in cates:
        # d=dict()
        # first_cateName = cate['cateName']
        cateId = cate['cateId']
        # d['first_cateName']=first_cateName
        d['cateId'] = cateId
        print('second id', cateId)
        print('second name', cate['cateName'])
        #getdata(d)
        # print('type')
        # print(type(cateId))
        '''
        if (cateId==1191294) or (cateId==1041045):
            print('got')
            getdata(d)
        else:
            continue
        '''


def getdata(d):
    url = 'http://qianfan.analysys.cn/qianfan/category/appIndexs'
    header = {'Origin': 'http://qianfan.analysys.cn', 'Content-Length': '59',
              'Accept-Language': 'zh,en;q=0.8,en-US;q=0.6', 'Accept-Encoding': 'gzip, deflate',
              'X-Requested-With': 'XMLHttpRequest', 'Host': 'qianfan.analysys.cn', 'Accept': '*/*',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
              'Connection': 'keep-alive',
              'Cookie': 'referer=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3Ds1vGcLrFlTzWdgeR9Eb6oH2SHim6I-hq9_F_71Z798voFVykU6D1AM6RV4QBQsta%26wd%3D%26eqid%3Dad661995000071910000000659e41f8b; notice=1505724860000; gdxidpyhxdE=iT89tkVk5PnnVNx1k1l0YSj%2Fr4Z0vwV5P6Goz38E7poaP1RfeVNbgqdf2zwyOXdSyhItPR70y6LloitbiOcYSJGhDMxWImn3nNaPNjYaXzodyAxwSQJfOKIP0m%5CCjdTB5dxHfQCis%5CnYZIu2Gfds%2Fzgw0rG%5Ca7Y%2BMzBUYm5RoVYTde2L%3A1508123613312; _9755xjdesxxd_=31; algtipA3home-=true; algtipA3-=true; cacheCookie=%5B%7B%22appIds%22%3A2601273%2C%22categoryIds%22%3A1011007%2C%22itemId%22%3A2601273%2C%22itemName%22%3A%22%E5%84%BF%E6%AD%8C%E5%A4%9A%E5%A4%9A%22%7D%5D; JSESSIONID=9EE2A7B29E2988256B328DD16F8FAE5C; Hm_lvt_abe5c65ffb860ebf053a859d05bee0ea=1508156428,1508159435,1508159448,1508205878; Hm_lpvt_abe5c65ffb860ebf053a859d05bee0ea=1508205987',
              'Pragma': 'no-cache', 'Cache-Control': 'no-cache',
              'Referer': 'http://qianfan.analysys.cn/view/category/detail.html?categoryId=%s' % d['cateId'],
              'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

    data = {'categoryId': d['cateId'],
            'statDate': '2016/01/01',
            'menuCode': '1001001'}
    try:
        r = useproxy(url=url, headers=header, postdata=data, post=True)

        # print(r.status_code)
        # print(r.text)
        js = r.json()
        app_lists = js['datas']['appIndexList']
        # print(len(app_lists))
        # d = dict()
        if len(app_lists) == 0:
            print("empyt app in catelogy", d['first_cateName'])
        for rank, app in enumerate(app_lists):
            app_rank = rank + 1
            try:
                appName = app['appName']
            except:
                appName = 'Nodata'
            # 开发公司全称
            try:
                developCompanyFullName = app['developCompanyFullName']

            except Exception, e:
                print(e)
                developCompanyFullName = 'Nodata'
            # 二级目录

            try:
                runtimeAvgPersonRatio = app['runtimeAvgPersonRatio']
            except:
                runtimeAvgPersonRatio = 0
            try:
                activeAvgDayRatio = app['activeAvgDayRatio']
            except:
                activeAvgDayRatio = 0

            try:
                runtimeNumsRatio = app['runtimeNumsRatio']
            except:
                runtimeNumsRatio = 0
            try:
                launchAvgDayRatio = app['launchAvgDayRatio']
            except:
                launchAvgDayRatio = 0

            # 公司名字缩写
            try:
                developCompanyAbbr = app['developCompanyAbbr']
            except:
                developCompanyAbbr = 'Nodata'
            try:
                second_cateName = app['cateName']
            except:
                second_cateName = 'Nodata'
            # 使用时长
            try:
                runtimeNums = app['runtimeNums']
            except:
                runtimeNums = 0
            # 启动次数
            try:
                launchNums = app['launchNums']
            except:
                launchNums = 0
            try:
                appId = app['appId']
            except:
                appId = 'Nodata'
            try:
                statDate = datetime.datetime.fromtimestamp(app['statDate'] / 1000.0)
            except:
                statDate = 'Nodata'
            try:
                activeNums = app['activeNums']
            except:
                activeNums = 0
            try:
                activeAvgDay = app['activeAvgDay']
            except:
                activeAvgDay = 0
            try:
                runtimeAvgDay = app['runtimeAvgDay']
            except:
                runtimeAvgDay = 0

            d['app_rank'] = app_rank
            d['appName'] = appName

            # 开发公司全称
            print(appName)
            d['developCompanyFullName'] = developCompanyFullName
            d['second_cateName'] = second_cateName
            # d['first_cateName'] = first_cateName
            d['appId'] = appId
            # 活跃用户
            d['activeNums'] = activeNums
            d['activeAvgDay'] = activeAvgDay
            d['runtimeAvgDay'] = runtimeAvgDay
            d['runtimeAvgPersonRatio'] = runtimeAvgPersonRatio
            d['activeAvgDayRatio'] = activeAvgDayRatio

            # 使用时长
            d['runtimeNums'] = runtimeNums
            # 启动次数
            d['launchNums'] = launchNums
            d['runtimeNumsRatio'] = runtimeNumsRatio
            d['launchAvgDayRatio'] = launchAvgDayRatio

            d['statDate'] = statDate

            # 公司名字缩写

            d['developCompanyAbbr'] = developCompanyAbbr
            storedata(d)

    except  Exception, e:
        print(e)
        print(d['cateId'])
        # r = requests.post(url=url, data=data, headers=header)
        print('wait')


getprimarycatelogy()
# getcatelogy()
# getdata()
session.close()
