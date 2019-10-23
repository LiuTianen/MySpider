from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html = urlopen(
      "https://morvanzhou.github.io/static/scraping/basic-structure.html"
).read().decode('utf-8')

# res = re.findall(r"<title>(.+?)</title>",html)
# print("\nPage title is:", res[0])

# res = re.findall(r"<p>(.*?)</p>",html, flags=re.DOTALL)
# print("\nPage paragragph is:",res[0])

# res = re.findall(r'href="(.*?)"', html)
# print("\nAll links: ", res)

soup = BeautifulSoup(html, features='lxml')
print(soup.h1)
print('\n', soup.p)
all_href = soup.find_all('a')
all_href = [l['href'] for l in all_href]
print('\n', all_href)