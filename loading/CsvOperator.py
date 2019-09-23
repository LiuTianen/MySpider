import csv

#csv 读操作
# with open('result.csv', encoding='utf-8') as f:
#     #for循环需要缩进
#     # reader = csv.DictReader(f)
#     #for循环不需要缩进
#     reader = [x for x in csv.DictReader(f)]
# for row in reader:
#     # print(row)
#     username = row['username']
#     content = row['content']
#     reply_time = row['reply_time']
#     print('用户名：{}，回复内容:{}'.format(username,content))

#csv 写操作

data = [{'name': 'kingname', 'age': 24, 'salary': 99999},
        {'name': 'meiji', 'age': 20, 'salary': 100},
        {'name': '小明', 'age': 30, 'salary': 'N/A'}]
with open('new.csv', 'w', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'age', 'salary'])
    writer.writeheader()
    writer.writerows(data)
    writer.writerow({'name': '超人', 'age': 999, 'salary': 0})