import requests
import json
import jsonpath
import csv

start_url = 'https://search.damai.cn/searchajax.html?keyword=&cty=&ctl=%E6%BC%94%E5%94%B1%E4%BC%9A&sctl=&tsg=0&st=&et=&order=1&pageSize=30&currPage=0&tn='
response = requests.get(start_url)
response.encoding = 'utf-8'

html = response.text

Hjson = json.loads(html)
# print(Hjson)
item_list = jsonpath.jsonpath(Hjson,'$..resultData')
# print(item_list)
item_dict_list = []

#只会无限取第一个
for actors in item_list:
    show_name = jsonpath.jsonpath(item_list,'*..name')
    show_jpg_url = jsonpath.jsonpath(item_list,'*..verticalPic')
    show_description = jsonpath.jsonpath(item_list,'*..description')
    show_time = jsonpath.jsonpath(item_list,'*..showtime')
    show_place = jsonpath.jsonpath(item_list,'*..price_str')
    show_price = jsonpath.jsonpath(item_list,'*..nameNoHtml')

    item_dict = {'show_name': show_name[0] if show_name else '',
                 'show_jpg_url': show_jpg_url[0] if show_jpg_url else '',
                 'show_description': show_description[0] if show_description else '',
                 'show_time': show_time[0].strip() if show_time else '',
                 'show_place': show_place[0] if show_place else '',
                 'show_price': show_price[0] if show_price else ''}
    item_dict_list.append(item_dict)

with open('result1.csv', 'w', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['show_name',
                                           'show_jpg_url',
                                           'show_description',
                                           'show_time',
                                           'show_place',
                                           'show_price'])
    writer.writeheader()
    writer.writerows(item_dict_list)
