import requests
import lxml.html
import csv
from selenium import webdriver
import re

#动态加载的页面，需要后续补充
# driver = webdriver.PhantomJS()
# url = 'https://search.damai.cn/search.htm'
#真的网址
url = 'https://search.damai.cn/searchajax.html?keyword=&cty=&ctl=%E6%BC%94%E5%94%B1%E4%BC%9A&sctl=&tsg=0&st=&et=&order=1&pageSize=30&currPage=2&tn='
# driver.get(url)
source = requests.get(url).content.decode('utf-8')
# source = driver.page_source
# selector = lxml.html.fromstring(source)
# item_list = source.xpath('div[@class="search__itemlist"]')
item_list = re.search('<body>(.*?)</body>',source)
item_dict_list = []
for item in item_list:
    show_name = item.xpath('div[@class="items"]div[@class="items__txt__title"]/a/text()')
    show_url = item.xpath('div[@class="items__txt__title"]/a/@href')
    show_description = item.xpath('div[@class="items__txt__title"]/div[@class="items__txt__time"]/text()')
    show_time = item.xpath('div[@class="items__txt__time"]/a[@class="items__txt__time__icon"]/text()')
    show_place = item.xpath('div[@class="items__txt__price"]/text()')
    show_price = item.xpath('div[@class="items__txt__price"]/span/text()')

    item_dict = {'show_name': show_name[0] if show_name else '',
                 'show_url': 'https:' + show_url[0] if show_url else '',
                 'show_description': show_description[0] if show_description else '',
                 'show_time': show_time[0].strip() if show_time else '',
                 'show_place': show_place[0] if show_place else '',
                 'show_price': show_price[0] if show_price else ''}
    item_dict_list.append(item_dict)

with open('result.csv', 'w', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['show_name',
                                           'show_url',
                                           'show_description',
                                           'show_time',
                                           'show_place',
                                           'show_price'])
    writer.writeheader()
    writer.writerows(item_dict_list)
