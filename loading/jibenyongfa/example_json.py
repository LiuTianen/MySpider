import json

#列表转换成json格式
# book_list = [
#     {'name':'三国演义',
#      'price':99.99},
#     {'name': '西游记',
#      'price': 10.9},
#     {'name': '红楼梦',
#      'price': 100},
#     {'name': '水浒传',
#      'price': 20}
#              ]
#
# book_json = json.dumps(book_list,indent=4)
# print(book_json)


#json格式转为字典

person = {
    'basic_info':{'name':'青南',
                  'age': 24,
                  'sex':'male',
                  'merry': False},

    'work_info':{'salary':99999,
                 'position': 'engineer',
                 'department':None}
}

person_json_indent = json.dumps(person, indent=4)
print(f'person_json_indent变量的类型为：{type(person_json_indent)}')

person_dict = json.loads(person_json_indent)
print(f'person_doct变量的类型为：{type(person_dict)}')
print(person_dict['basic_info']['name'])