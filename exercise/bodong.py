from selenium import webdriver
import time
import re
import requests



browser =webdriver.Firefox()
url = 'https://boodo.qq.com/pages/tag.html?name=COSPLAY'

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Content-Type": "application/x-www-form-urlencoded",
    # "Content-Length":str(311),
    # "Referer": "https://boodo.qq.com/pages/tag.html?name=COSPLAY"
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
                elif num < 4:
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
    box = re.findall('<div class="biz-ugc" style="max-height:none;">(.*?)</ul><div class="mask-waterfall">',html, re.S)
    Top_url = re.findall('<a href="(.*?)" class="box">', str(box), re.S)
    for i in Top_url:
        detail_url = 'https://boodo.qq.com' + i
        detail_url_list.append(detail_url)
    return detail_url_list

def urls_crawler(url):
    for i in url:
        html = requests.get(url=i).content.decode('utf-8')
        data = re.findall('<div class="layer-login hover-class">(.*?)<div class="time">', html, re.S)
        url = re.findall('<img src="(.*?)" class="imgauto">', str(data), re.S)
        url_list.append(url)
    return url_list

def save_pic(pic_src):
    """
    保存图片到本地
    """
    for i in pic_src:
        for ii in i:
            time.sleep(0.10)
            img = requests.get(ii, headers=HEADERS, timeout=10)
            img_name = ii.split('/')[-2] + '.jpg'
            with open('D:\imgs\%s' % img_name, 'ab') as f:
                f.write(img.content)
                print(img_name)


if __name__ == '__main__':
    html = get_page_detail(url)
    detail_url = get_deatil_url(html)
    Pic_url = urls_crawler(detail_url)
    save_pic(Pic_url)
