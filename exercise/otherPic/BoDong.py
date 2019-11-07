import requests
import json
import re
import os
import time
"""
波洞cosplay专区的爬虫
未完成部分：
    1、按页面标题分类
    2、持续爬取（目前只爬取了一页）
"""
# start_urls = 'https://cgi.boodo.qq.com/cgi-bin/comicpc_async_cgi?_wv=1&_secondWebView=1&fromWeb=1&platId=110&mqqVersion=&app_version=0.0.0.0&app_platId=109&app_from=8&merge=1&_t=0.8778173866683775&g_tk=false&p_tk=&fromWeb=1'
start_urls = 'https://cgi.boodo.qq.com/cgi-bin/comicpc_async_cgi?_wv=1&_secondWebView=1&fromWeb=1&platId=110&mqqVersion=&app_version=0.0.0.0&app_platId=109&app_from=8&merge=1&_t=0.8161234672080656&g_tk=false&p_tk=&fromWeb=1'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Content-Type": "application/x-www-form-urlencoded",
    # "Content-Length":str(311),
    "Referer": "https://boodo.qq.com/pages/tag.html?name=COSPLAY"
}
# payload_dict = {"0": {"module": "community.TagMtServer.TagMtServerObj", "method": "getTagRecommModuleList",
#                       "param": {"listIndex": str(0), "listSize": str(15), "feedsLength": str(15), "tab": "最热",
#                                 "tagName": "COSPLAY", "category": ""}}}
payload = "param=%7B%220%22%3A%7B%22module%22%3A%22community.TagMtServer.TagMtServerObj%22%2C%22method%22%3A%22getTagRecommModuleList%22%2C%22param%22%3A%7B%22listIndex%22%3A0%2C%22listSize%22%3A15%2C%22feedsLength%22%3A15%2C%22tab%22%3A%22%E6%9C%80%E7%83%AD%22%2C%22tagName%22%3A%22COSPLAY%22%2C%22category%22%3A%22%22%7D%7D%7D"
# payload = "param=%7B%220%22%3A%7B%22module%22%3A%22community.TagMtServer.TagMtServerObj%22%2C%22method%22%3A%22getTagCommonModuleList%22%2C%22param%22%3A%7B%22listIndex%22%3A0%2C%22listSize%22%3A15%2C%22feedsLength%22%3A15%2C%22tab%22%3A%22%E7%8E%8B%E8%80%85COS%22%2C%22tagName%22%3A%22COSPLAY%22%2C%22category%22%3A%22%22%7D%7D%7D"
picurl_list= []
url_list= []
def get_html(url):
    response = requests.request("POST", url, data=payload, headers=headers).text
    return response

def get_Picurl(html):
    result = json.loads(html)
    datas = result['data']['0']
    data = re.findall("{'algorithmSource': 2, 'id': '(.*?)', 'rule_id': .*?}", str(datas), re.S)
    for i in data:
        Pic_url = 'https://boodo.qq.com/pages/ugc/detail.html?id=' + i
        picurl_list.append(Pic_url)
    return picurl_list

def get_picdetail(Purl):
    for i in Purl:
        html = requests.get(url=i).content.decode('utf-8')
        data = re.findall('<div class="layer-login hover-class">(.*?)<div class="time">', html, re.S)
        url = re.findall('<img src="(.*?)" class="imgauto">', str(data), re.S)
        url_list.append(url)
    return url_list

def save(img_url):
    for i in img_url:
        for ii in i:
            r = requests.get(url=ii, stream=True)
            image_name = ii.split('/')[-2] + '.jpg'
            with open('D:\imgs\%s' % image_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    f.write(chunk)

if __name__ == '__main__':
    html = get_html(start_urls)
    Pic_url = get_Picurl(html)
    # print(Pic_url)
    image_url = get_picdetail(Pic_url)
    save(image_url)