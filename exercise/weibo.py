import requests
import json
import time
import re

url_list = []

def getHtml(url):
    respones = requests.get(url).text.encode('utf-8')
    return respones
def get_html(url):
    html = requests.get(url).content.decode('utf-8')
    return html

def getUrl(respones):
    data = json.loads(respones)
    comcert = data['data']['cards']
    url = re.findall("'scheme': \'(https://m.weibo.cn/status.*?)\'", str(comcert), re.S)
    return url

def getPic_url(pic_html):
    url_loc = re.findall('"status": (.*?)"hotScheme"', pic_html, re.S)
    img_loc = re.findall('"pics": (.*?)"bid"', str(url_loc), re.S)
    img_url_loc = re.findall('"large":(.*?)"geo":', str(img_loc), re.S)
    img_url = re.findall('"url": "(.*?.jpg)"', str(img_url_loc), re.S)
    return img_url

def save(img_url):
    for i in img_url:
        url = i
        img_name = i.split('/')[-1]
        r = requests.get(url, stream=True)
        with open('D:\img\%s' % img_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)


def main(offset):
    #
    start_url = "https://m.weibo.cn/api/container/getIndex?containerid=1076032267821341&page=" + str(offset)
    # start_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=2565076590&containerid=1076032565076590&page=' + str(offset)
    respones = getHtml(start_url)
    url = getUrl(respones)
    pic_html = get_html(url.pop())
    img_url = getPic_url(pic_html)
    save(img_url)

if __name__ == '__main__':
    for i in range(1,10):
        main(offset=i)
        time.sleep(1)