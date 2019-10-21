from pyquery import PyQuery as pq
import re
import time
import pymysql


def get_details(url):
    html = pq(url=url)
    # 获取电影的评分
    sore = html(".rating_num").text()
    # 定位到目标信息的区域，并将定位区域网页的PyQuery对象转换为字符串
    info = str(html(".subject.clearfix #info").children())
    # 将对应区域网站信息去空额、去回车换行
    info = info.replace(' ', '').replace('\n', '').replace('\r', '')
    # 用正则表达式匹配导演信息
    director = ""
    try:
        director = re.match('.*?rel="v:directedBy">(.*?)</a>.*?', info).group(1)
    except:
        print("获取导演信息失败")
    # 匹配编剧信息，对于编剧数量大于2的只取前两个，只有一个的只取第一个
    scriptwriters = []
    try:
        scriptwriter = re.match('.*?编剧.*?ahref=.*?">(.*?)</a>.*?ahref=.*?">(.*?)</a>', info)
        scriptwriters.append(scriptwriter.group(1))
        scriptwriters.append(scriptwriter.group(2))
    except:
        scriptwriter = re.match('.*?编剧.*?ahref=.*?">(.*?)</a>.*?', info)
        if scriptwriter:
            scriptwriters.append(scriptwriter.group(1))
    # 匹配演员信息，演员信息较多，一般大于5个，但也有为4个的，这里只匹配五个演员信息，演员信息不足5的电影很少，可以手动输入
    actors = []
    try:
        actor = re.match('.*?主演.*?starring">(.*?)</a>.*?v:starring">(.*?)</a>.*?starring">(.*?)</a>.*?starring">(.*?)</a>.*?starring">(.*?)</a>.*?', info)
        for i in range(1, 6):
            actors.append(actor.group(i))
    except:
        print("未匹配到合适的演员信息")
    # 匹配电影的类型信息，最多匹配两个
    movie_types = []
    try:
        types = re.match('.*?类型.*?genre">(.*?)</span>.*?genre">(.*?)</span>.*?', info)
        for i in range(1, 3):
            movie_types.append(types.group(i))
    except:
        movie_types.append(re.match('.*?类型.*?genre">(.*?)</span>.*?', info).group(1))
        print("电影类型获取失败")
    # 匹配电影的地区信息
    location = ""
    try:
        location = re.match('.*?地区:</span>(.*?)<br/>', info).group(1)
    except:
        print("电影地区获取失败")
    # 匹配电影的语言
    language = ""
    try:
        language = re.match('.*?语言:</span>(.*?)<br/>', info).group(1)
    except:
        print("电影语言获取失败")
    # 匹配电影的上映日期
    movie_date = ""
    try:
        movie_date = re.match('.*?上映日期.*?">(.*?)</span>', info).group(1)
    except:
        print("电影上映日期获取失败")
    # 匹配电影的时长
    movie_time = ""
    try:
        movie_time = re.match('.*?片长.*?">(.*?)</span>', info).group(1)
    except:
        print("电影时长获取失败")
    # 匹配电影的其他名称
    movie_other_name = ""
    try:
        movie_other_name = re.match('.*?又名:</span>(.*?)<br/>', info).group(1)
    except:
        print("电影其他名称获取失败")
    context = {
        "sore": sore,
        "scriptwriters": scriptwriters,
        "director": director,
        "actors": actors,
        "movie_types": movie_types,
        "location": location,
        "language": language,
        "movie_date": movie_date,
        "movie_time": movie_time,
        "movie_other_name": movie_other_name
    }
    return context


if __name__ == '__main__':
    # 链接数据库
    db = pymysql.connect(host="localhost", user="root", password="123qweaa", db="movies", port=3308)
    cur = db.cursor()
    # 通过榜单爬取前250部电影的详细地址
    movie_urls = {}
    movie_names = []
    for i in range(10):
        url = "https://movie.douban.com/top250?start=" + str(i*25)
        html = pq(url=url)
        a = html('.item .pic a')
        for b in a.items():
            movie_name = b('img').attr('alt')
            movie_names.append(movie_name)
            movie_url = b.attr('href')
            movie_urls[movie_name] = movie_url
            # print("%s:%s" % (movie_name, movie_url))
        print("ok"+str(i))
        time.sleep(2)
    id = 1
    for name in movie_names:
        print("开始爬取%s的内容" % name)
        movie_info = get_details(movie_urls[name])
        movie_info["name"] = name
        # 将演员信息的列表转换为字符串
        movie_info["actors"] = '/'.join(movie_info["actors"])
        movie_info["scriptwriters"] = '/'.join(movie_info["scriptwriters"])
        movie_info["movie_types"] = '/'.join(movie_info["movie_types"])
        data = (str(id), movie_info["name"], movie_info["scriptwriters"], movie_info["sore"], movie_info["director"],
                movie_info["actors"], movie_info["movie_types"], movie_info["location"], movie_info["language"],
                movie_info["movie_date"], movie_info["movie_time"], movie_info["movie_other_name"])
        print(data)
        sql_insert = """insert into top(id, movie_name, scriptwriters, sore, director, actors, types, location,
                        language, movie_date, movie_time, movie_other_name)
                        values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                     """
        reCount = cur.execute(sql_insert, data)
        db.commit()
        time.sleep(2)  # 每次操作完一个页面均等待两秒
        id += 1  # id存放电影的排名
    cur.close()
    db.close()