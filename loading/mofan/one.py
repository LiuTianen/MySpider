from bs4 import BeautifulSoup
import requests

URL = "https://wallhaven.cc/latest"

#打开链接，并获取相关的信息
html = requests.get(URL).text
#解析链接包含的信息
soup = BeautifulSoup(html,'lxml')
#找到外部的框架
img_link_ul = soup.find_all('section',{"class":"thumb-listing-page"})
#循环查找ul标签
for ul in img_link_ul:
    imgs = ul.find_all('img')
    #循环查找img标签
    for img in imgs:
        #找到链接的标签
        url = img['data-src']
        #stream=True 推迟响应内容的下载
        r = requests.get(url, stream=True)
        #URL切片，去最后一个当文件名
        image_name = url.split('/')[-1]
        with open('D:\img\%s'  % image_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)
        print('Saved %s' % image_name)
#随机打开一个页面进行获取
# for i in range(6):
#     if i > 1:
#         URL = "https://wallhaven.cc/latest?page="+ str(i)

# URL = "http://www.nationalgeographic.com.cn/animals/"
#
# html = requests.get(URL).text
# soup = BeautifulSoup(html, 'lxml')
# img_ul = soup.find_all('ul', {"class": "img_list"})
#
# for ul in img_ul:
#     imgs = ul.find_all('img')
#     for img in imgs:
#         url = img['src']
#         r = requests.get(url, stream=True)
#         image_name = url.split('/')[-1]
#         with open('D:\img\%s' % image_name, 'wb') as f:
#             for chunk in r.iter_content(chunk_size=128):
#                 f.write(chunk)
#         print('Saved %s' % image_name)