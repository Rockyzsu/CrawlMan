import redis
from scrapy.dupefilters import BaseDupeFilter
# 自定义dupefilter
class DupeFilter(BaseDupeFilter):

    def __init__(self,host,port,db,key,reset):
        print('='*20)
        print('using my dupefilter ')
        print('='*20)
        self.r = redis.StrictRedis(host=host,port=port,db=db)
        self.key = key
        self.reset = reset

    
    @classmethod
    def from_settings(cls, settings):
        # result=(dict(settings))

        # name=settings.get('BOT_NAME')
        # print(f'name is {name}')
        host=settings.get('REDIS_HOST','127.0.0.1')
        port=settings.get('REDIS_PORT',6379)
        
        print(f'host:{host},port {port}')
        db=settings.get('REDIS_DB',0)
        redis_key=settings.get('REDIS_KEY')


        print(f'redis key{redis_key}')
        user=settings.get('USER_AGENT')
        print(user)
        if redis_key is None:
            raise ValueError('No value assign to redis_key')

        reset=settings.getbool('REDIS_REST',False)
       


        return cls(host,port,db,redis_key,reset)

    def request_seen(self, request):

        if self.r.sismember(self.key,request.url):
            print(f'url ---{request.url}---has been seen 重复URL')

            return True

        else:
            # print('add an url in redis')
            self.r.sadd(self.key,request.url)

            return False

    def open(self):  # can return deferred
        pass

    def close(self, reason):  # can return a deferred
        print('dup closed')

        if self.reset:
            print(f'delete redis key {self.key}')
            self.r.delete(self.key)

    def log(self, request, spider):  # log that a request has been filtered
        pass