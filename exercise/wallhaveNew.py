import requests
import time
from bs4 import BeautifulSoup
import re
from multiprocessing.dummy import Pool


headers = {
        "Host": "wallhaven.cc",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
    }

def main(offset):
    start_url = "https://wallhaven.cc/latest?page=" + str(offset)
    html = get_source(start_url)
    toc_list = get_toc(html)
    pool = Pool(4)
    pool.map(get_pic, toc_list)

def get_source(url):
    html = requests.get(url, headers=headers).text
    return html

def get_toc(html):
    # 解析链接包含的信息
    soup = BeautifulSoup(html, 'lxml')
    #找到外部的框架
    img_link_ul = soup.find_all('section',{"class":"thumb-listing-page"})
    img_list = []
    for ul in img_link_ul:
        imgs = ul.find_all('a',{"class":"preview"})
        #循环查找img标签
        for img in imgs:
            #找到链接的标签
            url = img['href']
            img_list.append(url)
        return img_list

def get_pic_url(pic_html):
    img_url_loc = re.search('<div class="scrollbox"(.*?)</div>',pic_html,re.S).group(1)
    img_url = re.search('<img id="wallpaper" src="(.*?)"',img_url_loc,re.S).group(1)
    img_name = img_url.split('/')[-1]
    return img_url,img_name

def save(img_url,image_name):
    r = requests.get(img_url, stream=True)
    with open('D:\img\%s' %image_name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            f.write(chunk)

def get_pic(url):
    pic_html = get_source(url)
    img_url,img_name = get_pic_url(pic_html)
    save(img_url,img_name)

if __name__ == '__main__':
    for i in range(1,5):
        main(offset=i)
        time.sleep(1)
