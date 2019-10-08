# import re
# import csv
#
# with open('source.txt', 'r', encoding='utf-8') as f:
#     source = f.read()
#
# result_list = []
# #首先获得包含每一层楼所有信息的大文本块
# every_reply = re.findall('l_post l_post_bright j_l_post clearfix  "(.*?)p_props_tail props_appraise_wrap', source, re.S)
#
# #从每一个大文本块里面提取出来各个楼层的发帖人姓名，发帖内容和发帖时间
# for each in every_reply:
#     result = {}
#     result['username'] = re.findall('username="(.*?)"',each, re.S)[0]
#     result['content'] = re.findall('j_d_post_content ">(.*?)<', each, re.S)[0].replace('            ', '')
#     result['reply_time'] = re.findall('class="tail-info">(2017.*?)<', each, re.S)[0]
#     result_list.append(result)
#
# with open('tieba.csv', 'w', encoding='utf-8') as f:
#     writer = csv.DictWriter(f, fieldnames=['username', 'content', 'reply_time'])
#     writer.writeheader()
#     writer.writerows(result_list)


import requests
import lxml.html
source = requests.get('http://tieba.baidu.com/f?ie=utf-8&kw=%E5%91%A8%E6%9D%B0%E4%BC%A6&red_tag=g2896306195').content
selector = lxml.html.fromstring(source)
post_title_list = selector.xpath('//div[@class="threadlist_title pull_left j_th_tit "]/a/text()')
for post_title in post_title_list:
    print(post_title)
