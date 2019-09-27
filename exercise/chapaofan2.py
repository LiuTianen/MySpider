import requests
import threading
import time
import lxml.html
import csv

all_urls = []
all_urls_list = []
g_lock = threading.Lock()
movies_links = []
"""
半成品，参考：https://blog.csdn.net/hihell/article/details/82490799
"""

class Spider():

    def __init__(self,target_url,headers):
        self.target_url = target_url
        self.headers =headers
    def getUrls(self, start_page, page_num):
        #添加全局变量
        global all_urls
        #循环得到URL
        for i in range(start_page,page_num+1):
            url = self.target_url % i
            all_urls.append(url)

        for x in range(2):
            t = Producer()
            t.start()
        threads= []
        # 开启两个线程去访问
        for x in range(2):
            t = Producer()
            t.start()
            threads.append(t)

        for tt in threads:
            tt.join()

        print("进行到我这里了")
        # 开启10个线程去获取链接
        for x in range(10):
            ta = Consumer()
            ta.start()
class Producer(threading.Thread):

    def run(self):
        headers = {
            "Host": "www.chapaofan.com",
            "User - Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 76.0.3809.132Safari / 537.36"
        }
        global all_urls
        while len(all_urls) > 0:
            g_lock.acquire() #访问all_urls的时候，需要使用锁机制
            page_url = all_urls.pop() #通过pop方法移出最后一个元素，并且返回该值

            g_lock.release() #使用完成之后及时把锁给释放，方便其他线程使用
            try:
                print("分析"+page_url)
                response = requests.get(page_url, headers=headers, timeout=5).text.encode('utf-8')
                selector = lxml.html.fromstring(response)
                url_list = selector.xpath('//div[@class="list"]/ul/li[@style="width: 30%"]/a/@href')
                global all_urls_list
                g_lock.acquire()  # 这里还有一个锁
                all_urls_list+= url_list  # 这个地方注意数组的拼接，没有用append直接用的+=也算是python的一个新语法吧
                print(all_urls_list)
                g_lock.release()  # 释放锁
                time.sleep(2)
            except:
                pass


# 消费者
class Consumer(threading.Thread):
    def run(self):
        headers = {
            "Host": "www.chapaofan.com",
            "User - Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 76.0.3809.132Safari / 537.36"
        }
        global all_urls_list  # 调用全局的图片详情页面的数组
        print("%s is running " % threading.current_thread)
        while len(all_urls_list) > 0:
            g_lock.acquire()
            movies_url = all_urls_list.pop()

            g_lock.release()
            # try:
            print(movies_url)
            response2 = requests.get(movies_url, headers=headers).text.encode('utf-8')
            selector2 = lxml.html.fromstring(response2)
            movies_list = []
            title = selector2.xpath('//div[@class="details-box"]/h2/text()')
            ed2k_link = selector2.xpath('//div[@class="download-list"]/ul/li/a/@href')
            introduction = selector2.xpath('//div[@class="introduce mt"]/text()')
            item_dict = {
                '片名': title if title else '',
                '磁力链接': ed2k_link if ed2k_link else '',
                '简介': introduction if introduction else ''
            }
            movies_list.append(item_dict)
        with open('chapaofan2.csv', 'w', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                '片名',
                '磁力链接',
                '简介'
            ])
            writer.writeheader()
            writer.writerows(movies_list)


if __name__ =="__main__":
    target_url = 'http://www.chapaofan.com/movies.html?page=%d'
    headers ={
        "Host": "www.chapaofan.com",
        "User - Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 76.0.3809.132Safari / 537.36"
    }
    spider =Spider(target_url,headers)
    spider.getUrls(1,3)
    print(all_urls)


