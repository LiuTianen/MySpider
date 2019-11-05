## 使用说明
这是一个**scrapy**爬虫Demo，爬取目标：[wallhaven](https://wallhaven.cc/)壁纸分享网站

目录结构说明：
│  main.py  *运行文件
│  README.md
│  scrapy.cfg
└─bizhi
    │  items.py
    │  middlewares.py
    │  pipelines.py
    │  settings.py	
    │  __init__.py
    ├─spiders
    	│  wallhaven.py  *爬虫主文件
    	│  __init__.py

clone项目后，直接运行main.py即可。

PS：需要先安装scrapy。（pip install scrapy）

