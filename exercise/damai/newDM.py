import requests
import re
import time
import lxml.html


def get_source(url):
    html = requests.get(url,).text
    return html

def get_toc(html):
    url_list = []
    selector = lxml.html.fromstring(html)
    url = selector.xpath('//div[@class="article-list wow fadeInUp"]/div[@class="content-list"]/div/ul/li[@style="width: 30%"]/a/@href')
    url_list.append(url)
    return url_list

if __name__ == '__main__':
    start_url = 'http://www.daomubiji.org/'
    html = get_source(start_url)
    toc_list = get_toc(html)
    print(toc_list)