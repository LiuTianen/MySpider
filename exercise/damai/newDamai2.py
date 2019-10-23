import requests
import json
import csv

start_url = 'https://search.damai.cn/searchajax.html?keyword=&cty=&ctl=%E6%BC%94%E5%94%B1%E4%BC%9A&sctl=&tsg=0&st=&et=&order=1&pageSize=30&currPage=0&tn='

respones = requests.get(start_url).text.encode('utf-8')

data = json.loads(respones)

concert = data['pageData']['resultData']

item_dict_list = []

for C in concert:
    show_name = C['name']
    show_jpg_url = C['verticalPic']
    show_description =  C['description']
    show_time = C['showtime']
    show_place = C['price_str']
    show_price = C['venue']

    item_dict = {'show_name': show_name if show_name else '',
                 'show_jpg_url': show_jpg_url if show_jpg_url else '',
                 'show_description': show_description if show_description else '',
                 'show_time': show_time.strip() if show_time else '',
                 'show_place': show_place if show_place else '',
                 'show_price': show_price if show_price else ''}
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