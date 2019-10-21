import requests
import re
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup

headers= {
    "Host": "movie.douban.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
}
url_list = []

def get_html(url):
    html = requests.get(url,headers=headers).text
    return html


def get_url(html):
    soup = BeautifulSoup(html,'lxml')
    box = soup.find_all('li', {"class":"poster"})
    for a in box:
        # 找到链接的标签
        box1 = a.find_all('a')
        for i in box1:
            url = i['href']
            url_list.append(url)
    # return url_list
    print(url_list)

if __name__ == '__main':
    start_url = 'https://movie.douban.com/'
    html = get_html(start_url)
    url = get_url(html)
