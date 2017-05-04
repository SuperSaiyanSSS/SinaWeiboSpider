# coding=utf-8
from __future__ import unicode_literals, print_function
import time as tt
from bs4 import BeautifulSoup
import re
import requests
from base import SinaBaseObject
import sina_weibo
import sina_people
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class SinaSearch(SinaBaseObject):
    def __init__(self, search_criteria='', required_count=10, time_delay=0.2):
        super(SinaSearch, self).__init__()
        if search_criteria == '':
            raise ValueError("Must input the search criteria!")
        self.search_criteria = search_criteria
        self.requried_count = required_count
        # 模糊匹配和精确匹配结果
        self.fuzzy_matching_result_list = []
        self.exact_matching_result_list = []
        self.search_list = []
        self.__get_search_result__(required_count=required_count, time_delay=time_delay)

    @property
    def basic_url(self):
        return 'http://weibo.cn/search/mblog?hideSearchFrame=&keyword='+self.search_criteria

    def get_search_result(self):
        requests_content = self.retry_requests(self.search_basic_url)
        print(requests_content)

    def __get_search_result__(self, required_count, time_delay=0.2):
        """
        获取指定用户的微博
        :param required_count: 所需的微博条数
        :param time_delay: 时间延迟
        :return: weibo_list 元素为SinaWeibo对象
            ..  code-block:: python
            [
                {
                    'uid': 'EpO2KnAor',
                    'is_repost': False,
                    'text': '物是人非.',
                    'attitude_count' : 0,
                    'repost_count': 7,
                    'comment_count': 0,
                    'time': '01月08日 04:44'
                    'terminal_source': 'iPad mini'
                },
                {
                    'uid': 'EAJwkph8X',
                    'is_repost': False,
                    'text': '祝你生日快乐',
                    'attitude_count' : 0,
                    'repost_count': 0,
                    'comment_count': 1,
                    'time': '2016-12-30 23:34:34'
                    'terminal_source': '生日动态'
                },
            ]
        """
        weibo_url = self.basic_url
        required_weibo_count = required_count
        weibo_count = 0
        page_count = 1
        weibo_list = []
        now_page_count = 1
        is_first = True
        pattern = re.compile(r'\d+')
        while True:

            tt.sleep(time_delay)
            # 获取页面源码(bs4对象)
            requests_content = self.retry_requests(weibo_url)

            # 获取当前页的微博列表
            unit_list = requests_content.find_all('div', attrs={'class': 'c'})
            for i in unit_list:
                # 每个微博的信息以微博类SinaWeibo存储
                try:
                    if str(i.attrs['id']) and str(i.attrs['id']).startswith('M'):
                        weibo_uid = i.attrs['id'].split('_')[1]
                    else:
                        continue
                except:
                    continue
                weibo = sina_weibo.SinaWeibo(uid=weibo_uid)

                # 检查是否为转发的微博
                for c in i.div.find_all('span'):
                    if str(c.attrs['class']) == "['cmt']":
                        weibo.is_repost = True
                if weibo.is_repost:
                    weibo.text = i.div.find_all('span')[0].get_text()+i.div.find_all('span')[1].get_text()
                else:
                    weibo.text = i.div.span.get_text()[1:]

                weibo.uid = weibo_uid
                print(weibo_uid)
                weibo.attitude_count = int(re.findall(pattern, i.find_all('div')[-1].find_all('a')[-4].get_text())[0])
                weibo.repost_count = int(re.findall(pattern, i.find_all('div')[-1].find_all('a')[-3].get_text())[0])

                # 有的微博处html格式不对
                try:
                    weibo.comment_count = int(re.findall(pattern, i.find_all('div')[-1].find_all('a')[-2].get_text())[0])
                except IndexError:
                    weibo.comment_count = int(re.findall(pattern, i.find_all('div')[-1].find_all('a')[-3].get_text())[0])
                    weibo.repost_count = int(re.findall(pattern, i.find_all('div')[-1].find_all('a')[-4].get_text())[0])
                    weibo.attitude_count = int(re.findall(pattern, i.find_all('div')[-1].find_all('a')[-5].get_text())[0])

                weibo.time = i.find_all('div')[-1].find_all('span', attrs={'class': 'ct'})[0].get_text().split('来自')[0]
                # 有的微博没有终端来源
                try:
                    weibo.terminal_source = i.find_all('div')[-1].find_all('span', attrs={'class': 'ct'})[0].\
                                                                                            get_text().split('来自')[1]
                except IndexError:
                    weibo.terminal_source = 'weibo.com'
                # 计数器加一
                weibo_count += 1
                # 若超过了要求获取的用户数量，则返回
                if weibo_count > required_weibo_count:
                    self.search_list = weibo_list
                    return weibo_list
                weibo_list.append(weibo)

            # 若是第一页，则获取总页数
            if is_first:
                # 若发现‘x/y页’ 则有不止一页
                if requests_content.find(attrs={'id': 'pagelist'}):
                    page_count = requests_content.find(attrs={'id': 'pagelist'}).form.div.contents[-1].strip()
                    page_count = page_count.split('/')[1]
                    page_count = int(re.findall(pattern, page_count)[0])
                    print("现在有"+str(page_count))
                else:
                    self.search_list = weibo_list
                    return weibo_list
                is_first = False

            now_page_count += 1
            if now_page_count >= page_count:
                break

            weibo_url = self.basic_url + '&page=' + str(now_page_count)

        self.search_list = weibo_list
        return weibo_list

headers_2 = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie':'_T_WM=0ff248d78f4984aa135c5b2e53c11079; ALF=1495891126; SCF=AjsEaVa0e8KjEg3yEjwEx270PLOpYvK-1BhV7AdkMSQgBo5dWavtDwJhFsrOKstZIFwodKTXR6HTcJR8MicUons.; SUB=_2A250AV-XDeThGeBP4lQW-CbLyTqIHXVXCmHfrDV6PUNbktANLUinkW0QuhiMpO25FCMzyB3th5DcL_kXrg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhzhoVOn6pkLuGbnO5GBEu35JpX5KMhUgL.Foqp1KqN1hnNeoq2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMceK.cS0nRS0zc; SUHB=0N2lfZuIBwcoTy; SSOLoginState=1493512120',
'Host':'weibo.cn',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'
}

if __name__ == '__main__':
    if 1:
        client = SinaBaseObject
        dic_c = {}
        str_c = headers_2['Cookie']
        for i in str_c.split('; '):
            dic_c[i.split('=')[0]] = i.split('=')[1]
        cookies2 = requests.utils.cookiejar_from_dict(dic_c)
        client.cookies = cookies2
    search_criteria = raw_input(u'请输入要搜索的内容：')
    print(len(search_criteria))
    a = SinaSearch(search_criteria, required_count=20)
    print(a.cookies)
    print(a.search_list)
    for i in a.search_list:
        print(type(i))
        print(i.text)




