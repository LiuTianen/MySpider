import requests
import csv
import re

start_url = "http://www.chapaofan.com/movies.html?page=1"

respones = requests.get(start_url).text.encode('utf-8')

move_box_list = re.findall('<div class="article-list wow fadeInUp">(.*?)</div>',respones,re.S)[0]
print(move_box_list)