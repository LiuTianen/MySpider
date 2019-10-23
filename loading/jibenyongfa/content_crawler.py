import requests
import pymongo
import redis
from lxml import html

connection = pymongo.MongoClient()
#链接mongoDB
db = connection.Chapter6
#定义方法
handler = db.white

client = redis.StrictRedis()

content_list = []

while client.llen('url_queue') > 0:
    #取urllist，并解码
    url = client.lpop('url_queue').decode()
    #使用链接去请求
    source = requests.get(url).content
    selector = html.fromstring(source)
    chapter_name = selector.xpath('//div[@class="h1title"]/h1/text()')[0]
    content = selector.xpath('//div[@id="htmlContent"]/p/text()')
    content_list.append({'title': chapter_name, 'content': '\n'.join(content)})
#存入数据库
handler.insert(content_list)