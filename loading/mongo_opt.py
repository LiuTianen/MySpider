# from pymongo import MongoClient
#
# client = MongoClient()
# database = client['Chapter6']
# collection = database['spider']
# data = {'id': 0, 'name': 'kingnam', 'age': 20, 'salary': 999999}
# collection.insert(data)
#
# more_data = [
#     {'id': 6, 'name': '一一', 'age': 29, 'salary': 0},
#     {'id': 7, 'name': '二二', 'age': 29, 'salary': -100},
#     {'id': 8, 'name': '三三', 'age': 29, 'salary': 1000},
#     {'id': 9, 'name': '四四', 'age': 29, 'salary': '未知'},
# ]
# collection.insert(more_data)

# 查询数据
# content = [x for x in collection.find({'age': 29}, {'_id': 0, 'name': 1, 'salary': 1})]
# content_obj = collection.find({'age': 29}, {'_id': 0, 'name': 1, 'salary': 1})
# # content = []
# for each in content_obj:
#     content.append(each)

# content = [x for x in collection.find({'age': 29})]
#逻辑查询
# content =[x for x in collection.find({'age':{'$gte': 29, '$lte': 40}})]
# collection.find({'age': {'$gt': 29}}) #查询所有age > 29的记录
# collection.find({'age': {'$gte': 29, '$lte': 40}})  #查询29 ≤ age ≤ 40的记录
# collection.find({'salary': {'$ne': 29}}) #查询所有salary不等于29的记录


#排序
#降序
# content =[x for x in collection.find({'age': {'$gte': 29, '$lte': 40}}).sort('age', -1)]
#升序
# content = [x for x in collection.find({'age': {'$gte': 29, '$lte': 40}}).sort('age', 1)]
#
# print(content)


#逐条插入和批量插入的对比
import pymongo
import datetime
import random
import time

connection = pymongo.MongoClient()
db = connection.Chapter6
handler_1_by_1 = db.Data_1_by_1
handler_bat = db.Data_bat

today = datetime.date.today()

#逐条插入数据
# start_1_by_1 = time.time()
# for i in range(10000):
#     delta = datetime.timedelta(days=i)
#     fact_date = today - delta
#     handler_1_by_1.insert({'time': str(fact_date), 'data': random.randint(0, 10000)})
# end_1_by_1 = time.time()

#批量插入数据
start_bat = time.time()
insert_list = []
for i in range(10000):
    delta = datetime.timedelta(days=i)
    fact_date = today - delta
    insert_list.append({'time': str(fact_date), 'data': random.randint(0, 10000)})

handler_bat.insert(insert_list)
end_bat = time.time()

# print(f'一条一条插入数据，耗时：{end_1_by_1 - start_1_by_1}')
print(f'批量插入数据，耗时: {end_bat - start_bat}')