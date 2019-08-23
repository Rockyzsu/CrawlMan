import redis
from scrapy.dupefilters import BaseDupeFilter
# 自定义dupefilter
class DupeFilter(BaseDupeFilter):

    def __init__(self,host,port,db,key):
        print('='*20)
        print('using my dupefilter ')
        print('='*20)
        self.r = redis.StrictRedis(host=host,port=port,db=db)
        self.key = key
    
    @classmethod
    def from_settings(cls, settings):
        # result=(dict(settings))

        name=settings.get('BOT_NAME')
        print(f'name is {name}')
        host=settings.get('REDIS_HOST','127.0.0.1')
        port=settings.get('REDIS_PORT')
        print(f'port {port}')
        db=settings.get('REDIS_DB',0)
        print('litters')
        # print(settings.redis_port)
        redis_key=settings.get('REDIS_KEY')
        print('get key')
        print(redis_key)
        print('get host')
        print(host)
        user=settings.get('USER_AGENT')
        print(user)
        if redis_key is None:
            raise ValueError('No value assign to redis_key')

        return cls(host,port,db,redis_key)

    def request_seen(self, request):

        if self.r.sismember(self.key,request.url):
            print(f'url ---{request.url}---has been seen')
            return True

        else:
            self.r.sadd(self.key,request.url)

            return False

    def open(self):  # can return deferred
        pass

    def close(self, reason):  # can return a deferred
        print('dup closed')

    def log(self, request, spider):  # log that a request has been filtered
        pass