# -*- coding: UTF-8 -*-
import requests
import threading
import time
import lxml.html
import os

all_urls = []  # 我们拼接好的图片集和列表路径

all_img_urls = []       #图片列表页面的数组

g_lock = threading.Lock()  #初始化一个锁

pic_links = []

headers = {
        "Host": "wallhaven.cc",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
    }
class Spider():
    # 构造函数，初始化数据使用
    def __init__(self, target_url, headers):
        self.target_url = target_url
        self.headers = headers

    # 获取所有的想要抓取的URL
    def getUrls(self, start_page, page_num):
        global all_urls
        # 循环得到URL
        for i in range(start_page, page_num + 1):
            url = self.target_url % i
            all_urls.append(url)

# 生产者，负责从每个页面提取图片列表链接
class Producer(threading.Thread):
    def run(self):
        global all_urls
        while len(all_urls) > 0:
            g_lock.acquire()  # 在访问all_urls的时候，需要使用锁机制
            page_url = all_urls.pop()  # 通过pop方法移除最后一个元素，并且返回该值

            g_lock.release()  # 使用完成之后及时把锁给释放，方便其他线程使用
            try:
                print("分析" + page_url)
                response = requests.get(page_url, headers=headers, timeout=3).text.encode('utf-8')
                selector = lxml.html.fromstring(response)
                all_pic_link = selector.xpath('//div[@id="thumbs"]/section/ul/li/figure/a[@class="preview"]/@href')
                global all_img_urls
                g_lock.acquire()  # 这里还有一个锁
                all_img_urls += all_pic_link  # 这个地方注意数组的拼接，没有用append直接用的+=也算是python的一个新语法吧
                print(all_img_urls)
                g_lock.release()  # 释放锁
                time.sleep(0.5)
            except:
                pass


# 消费者
class Consumer(threading.Thread):
    def run(self):
        global all_img_urls  # 调用全局的图片详情页面的数组
        print("%s is running " % threading.current_thread)
        while len(all_img_urls) > 0:
            g_lock.acquire()
            img_url = all_img_urls.pop()
            g_lock.release()
            try:
                response2 = requests.get(img_url, headers=headers).text.encode('utf-8')
                selector = lxml.html.fromstring(response2)
                title = selector.xpath('//section[@id="showcase"]/div[@class="scrollbox"]/img/@data-wallpaper-id')
                all_pic_src = selector.xpath('//section[@id="showcase"]/div[@class="scrollbox"]/img/@src')
                pic_dict = {title: all_pic_src}  # python字典
                global pic_links
                g_lock.acquire()
                pic_links.append(pic_dict)  # 字典数组
                print(title + " 获取成功")
                g_lock.release()

            except:
                pass
            time.sleep(0.5)



#会触发死循环？？？
class DownPic(threading.Thread):
    def run(self):
        while True:          #写成死循环，检测图片链接数组是否更新
            global pic_links       # 导入储存所有图片链接的数组
            # 先上锁，锁住
            g_lock.acquire()
            if len(pic_links) == 0:
                g_lock.release()
                continue
            else:
                pic = pic_links.pop()
                g_lock.release()
                for key, values in pic.items():
                    path = key.rstrip("//")   #删除开头的/
                    pos = "图片保存位置"
                    is_exists = os.path.exists(pos+"//"+path)

                    if not is_exists:
                        # 如果目录不存在 ，创建目录，
                        os.makedirs(pos+"//"+path)
                        print(pos+"//"+path, "创建成功")

                    else:
                        print(pos+"//"+path, "已经存在")

                    for pic in values :
                        filename = pos+"//"+path+"/"+pic.split('/')[-1]
                        if os.pos+"//"+path.exists(filename):
                            continue
                        else:
                            try:
                                response = requests.get(pic, headers=headers)
                                with open(filename, 'wb') as f:
                                    f.write(response.content)
                                    f.close()
                            except Exception as e:
                                print(e)
                                pass
        # while True:
        #     global pic_links
        #     # 上锁
        #     g_lock.acquire()
        #     if len(pic_links) == 0:  # 如果没有图片了，就解锁
        #         # 不管什么情况，都要释放锁
        #         g_lock.release()
        #         continue
        #     else:
        #         pic = pic_links.pop()
        #         g_lock.release()
        #         image_name = pic.split('/')[-1]
        #         r = requests.get(pic, stream=True)
        #         with open('D:\img\%s' % image_name, 'wb') as f:
        #             for chunk in r.iter_content(chunk_size=128):
        #                 f.write(chunk)
        #         print('Saved %s' % image_name)

if __name__ == "__main__":
    threads = []

    target_url = 'https://wallhaven.cc/latest?page=%d'  # 图片集和列表规则

    spider = Spider(target_url, headers)
    spider.getUrls(1, 2)
    print(all_urls)
    for x in range(2):
        t = Producer()
        t.start()  # 可以调用 自己实现的fun方法， 但是不会多线程运行
        threads.append(t)

    for tt in threads:
        tt.join()
    print("进行到我这里了")

    for x in range(10):
        ta = Consumer()
        ta.start()

    for x in range(1):
        down = DownPic()
        down.start()