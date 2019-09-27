import requests
import csv
import re
from bs4 import BeautifulSoup


start_url = "http://www.chapaofan.com/movies.html?page=1"

respones = requests.get(start_url).text

soup = BeautifulSoup(respones,'lxml')
move_big_box = soup.find_all('div',{"class":"content"})
url_list = []
for div in move_big_box:
    div1 = div.find_all('div',{"class":"list"})
    for ul in div1:
        ul = ul.find_all('ul',{"class":"item"})
        for li in ul:
            li = li.find_all('li',{"style":"width: 30%"})
            for aurl in li:
                aurl = aurl.find_all('a')
                for url in aurl:
                    Burl = url['href']
                    title_name = url['title']
                    item_dict = {
                            'title_name': title_name if title_name else '',
                            'url' : Burl if Burl else ''
                    }
                    url_list.append(item_dict)
    with open('chapaofan.csv', 'w', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'title_name',
            'url'
        ])
        writer.writeheader()
        writer.writerows(url_list)