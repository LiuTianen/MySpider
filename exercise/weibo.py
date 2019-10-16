import requests
import json
import jsonpath
import re
from bs4 import BeautifulSoup
#start_url = "https://m.weibo.cn/api/container/getIndex?containerid=1076032267821341"
start_url ='https://m.weibo.cn/api/container/getIndex?type=uid&value=2565076590&containerid=1076032565076590'

respones = requests.get(start_url).text.encode('utf-8')
data = json.loads(respones)
comcert = data['data']['cards']
url = re.findall("'scheme': \'(https://m.weibo.cn/status.*?)\'", str(comcert),re.S)
print(url)
