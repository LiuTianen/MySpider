#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time

import requests
from lxml import etree


class MeiZiSpider(object):
    """27 bao website MM spider"""

    def __init__(self):
        self.base_url = 'https://www.27bao.com/meinv/list_1.html'
        self.headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)'}

        # 构建url的前缀
        self.url_prefix = 'https://www.27bao.com'

        # 构建第二层url的前缀
        self.inner_url_prefix = 'https://www.27bao.com/meinv/'

        # 构建点开每个MM内部的所有url
        self.inner_url = 'https://www.27bao.com/meinv/56870_{}.html'

        # 文件保存的路径
        self.path = os.getcwd() + '/27baoMM/'

    def send_first_req(self):
        """
        发送第一层请求，返回首页响应的html内容
        :return: 第一层url的html_str
        """

        html_str = requests.get(self.base_url, headers=self.headers).content.decode()

        return html_str

    def get_total_page(self):
        """
        获取网站MM图片总页数
        :return: 图片总页数
        """

        # 模拟发送请求, 返回响应数据(便于提取总页数)
        html_str = self.send_first_req()

        # 将返回的 html字符串 转换为 element对象
        element_obj = etree.HTML(html_str)

        # 提取末页的url, 再切片提取最大页数
        total_page = element_obj.xpath('//*[@id="pages"]/a[9]/@href')[0].split('_')[-1].split('.')[0]
        print('========该网站MM图片目前共有 {} 页========'.format(total_page))

        return total_page

    def get_each_girl_url(self, each_page_url):
        """
        第一层解析 ---> 获取每一页每个MM(第二层)的url
        :param each_page_url: 每一页的url
        :return: 每一页每个MM(第二层)的url和title
        """

        # 用于存放拼接后每个MM的url
        girl_url_list = []

        # 模拟发送请求, 返回响应数据(便于提取url)
        html_str = self.send_request(each_page_url)

        # 将返回的 html字符串 转换为 element对象
        element_obj = etree.HTML(html_str)

        # 提取所有url后缀  ---> 列表
        url_postfix = element_obj.xpath('/html/body/div[2]/div[2]/ul/li/a/@href')

        # 提取每个妹妹的标题, 便于后面命名
        url_title_li = element_obj.xpath('/html/body/div[2]/div[2]/ul/li/p/a/text()')

        # 遍历提取的url列表, 拼接完整的url, 并保存列表中
        for url in url_postfix:
            # 添加拼接后的url到列表
            girl_url_list.append(self.url_prefix + url)
        # print(girl_url_list)

        title_and_url_li = list(zip(url_title_li, girl_url_list))
        # print(title_and_url_li)

        return title_and_url_li

    def send_request(self, url):
        """
        发送第二层请求，返回响应的html内容
        :param url: 每个MM(第二层)的url
        :return: html_str
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
        except:
            return None
        html_str = response.content

        return html_str

    def parse_data(self, html_str):
        """
        第二层解析 ---> 获取当前的每个url
        :param html_str: 第二层响应的html内容
        :return: 具体每张图片的url
        """

        # 将返回的 html字符串 转换为 element对象
        element_obj = etree.HTML(html_str)
        each_image = element_obj.xpath('/html/body/div[3]/center/img/@src')[0]
        # print(each_image)
        return each_image

    def save_file(self, image_data, title, image_name):
        """
        保存图片
        :param image_data: 具体每张图片的数据
        :param title: 具体每个MM的标题
        :param image_name: 具体每张图片的名字
        :return:
        """

        # 如果目录不存在, 就新建
        if not os.path.exists(self.path + title):
            os.makedirs(self.path + title)
        # 切换到新建目录下
        os.chdir(self.path + title)

        with open(image_name, 'wb') as f:
            f.write(image_data)

    def download(self):
        total_page = self.get_total_page()
        # 开循环, 爬取每个页面的每个妹妹的所有图片
        for page in range(1, int(total_page) + 1):
            print('\n正在爬取第 {} 页...\n'.format(page))
            # 构建每一页的url
            each_page_url = 'https://www.27bao.com/meinv/list_{}.html'.format(page)
            title_and_url_li = self.get_each_girl_url(each_page_url)

            # 遍历获取每个妹妹的总url
            for girl_url in title_and_url_li:
                # print(girl_url[1])

                html_str = self.send_request(girl_url[1])
                print('正在爬取的地址: {}'.format(girl_url[1]))

                # 获取目前爬取的MM内部总页数
                inner_total_page = etree.HTML(html_str).xpath('//*[@id="pages"]/a[last()-1]/text()')[0]
                print('\n目前爬取的MM图片共有 {} 张\n'.format(inner_total_page))

                # 循环并构造每一张图片的url, 请求, 解析, 并保存
                image_data = None
                for inner_page in range(1, int(inner_total_page) + 1):
                    print('正在爬取 {} 第 {} 张图片...'.format(girl_url[0], inner_page))
                    # 构造第二页以后的每个url
                    each_image_url = girl_url[1].split('.html')[0] + '_{}.html'
                    if inner_page == 1:
                        # 获取第一页的url, 因为第一页和其他页的规律不一样，所以这里单独出来
                        each_image_url = self.parse_data(html_str)
                        # html_str = self.send_request(each_image_url)
                        image_data = self.send_request(each_image_url)
                    else:
                        each_image_url = each_image_url.format(inner_page)
                        # print(each_image_url)
                        html_str = self.send_request(each_image_url)
                        image = self.parse_data(html_str)
                        image_data = self.send_request(image)

                    # 如果请求图片的url在5秒之内无响应, 立即终止当前妹妹所有url的循环
                    if image_data is None:
                        print('当前MM的url无响应，正在跳转到下一个MM的url\n')
                        break
                    # 拼接保存图片的名称
                    image_name = str(inner_page) + '.jpg'
                    try:
                        # 切换图片保存目录
                        os.chdir(self.path + girl_url[0])
                        # 判断文件是否存在, 存在则不再保存, 跳过
                        if os.path.exists(image_name):
                            print('第 {} 张已保存, 跳过...'.format(inner_page))
                            continue
                    except Exception as e:
                        print('目录 "{}"：不存在, 正在新建...'.format(self.path + girl_url[0]))

                    # 保存图片到本地
                    self.save_file(image_data, girl_url[0], image_name)
                # print(image_list)
                if image_data:
                    print('\n{} 的所有图片已全部爬取完毕...\n'.format(girl_url[0]))

                # 休眠5秒中, 避免请求一直处于长连接导致ip被封
                time.sleep(10)


if __name__ == '__main__':
    MeiZiSpider().download()