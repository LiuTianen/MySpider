from pyquery import PyQuery as pq
import re

url = 'http://www.chapaofan.com/31736.html'

html = pq(url)
# print(html)

box = str(html('.details-top .details-box'))
dlbox = html('.download-list li a')
info = box.replace(' ', '').replace('\n', '').replace('\r', '')
#
# print(info)
# print(dlbox)
director = ""
try:
    director = re.findall('导演:<ahref=".*?">(.*?)</a></span></div>', info)
    print(director)
except:
    print("获取导演信息失败")
# 匹配编剧信息，对于编剧数量大于2的只取前两个，只有一个的只取第一个
scriptwriters = []
try:
    scriptwriter = re.match('.*?编剧.*?ahref=.*?">(.*?)</a>.*?ahref=.*?">(.*?)</a>', info)
    scriptwriters.append(scriptwriter.group(1))
    scriptwriters.append(scriptwriter.group(2))
    print(scriptwriters)
except:
    scriptwriter = re.match('.*?编剧.*?ahref=.*?">(.*?)</a>.*?', info)
    if scriptwriter:
        scriptwriters.append(scriptwriter.group(1))
# 匹配演员信息，演员信息较多，一般大于5个，但也有为4个的，这里只匹配五个演员信息，演员信息不足5的电影很少，可以手动输入
actors = []
try:
    actor = re.match('.*?主演.*?ahref=.*?">(.*?)</a>.*?ahref=.*?">(.*?)</a>.*?ahref=.*?">(.*?)</a>.*?ahref=.*?">(.*?)</a>.*?ahref=.*?">(.*?)</a>.*?', info)
    for i in range(1, 6):
        actors.append(actor.group(i))
    print(actors)
except:
    print("未匹配到合适的演员信息")

# 匹配电影的类型信息，最多匹配两个
movie_types = []
try:
    types = re.match('.*?类型.*?ahref=.*?>(.*?)</a>.*?ahref=.*?>(.*?)</a>', info)
    for i in range(1, 3):
        movie_types.append(types.group(i))
    print(movie_types)
except:
    movie_types.append(re.match('.*?类型.*?ahref=.*?>(.*?)</a>', info).group(1))
    print("电影类型获取失败")

 # 匹配电影的地区信息
location = ""
try:
    location = re.match('.*?地区:(.*?)</span></div>', info).group(1)
    print(location)
except:
    print("电影地区获取失败")

 # 匹配电影的语言
language = ""
try:
    language = re.match('.*?语言:(.*?)</span></div>', info).group(1)
    print(language)
except:
    print("电影语言获取失败")

# 匹配电影的上映日期
movie_date = ""
try:
    movie_date = re.match('.*?上映日期:(.*?)</span></div>', info).group(1)
    print(movie_date)
except:
    print("电影上映日期获取失败")
# 匹配电影的时长
movie_time = ""
try:
    movie_time = re.match('.*?片长:(.*?)</span></div>', info).group(1)
    print(movie_time)
except:
    print("电影时长获取失败")
# 匹配电影的其他名称
movie_other_name = ""
try:
    movie_other_name = re.match('.*?又名:(.*?)</span></div>', info).group(1)
    print(movie_other_name)
except:
    print("电影其他名称获取失败")

ed2k_list = []

for item in dlbox.items():
    ed2k= item.attr('href')
    ed2k_list.append(ed2k)
print(ed2k_list)