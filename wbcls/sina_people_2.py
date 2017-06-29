# coding=utf-8
from __future__ import unicode_literals, print_function
import time as tt
import pymongo
from bs4 import BeautifulSoup
import re
import requests
from base import SinaBaseObject
from sina_weibo import SinaWeibo
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class SinaPeople(SinaBaseObject):
    """
    新浪微博的用户类
    """
    def __init__(self, uid=None, href=None):
        super(SinaPeople, self).__init__()
        self.uid = str(uid)
        self.href = href
        self.name = ''
        self.sex = '未知'
        self.location = '未知'
        self.birthday = '未知'
        self.member_level = ''
        self.weibo_count = ''
        self.follow_count = ''
        self.follow_list = []
        self.fans_count = ''
        self.fans_list = []
        if not self.href:
            self.href = 'http://weibo.cn/u/'+self.uid
        if not self.uid:
            self.uid = self.href.split('cn/')

    def get_personal_information(self):
        """
        注：新浪有奇怪的BUG 带cookies访问http://weibo.cn/3193031501/info这类个人资料url时，总是File not found
            若不带cookies则不能访问该页
            所以只能获取个人主页简单的性别和地点信息
        :return:
        """
        requests_content = self.retry_requests(self.href)
        info_content = requests_content.find('div', attrs={'class': 'ut'}).contents[0]
        self.name = info_content.split(' ')[0].strip()
        self.sex = info_content.split(' ')[1].split('/')[0].strip()
        self.location = info_content.split(' ')[1].split('/')[1].strip()
        print(self.name, self.sex, self.location)

    def __get_member_list__(self, required_member_count=20, time_delay=0.2, target_member_type='fans'):
        """
        获取所指定的当前用户的关注/粉丝列表
        每个被关注者或粉丝的信息存储在dict中
        :param required_member_count: 指定获取用户的数量
        :param time_delay: 延迟时间
        :param target_member_type: 指定获取用户的种类：fans或follow
        :return: member_list: 存放已获取的用户列表

        TODO: 获取人物基本信息
        """
        member_url = 'http://weibo.cn/' + str(self.uid) + '/' + str(target_member_type)
        self.href = member_url
        print(member_url)
        member_list = []
        member_count = 0
        page_count = 1
        now_page_count = 1
        is_first = True
        while True:

            tt.sleep(time_delay)
            # 获取页面源码(bs4对象)
            requests_content = self.retry_requests(member_url, uid=self.uid)

            # 获取当前页的关注列表
            unit_list = requests_content.find_all('table')
            for i in unit_list:
                # 每个用户的信息以dict存储
                member = {}
                member['href'] = str(i.tr.td.a.attrs['href'])
                try:
                    member['uid'] = i.tr.td.a.attrs['href'].split('u/')[1]
                except:
                    member['uid'] = i.tr.td.a.attrs['href'].split('cn/')[1]
                member['name'] = i.tr.find_all('td')[1].a.get_text()
                # 正则匹配获取粉丝的粉丝数
                pattern = re.compile(r'\d+')
                # 若粉丝是大V，则多了一个图片标签
                try:
                    member['is_v'] = False
                    member['fans_count'] = int(re.findall(pattern, i.tr.find_all('td')[1].contents[2])[0])
                except:
                    member['fans_count'] = int(re.findall(pattern, i.tr.find_all('td')[1].contents[3])[0])
                    member['is_v'] = True
                print(member['name'])
                print(member['fans_count'])
                # 计数器加一
                member_count += 1
                # 若超过了要求获取的用户数量，则返回
                if member_count > required_member_count:
                    return member_list
                member_list.append(member)

            # 若是第一页，则获取总页数
            if is_first == True:
                # 若发现‘x/y页’ 则有不止一页
                if requests_content.find(attrs={'id': 'pagelist'}):
                    page_count = requests_content.find(attrs={'id': 'pagelist'}).form.div.contents[-1].strip()
                    page_count = page_count.split('/')[1]
                    page_count = int(re.findall(pattern, page_count)[0])
                    print(page_count)
                else:
                    return member_list
                is_first = False

            now_page_count += 1
            if now_page_count >= page_count:
                break

            member_url = 'http://weibo.cn/' + str(self.uid) + '/'+str(target_member_type)+'?page=' + str(now_page_count)

        return member_list

    def get_fans_list(self, required_member_count=20, time_delay=0.2):
        """
        获取当前用户的粉丝列表
        :param required_member_count: 限定获取的数量
        :param time_delay: 时间延迟
        :return: 指定数量的粉丝基本信息列表
            ..  code-block:: python
            [
                {
                    'fans_count': 104,
                    'is_v' : False,
                    'href': 'http://weibo.cn/u/5977488639',
                    'uid': 5977488639,
                    'name': '小山环环1996'
                },
                {
                    'fans_count': 10,
                    'is_v' : False,
                    'href': 'http://weibo.cn/u/6187915152',
                    'uid': 6187915152,
                    'name': '08iCu京伯'
                },
            ]
        """
        self.fans_list = self.__get_member_list__(required_member_count=required_member_count, time_delay=time_delay,
                                              target_member_type='fans')
        return self.fans_list

    def get_follow_list(self, required_member_count=20, time_delay=0.2):
        """
        获取当前用户的关注列表
        :param required_member_count: 限定获取的数量
        :param time_delay: 时间延迟
        :return: 指定数量的关注基本信息列表
            ..  code-block:: python
            [
                {
                    'fans_count': 104,
                    'is_v' : False,
                    'href': 'http://weibo.cn/u/5977488639',
                    'uid': 5977488639,
                    'name': '小山环环1996'
                },
                {
                    'fans_count': 10,
                    'is_v' : False,
                    'href': 'http://weibo.cn/u/6187915152',
                    'uid': 6187915152,
                    'name': '08iCu京伯'
                },
            ]
        """
        self.follow_list = self.__get_member_list__(required_member_count=required_member_count, time_delay=time_delay,
                                                target_member_type='follow')
        return self.follow_list

    def get_weibo_list(self, required_weibo_count=10, time_delay=0.2):
        """
        获取指定用户的微博
        :param required_weibo_count: 所需的微博条数
        :param time_delay: 时间延迟
        :return: weibo_list 元素为SinaWeibo对象
            ..  code-block:: python
            [
                {
                    'uid': 'EpO2KnAor',
                    'text': '物是人非.',
                    'attitude_count' : 0,
                    'repost_count': 7,
                    'comment_count': 0,
                    'time': '01月08日 04:44'
                    'terminal_source': 'iPad mini'
                },
                {
                    'uid': 'EAJwkph8X',
                    'text': '祝你生日快乐',
                    'attitude_count' : 0,
                    'repost_count': 0,
                    'comment_count': 1,
                    'time': '2016-12-30 23:34:34'
                    'terminal_source': '生日动态'
                },
            ]
        """
        weibo_url = 'http://weibo.cn/u/' + str(self.uid)
        weibo_list = []
        weibo_count = 0
        page_count = 1
        now_page_count = 1
        is_first = True
        pattern = re.compile(r'\d+')
        while True:

            tt.sleep(time_delay)
            # 获取页面源码(bs4对象)
            requests_content = self.retry_requests(weibo_url, uid=self.uid)

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
                weibo = SinaWeibo(uid=weibo_uid)
                weibo.text = i.div.span.get_text()
                weibo.uid = weibo_uid
                weibo.attitude_count = int(re.findall(pattern, i.div.find_all('a')[-4].get_text())[0])
                weibo.repost_count = int(re.findall(pattern, i.div.find_all('a')[-3].get_text())[0])
                weibo.comment_count = int(re.findall(pattern, i.div.find_all('a')[-2].get_text())[0])
                weibo.time = i.div.find_all('span', attrs={'class': 'ct'})[0].get_text().split('来自')[0]
                weibo.terminal_source = i.div.find_all('span', attrs={'class': 'ct'})[0].get_text().split('来自')[1]
                # 计数器加一
                weibo_count += 1
                # 若超过了要求获取的用户数量，则返回
                if weibo_count > required_weibo_count:
                    return weibo_list
                weibo_list.append(weibo)

            # 若是第一页，则获取总页数
            if is_first:
                # 若发现‘x/y页’ 则有不止一页
                if requests_content.find(attrs={'id': 'pagelist'}):
                    page_count = requests_content.find(attrs={'id': 'pagelist'}).form.div.contents[-1].strip()
                    page_count = page_count.split('/')[1]
                    page_count = int(re.findall(pattern, page_count)[0])
                    print(page_count)
                else:
                    return weibo_list
                is_first = False

            now_page_count += 1
            if now_page_count >= page_count:
                break

            weibo_url = 'http://weibo.cn/u/' + str(self.uid) + '?page=' + str(page_count)

        return weibo_list

