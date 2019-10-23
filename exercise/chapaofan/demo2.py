#获取URL的
from pyquery import PyQuery as pq
import time


movie_urls = {}
movie_names = []

for i in range(1,22):
    url = 'http://www.chapaofan.com/movies.html?page=' + str(i)
    html = pq(url)
    dlbox = html('.content-list .list ul .imgpop a')
    for b in dlbox.items():
        movie_name = b('a').attr('title')
        movie_names.append(movie_name)
        movie_url = b.attr('href')
        movie_urls[movie_name] = movie_url
    print("ok" + str(i))
    time.sleep(2)

# info = dlbox.replace(' ', '').replace('\n', '').replace('\r', '')
# movie_url= re.findall('<listyle="width:30%"><ahref="(.*?)"title=.*?', info)
# movie_name = re.findall('<listyle="width:30%"><ahref=".*?"title=.*?>(.*?)</a></li>',info)
# movie_names.append(movie_name)
# movie_urls[movie_name] = movie_url
# print(movie_urls)

