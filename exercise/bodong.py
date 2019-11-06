from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import re
import requests
import os



browser =webdriver.Firefox()
url = 'https://boodo.qq.com/pages/tag.html?name=COSPLAY'
detail_url_list = []
url_list = []
# 下载图片保存路径
DIR_PATH = r"D:\mzitu"

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
                elif num < 3:
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
    box = re.findall('<div class="biz-ugc" style="max-height:none;">(.*?)<div class="mask-waterfall">',html, re.S)
    Top_url = re.findall('<a href="(.*?)" class="box">', str(box), re.S)
    for i in Top_url:
        detail_url = 'https://boodo.qq.com' + i
        detail_url_list.append(detail_url)
    return detail_url_list

def urls_crawler(url):
    for i in url:
        html = requests.get(url=i).content.decode('utf-8')
        folder_name = re.findall('<h1 class="detail-title">(.*?)</h1>', html, re.S)
        
        data = re.findall('<div class="layer-login hover-class">(.*?)<div class="time">', html, re.S)
        url = re.findall('<img src="(.*?)" class="imgauto">', str(data), re.S)
        url_list.append(url)


def make_dir(folder_name):
    """
    新建文件夹并切换到该目录下
    """
    path = os.path.join(DIR_PATH, folder_name)
    # 如果目录已经存在就不用再次爬取了，去重，提高效率。存在返回 False，否则反之
    if not os.path.exists(path):
        os.makedirs(path)
        print(path)
        os.chdir(path)
        return True
    print("Folder has existed!")
    return False

if __name__ == '__main__':
    html = get_page_detail(url)
    detail_url = get_deatil_url(html)
    Pic_url = urls_crawler(detail_url)
    print(detail_url)
