import requests
import re
import time
import lxml.html

headers ={
        "Host": "www.chapaofan.com",
        "User - Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 76.0.3809.132Safari / 537.36"
    }
def main(offset):
    start_url = 'http://www.chapaofan.com/movies.html?page='+ str(offset)
    html = get_source(start_url)
    toc_list = get_toc(html)
    print(toc_list)

def get_source(url):
    html = requests.get(url,headers=headers).text
    return html

def get_toc(html):
    url_list = []
    selector = lxml.html.fromstring(html)
    url = selector.xpath('//div[@class="article-list wow fadeInUp"]/div[@class="content-list"]/div/ul/li[@style="width: 30%"]/a/@href')
    url_list.append(url)
    return url_list

if __name__ == '__main__':
    for i in range(1,10):
        main(offset=i)
        time.sleep(1)
