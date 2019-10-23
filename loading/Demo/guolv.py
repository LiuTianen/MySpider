#xpath过滤标签提取url

import requests
from lxml import etree
root_url = 'http://www.ygdy8.com'
#请求阳光电影网站
req = requests.get(root_url)
#输出请求的状态码
status_code = req.status_code
print(status_code)
#输出网页源码
req.encoding = 'gb2312'
html = req.text
selector = etree.HTML(html)
infos = selector.xpath('//div[@class="contain"]/ul/li[position()<10]/a')
for info in infos:
    info_text = info.xpath('text()')[0]
    if info_text == '经典影片':
        continue
    info_url = root_url + info.xpath('@href')[0]
    #将阳光电影网首页导航栏前9个菜单url抓取,输出结果为可以正常访问的url, 并过滤掉"经典影片"的菜单url
    #print(info_text,info_url)
    req1 = requests.get(info_url)
    req1.encoding = 'gb2312'
    html1 = req1.text
    selector1 = etree.HTML(html1)
    page = selector1.xpath('//div[@class="co_content8"]/div[@class="x"]//text()')[1].split('/')[0].replace('共','').replace('页','').strip()
    page = int(page)
    page_list = selector1.xpath('//div[@class="co_content8"]/div[@class="x"]//a/@href')[0].replace('2.html','')
    url_list = []
    for i in range(1,page+1):
        page_url = info_url.replace('index.html','')+page_list+str(i)+'.html'
        url_list.append(page_url)
    print(info_text,'共'+str(page)+'页',url_list)