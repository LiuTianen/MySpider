# -*- coding: UTF-8 -*-

import requests
import threading
import re
import time
import os

all_urls = []
pic_links = []
g_lock = threading.Lock()

class Spider():

    def __init__(self, target_url, headers):
        self.targer_rul = target_url
        self.headers = headers

    def getUrls(self, start_page,page_num):

        global all_urls

        for i in range(start_page, page_num+1):
            url = self.targer_rul % i
            all_urls.append(url)

        threads = []
        for x in range(2):
            t = Producer()
            t.start()
            threads.append(t)

        for tt in threads:
            tt.join()
        print("进行到我这里了")
        for x in range(10):
            ta = Consumer()
            ta.start()
class Producer(threading.Thread):

    def run(self):
        headers = {
            "Host": "wallhaven.cc",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        }
        global all_urls
        while len(all_urls) > 0:
            g_lock.acquire()
            page_url = all_urls.pop()

            g_lock.release()
            try:
                print("分析"+ page_url)
                response = requests.get(page_url, headers=headers,timeout=3)
                all_pic_link = re.findall('<a class="preview" href="(.*?)"',response.text,re.S)
                global all_img_urls
                g_lock.acquire()
                all_img_urls = all_pic_link
                print(all_img_urls)
                g_lock.release()
                time.sleep(1)
            except:
                pass


# 消费者
class Consumer(threading.Thread):
    def run(self):
        headers = {
            "Host": "wallhaven.cc",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        }
        global all_img_urls  # 调用全局的图片详情页面的数组
        print("%s is running " % threading.current_thread)
        while len(all_img_urls) > 0:
            g_lock.acquire()
            img_url = all_img_urls.pop()
            g_lock.release()
            try:
                response = requests.get(img_url, headers=headers)
                response.encoding = 'utf-8'  #设置编码
                # title = re.search('< a class ="username usergroup-2" href="https://wallhaven.cc/user/(.*?)" *>', response.text).group(1)
                all_pic_src = re.findall('< img id = "wallpaper" src="(.*?)" ', response.text, re.S)
                pic_dict = {all_pic_src}  # python字典
                global pic_links
                g_lock.acquire()
                pic_links.append(pic_dict)  # 字典数组
                print(" 获取成功")
                # print(title + " 获取成功")
                g_lock.release()

            except:
                pass
            time.sleep(0.5)

if __name__ == "__main__":
    headers = {
        "Host": "wallhaven.cc",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
    }
    target_url = 'https://wallhaven.cc/latest?page=%d'

    spider = Spider(target_url,headers)
    spider.getUrls(1,2)
    print(all_urls)
