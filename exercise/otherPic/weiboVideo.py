import requests
import json
import time
import re

url = 'https://m.weibo.cn/api/container/getIndex?uid=2565076590&luicode=10000011&lfid=1076032565076590&type=uid&value=2565076590&containerid=1076032565076590'

respones = requests.get(url).text.encode('utf-8')
data = json.loads(respones)
comcert = str(data['data']['cards'])
info = comcert.replace(' ', '').replace('\n', '').replace('\r', '')
print(info)
url = re.findall(".*?stream_url_hd':'(.*?)','h5_url",info)
print(url)