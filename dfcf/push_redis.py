import pandas as pd
import redis
r=redis.StrictRedis('192.168.10.48',db=2,decode_responses=True)

# name='要爬取的个股列表.xlsx'
# df=pd.read_excel(name,dtype={'代码':str})
# # print(df.head())
# for i in df['代码'].values:
#     r.lpush('code_list',i)
