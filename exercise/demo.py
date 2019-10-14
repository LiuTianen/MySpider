#utf-8
import requests
import re
import lxml.html
from bs4 import BeautifulSoup

# start_url = 'https://www.kanunu8.com/files/terrorist/200909/858.html'
# root_url = 'https://www.kanunu8.com'
start_url = 'http://www.daomubiji.org/'
# html = requests.get(start_url).content.decode('utf-8')
# # soup = BeautifulSoup(html, 'lxml')
# # print(soup)
# patter = re.compile('<h2>盗墓笔记(.*?)</div>', re.S)
# toc = re.findall(patter,html)
# list = re.findall('href="(.*?)"',str(toc),re.S)
# print(list)
# print(html.encoding)
# print(html.headers)
# print(html)
html = requests.get(start_url)
print(html.headers)
