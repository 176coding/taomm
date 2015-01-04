# coding:utf-8
import re, os, requests, sys, uuid, hashlib, time

from scrapy import Spider
from bs4 import BeautifulSoup
from taomm.items import TaommItem

reload(sys)
sys.setdefaultencoding('utf-8')
rc = re.compile(r'src=\"(http\:\/\/img[\w\/!\-\.]*\.jpg)\"')  # 正则表达式匹配所有的图片，提前编译


class mmspider(Spider):
    name = 'taomm'
    allowed_domains = ['taobao.com']
    start_urls = []
    # start_urls = ['http://mm.taobao.com/687471686.htm']
    mm_url_name_dict = {}
    page_url = 'http://mm.taobao.com/json/request_top_list.htm?page=%s'

    hello = ''

    def __init__(self):#预处理，主要是先找到各个mm的姓名和主页
        for page_index in range(1, 2):  # 只取前1页
            p_url = self.page_url % page_index
            bs_html = BeautifulSoup(requests.get(p_url).content.decode('GBK'))
            div_personal_info_list = bs_html.find_all('div', {'class': 'personal-info'})
            for personal_info in div_personal_info_list:
                mm_name = personal_info.find('a', {'class': 'lady-name', 'target': '_blank'}).get_text()
                mm_href = personal_info.find('a', {'class': 'lady-avatar', 'target': '_blank'}).get('href')
                self.mm_url_name_dict[mm_href] = mm_name
                self.start_urls.append(mm_href)
                pass
            pass

    def parse(self, response):
        mm_html = BeautifulSoup(response.body).find('div', {'id': 'J_AixiuShow'})
        image_urls = re.findall(rc, str(mm_html))
        mm = TaommItem()
        mm['mm_name'] = self.mm_url_name_dict[response.url]
        mm['image_urls'] = image_urls
        return mm
        pass


if __name__ == '__main__':#测试采用scrapy框架和不采用该框架时间上对比
    start_time = time.time()
    start_urls = []
    # start_urls = ['http://mm.taobao.com/687471686.htm']
    mm_url_name_dict = {}
    page_url = 'http://mm.taobao.com/json/request_top_list.htm?page=%s'
    for page_index in range(1, 2):  # 只取前1页
        p_url = page_url % page_index
        bs_html = BeautifulSoup(requests.get(p_url).content.decode('GBK'))
        div_personal_info_list = bs_html.find_all('div', {'class': 'personal-info'})
        for personal_info in div_personal_info_list:
            mm_name = personal_info.find('a', {'class': 'lady-name', 'target': '_blank'}).get_text()
            mm_href = personal_info.find('a', {'class': 'lady-avatar', 'target': '_blank'}).get('href')
            mm_url_name_dict[mm_href] = mm_name
            start_urls.append(mm_href)
            pass
        pass
    print 'page 1 is over'
    for mm_url in start_urls:
        mm_name = mm_url_name_dict[mm_url]
        path = '../../pics/%s' % mm_name
        os.makedirs(path)
        mm_html = BeautifulSoup(requests.get(mm_url).content).find('div', {'id': 'J_AixiuShow'})
        image_urls = re.findall(rc, str(mm_html))
        for img_url in image_urls:
            resp = requests.get(img_url)
            image_guid = hashlib.sha1(img_url).hexdigest()
            image_path = '../../pics/%s/%s.jpg' % (mm_name, image_guid)
            with open(image_path, 'wb') as f:
                f.write(resp.content)
        print mm_name, 'over'
        pass
    end_time = time.time()
    print end_time - start_time