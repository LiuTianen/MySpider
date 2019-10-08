import requests
import json
import jsonpath
start_url = "https://m.weibo.cn/api/container/getIndex?containerid=1076032267821341"

respones = requests.get(start_url).text.encode('utf-8')

data = json.loads(respones)

comcert = data.get('data').get('cards')
# print(comcert)

#jsonpath的用法
url = jsonpath.jsonpath(comcert,expr='$..avatar_hd')
print(url)