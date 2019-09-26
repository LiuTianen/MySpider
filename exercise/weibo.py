import requests
import json

start_url = "https://m.weibo.cn/api/container/getIndex?containerid=1076032267821341"

respones = requests.get(start_url).text.encode('utf-8')

data = json.loads(respones)

comcert = data.get('data').get('cards')
#需要找到忽略不需要信息的方法
for Wei in comcert:
    loc = Wei['itemid']
    for BO in loc:
        url = BO['mblog']
        # ['pics']['large']['url']
        img_name = url.split('/')[-1]

        r = requests.get(url, stream=True)
        with open('D:\img\%s' % img_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)
