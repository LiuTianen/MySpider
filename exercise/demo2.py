from pyquery import PyQuery as pq


url = 'http://www.chapaofan.com/31736.html'

html = pq(url)
# print(html)

dlbox = html('.download-list li a')
for item in dlbox.items():
    print(item.attr('href'))

