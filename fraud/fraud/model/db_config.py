from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis


engine = create_engine('mysql+pymysql://root:123456z@localhost:3306/spider?charset=utf8')
# engine = create_engine('mysql+pymysql://crawler:Crawler@1234@10.18.4.211:3367/spider?charset=utf8')
DBSession = sessionmaker(bind=engine)


class RedisPool:
    def __init__(self, client_host="localhost", client_port=6379, client_db=0):
        self.client_host = client_host
        self.client_port = client_port
        self.client_db = client_db

    def redis_pool(self):
        pool = redis.ConnectionPool(
            host=self.client_host,
            port=self.client_port,
            db=self.client_db,
            decode_responses=True)
        return redis.StrictRedis(connection_pool=pool)