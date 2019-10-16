import requests
import json
import re

# start_url = 'https://bcy.net/apiv3/common/getFeeds?refer=channel&direction=loadmore&cid=6618800694038102275'
headers = {
    "Host": "bcy.net",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"

}
id_list =[]
url_list = []

def get_html(url):
    html = requests.get(url,headers=headers)
    return html.content.decode("utf-8")

def get_wurl(html):
    data = json.loads(html)
    comcert = data['data']['item_info']
    id = re.findall("'item_id': '(.*?)', 'uid':", str(comcert), re.S)
    for i in id:
        url = "https://bcy.net/item/detail/" + i + "?_source_page=cos"
        url_list.append(url)
    print(url_list)

if __name__ == '__main__':
    start_url = 'https://bcy.net/apiv3/common/getFeeds?refer=channel&direction=loadmore&cid=6618800694038102275'
    html = get_html(start_url)
    wurl = get_wurl(html)