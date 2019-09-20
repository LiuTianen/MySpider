import requests
import re
import os
from multiprocessing.dummy import Pool

start_url = 'http://www.daomubiji.org/'

def get_source(url):
    """
    获取网页源代码。
    :param url: 网址
    :return: 网页源代码
    """
    html = requests.get(url)
    return html.content.decode('utf-8')

def get_toc(html):
    """
    获取每一章链接，储存到一个列表中并返回。
    :param html: 目录页源代码
    :return: 每章链接
    """
    toc_url_list = []
    toc_block = re.findall('<h2>盗墓笔记(.*?)</div>',html,re.S)[0]
    toc_url = re.findall('href="(.*?)"', toc_block, re.S)
    for url in toc_url:
        toc_url_list.append(url)
    return toc_url_list

def get_article(html):
    """
    获取每一章的正文并返回章节名和正文。
    :param html: 正文源代码
    :return: 章节名，正文
    """
    chapter_name = re.search('<h1>(.*?)<', html, re.S).group(1)
    text_block = re.search('<p>(.*?)</p>', html, re.S).group(1)
    # text_block = re.search('<div class="content">(.*?)</a></div>', html, re.S)
    return chapter_name, text_block

def save(chapter, article):
    """
    将每一章保存到本地。
    :param chapter: 章节名, 第X章
    :param article: 正文内容
    :return: None
    """
    os.makedirs('盗墓笔记',exist_ok=True)
    with open(os.path.join('盗墓笔记', chapter + '.txt'), 'w', encoding='utf-8')as f:
        f.write(article)

def query_article(url):
    """
    根据正文网址获取正文源代码，并调用get_article函数获得正文内容最后保存到本地。
    :param url: 正文网址
    :return: None
    """
    article_html = get_source(url)
    chapter_name, article_text = get_article(article_html)
    save(chapter_name, article_text)


if __name__ == '__main__':
    toc_html = get_source(start_url)
    toc_list = get_toc(toc_html)
    pool = Pool(4)
    pool.map(query_article, toc_list)