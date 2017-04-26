# coding=utf-8

from __future__ import unicode_literals, print_function
import time as tt
import pymongo
from bs4 import BeautifulSoup
import re
import requests
from base import SinaBaseObject
import sina_people
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class SinaWeibo(SinaBaseObject):
    """
    新浪微博的微博类
    """
    def __init__(self, uid=None, text='', time='', required_count=0):
        super(SinaWeibo, self).__init__()
        self.uid = uid
        self.href = 'http://weibo.cn/comment/'+uid
        self.main_page_resource = ''
        # 作者信息
        self.author_name = ''
        self.author_uid = ''
        # 评论
        self.comment_count = 0
        self.comment_list = []
        self.hot_comment_list = []
        # 赞
        self.attitude_count = 0
        self.attitude_list = []
        # 转发
        self.repost_count = 0
        self.repost_list = []

        self.text = text
        self.time = time
        self.terminal_source = ''
        if required_count != 0:
            self.get_text()
            self.comment_list = self.get_comment_list(required_comment_count=required_count)
            self.attitude_list = self.get_attitude_list(required_attitude_count=required_count)
            self.repost_list = self.get_repost_list(required_repost_count=required_count)

    def set_attributes(self, comment_count=0, attitude_count=0, repost_count=0):
        self.comment_count = comment_count
        self.attitude_count = attitude_count
        self.repost_count = repost_count

    def set_text(self, text):
        self.text = text

    def set_time(self, time):
        self.time = time

    def get_text(self):
        """
        获取微博内容
        :return: str类型的微博文本内容
        """
        if self.text != '':
            return self.text
        else:
            requests_content = self.retry_requests(self.href, uid=self.uid)
            self.main_page_resource = requests_content
            self.text = requests_content.find(attrs={'id': 'M_'}).div.span.get_text()
            self.__get_author_data__()
            return self.text

    # 获取微博作者的昵称和uid
    def __get_author_data__(self):
        self.author_name = self.main_page_resource.find(attrs={'id': 'M_'}).div.a.get_text()
        self.author_uid = self.main_page_resource.find(attrs={'id': 'M_'}).div.a.attrs['href'].split('/')[-1]

    def __get_attribute_list__(self, target_attribute_type, target_attribute_fuction, required_attribute_count=20,
                               time_delay=0.2):
        """

        :param target_attribute_type:
        :param target_attribute_fuction:
        :param required_attribute_count:
        :param time_delay:
        :return:
        """
        attribute_url = 'http://weibo.cn/' + str(target_attribute_type) + '/' + str(self.uid)
        print(attribute_url)
        attribute_list = []
        attribute_count = 0
        page_count = 1
        now_page_count = 1
        is_first = True
        pattern = re.compile(r'\d+')
        while True:
            tt.sleep(time_delay)
            # 获取页面源码(bs4对象)
            requests_content = self.retry_requests(attribute_url, uid=self.uid)

            # 获取当前页的关注列表
            unit_list = requests_content.find_all('div', attrs={'class': 'c'})
            for i in unit_list:
                # 调用具体函数提取内容
                attribute = target_attribute_fuction(i)
                if not attribute:
                    continue
                # 计数器加一
                attribute_count += 1
                # 若超过了要求获取的属性数量，则返回
                if attribute_count > required_attribute_count:
                    return attribute_list
                attribute_list.append(attribute)

            # 若是第一页，则获取总页数
            if is_first:
                # 若发现‘x/y页’ 则有不止一页
                if requests_content.find(attrs={'id': 'pagelist'}):
                    page_count = requests_content.find(attrs={'id': 'pagelist'}).form.div.contents[-1].strip()
                    page_count = page_count.split('/')[1]
                    page_count = int(re.findall(pattern, page_count)[0])
                    print(page_count)
                else:
                    return attribute_list
                is_first = False

            now_page_count += 1
            if now_page_count >= page_count:
                break

            attribute_url = 'http://weibo.cn/' + str(target_attribute_type) +'/' + str(self.uid) +'?&&page=' + \
                            str(now_page_count)

        return attribute_list

    @staticmethod
    def __get_comment_list__(unit):
        comment = {}
        # 若有id属性且id值以C开头，则证明是评论
        try:
            if str(unit.attrs['id']).startswith('C'):
                comment['uid'] = str(unit.attrs['id'])
            else:
                return False
        except:
            return False
        comment['name'] = unit.a.get_text()
        # 有的用户是个性域名，不符合/u/‘uid’的特点，故同时存href
        comment['people'] = sina_people.SinaPeople(uid=str(unit.a.attrs['href']).split('/')[-1],
                                       href='http://http://weibo.cn'+str(unit.a.attrs['href']))
        # 检查是否有“热门”标签
        try:
            is_hot = unit.span.attrs['kt']
            if is_hot:
                comment['is_hot'] = True
            else:
                comment['is_hot'] = False
        except:
            comment['is_hot'] = False
        # 正则匹配获取评论的赞数
        pattern = re.compile(r'\d+')
        comment['attitude_count'] = int(re.findall(pattern, unit.find_all('span', attrs={'class': 'cc'})[-2].get_text())
                                        [0])
        print(comment['name'])
        print(comment['attitude_count'])
        # 获取评论的正文
        comment['text'] = unit.find_all('span', attrs={'class': 'ctt'})[0].get_text()
        # 获取评论的时间
        comment['time'] = unit.find_all('span', attrs={'class': 'ct'})[-1].get_text().split('来自')[0]
        # 获取评论的终端来源
        comment['terminal_source'] = unit.find_all('span', attrs={'class': 'ct'})[-1].get_text().split('来自')[1]
        return comment

    def get_comment_list(self, required_comment_count=5, time_delay=0.2):
        """
        :param required_comment_count: 指定获取的条数
        :param time_delay: 时间延迟
        :return: 该微博的评论列表
            ..  code-block:: python
            [
                {
                    'uid': 'C_4100160336496887',
                    'is_hot': False,
                    'name' : '-猫猫站不稳-',
                    'people': <__main__.SinaPeople object at 0x0000000003498BE0>,
                    'time': 今天 20:44,
                    'terminal_source': 'iPhone 6'
                    'text': '稀罕你!'
                    'attitude_count': 0
                },
            ]
        """
        self.comment_list = self.__get_attribute_list__('comment', self.__get_comment_list__,
                                    required_attribute_count=required_comment_count, time_delay=time_delay)
        return self.comment_list

    # 获取热门评论
    def get_hot_comment_list(self):
        for i in self.comment_list:
            if i['is_hot']:
                self.hot_comment_list.append(i)
        return self.hot_comment_list


    @staticmethod
    def __get_attitude_list__(unit):
        attitude = {}
        # 若有a标签则为点赞的unit
        try:
            attitude['name'] = unit.a.get_text()
            attitude['time'] = unit.span.get_text()
            attitude['people'] = SinaPeople(uid=str(unit.a.attrs['href']).split('u/')[1],
                                            href='http://weibo.cn' + str(unit.a.attrs['href']))
        except:
            return False
        return attitude

    def get_attitude_list(self, required_attitude_count=5, time_delay=0.2):
        self.attitude_list = self.__get_attribute_list__('attitude', self.__get_attitude_list__,
                                    required_attribute_count=required_attitude_count, time_delay=time_delay)
        return self.attitude_list

    @staticmethod
    def __get_repost_list__(unit):
        repost = {}
        try:
            repost['name'] = unit.a.get_text()
            repost['text'] = unit.contents[1]
            print(str(unit.contents[1]))
            repost['people'] = SinaPeople(uid=unit.a.attrs['href'].split('u/')[1],
                                          href='http://weibo.cn/'+unit.a.attrs['href'])
        except:
            return False
        return repost

    def get_repost_list(self, required_repost_count=5, time_delay=0.2):
        self.repost_list = self.__get_attribute_list__('repost', self.__get_repost_list__, required_attribute_count=5,
                                                       time_delay=0.2)
        return self.repost_list
