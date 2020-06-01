import pandas as pd
import redis
r=redis.StrictRedis('192.168.10.48',db=5,decode_responses=True)

name='todo.xlsx'
df=pd.read_excel(name,dtype={'symbol':str})
# print(df.head())
new_list=df.loc[df.industry.str.contains('汽车'), :]['symbol'].tolist()
# for i in df['代码'].values:
#     r.lpush('code_list',i)
old_file = '要爬取的个股列表.xlsx'
df2=pd.read_excel(old_file,dtype={'代码':str})
old_list = df2['代码'].tolist()
for item in new_list:
    if item not in old_list:
        r.set(item,0)
