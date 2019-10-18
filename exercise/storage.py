import requests
from pymongo import MongoClient
import redis

redisClient = redis.StrictRedis()
mongoclient = MongoClient()
db = mongoclient['Chapter6']
collection = db['longzu']



def get_html(url):
    html = requests.get(url).content
    return html

def get_url(html):
    selector = html.fromstring(html)
    url_list = selector.xpath('//div[@class="section"]/div[@class="book_list"]/ul/li/a/@href')
    for url in url_list:
        # 写入redis
        redisClient.lpush('long', url)

if __name__ == '__main':
    start_url = 'https://www.kanunu8.com/book3/7748/'
    html = get_html(start_url)
    url_list = get_url(html)
