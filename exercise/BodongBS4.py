from selenium import webdriver
import time
import re
import requests
from bs4 import BeautifulSoup
import os


browser =webdriver.Firefox()
start_url = 'https://boodo.qq.com/pages/tag.html?name=COSPLAY'

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Content-Type": "application/x-www-form-urlencoded",
}
detail_url_list = []
url_list = []


def get_page_detail(url):
    try:
        browser.get(url)
        js = "return action=document.body.scrollHeight"
        height = browser.execute_script(js)
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        t1 = int(time.time())
        status = True
        num = 0
        while status:
            t2 = int(time.time())
            if t2 - t1 < 30:
                new_height = browser.execute_script(js)
                if new_height > height:
                    time.sleep(1)
                    browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                    height = new_height
                    t1 = int(time.time())
                elif num < 5:
                    time.sleep(3)
                    num = num + 1
                else:
                    print("滚动条已经处于页面最下方!")
                    status = False
                    browser.execute_script('window.scrollTo(0, 0)')
                    break
        time.sleep(2)
        return browser.page_source
    finally:
        browser.close()


def get_deatil_url(html):
    for i in range(1,5):
        ifolder_name = BeautifulSoup(html, 'lxml').find('li', class_="list-waterfall waterfall{}".format(i)).find_all('a', class_="box")
        for a in ifolder_name:
            folder_name = a.get_text()
            path = re.sub(r'[？\\*|”“<>:/()0123456789 ！!。.：]', '', folder_name)
            mkdir(path)
            href = 'https://boodo.qq.com' + a['href']
            urls_crawler(href)

def urls_crawler(url):
    html = requests.get(url).content.decode('utf-8')
    data = re.findall('<div class="layer-login hover-class">(.*?)<div class="time">', html, re.S)
    url = re.findall('<img src="(.*?)" class="imgauto">', str(data), re.S)
    for i in url:
        save(i)

def save(img_url): ##这个函数保存图片
    name = img_url.split('/')[-2]
    img = requests.get(img_url)
    f = open(name + '.jpg', 'ab')
    f.write(img.content)
    f.close()


def mkdir(path): ##这个函数创建文件夹
    path = path.strip()
    isExists = os.path.exists(os.path.join("D:\mzitu", path))
    if not isExists:
        print(u'建了一个名字叫做', path, u'的文件夹！')
        os.makedirs(os.path.join("D:\mzitu", path))
        os.chdir(os.path.join("D:\mzitu", path)) ##切换到目录
        return True
    else:
        pass

if __name__ == '__main__':
    WebBody = get_page_detail(start_url)
    detail_url = get_deatil_url(WebBody)
