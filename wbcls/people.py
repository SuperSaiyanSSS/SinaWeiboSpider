# coding=utf-8
from __future__ import unicode_literals, print_function
import time as tt
import pymongo
from utils import *
from bs4 import BeautifulSoup
import re
import requests
import weibo
from base import SinaBaseObject
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
pattern = re.compile(r'\d+')


class People(SinaBaseObject):
    """
    新浪微博的用户类
    """
    def __init__(self, id, href=None, cache={}):
        """
        <a1.sina_people.SinaPeople object at 0x0000000003791C88>
        {
            uid: 5501547091,
            name: 助人为乐的英逸,
            fans_count: 285,
            follow_count: 1500,
            weibo_count: 1335,
            time_delay: 1,
            birthday: 未知,
            sex: 男,
            location: 江西,
            member_level: '',
            required_weibo_count: 2,
            required_member_count: 2,
            href: http://weibo.cn/5501547091/follow,
            fans_list: [
                    {
                        name: 03775177m,
                        uid: 3874404440,
                        fans_count: 9,
                        is_v: False,
                        href: http://weibo.cn/u/3874404440,
                    },
                     ....
                       ]
            follow_list: [
                    {
                        name: silent\u9ed8_7045,
                        uid: 5534114512,
                        fans_count: 12,
                        is_v: False,
                        href: http://weibo.cn/u/5534114512,
                    },
                    ....
                        ]
            weibo_list: [
                        <a1.sina_weibo.SinaWeibo object at 0x0000000003920FD0>,
                        <a1.sina_weibo.SinaWeibo object at 0x00000000039D38D0>,
                        ....
                        ]
        :param uid:
        :param href:
        """
        super(People, self).__init__()
        self.uid = str(id)
        self._cache = cache
        self.href = href
        self.birthday = '未知'
        self.member_level = ''
        self.follow_list = []
        self.fans_list = []
        self.is_V = False
        self.uid = self.uid.strip('\n')
        if not self.href:
            self.href = 'http://weibo.cn/'+self.uid
        if not self.uid:
            self.uid = self.href.split('cn/')

    @property
    def basic_url(self):
        return 'http://weibo.cn/u/' + str(self.uid)

    @property
    @normal_attr()
    def html(self):
        return self._session.get(self.href).content

    @property
    @normal_attr()
    def _soup(self):
        return BeautifulSoup(self.html, "lxml")

    @property
    @normal_attr()
    def _info_content(self):
        try:
            info_content = self._soup.find('div', attrs={'class': 'u'}).table.tr.findAll('td'
                                                                                               )[1].div.span.contents[0]
        except AttributeError:
            return False
        return info_content

    @property
    @normal_attr()
    def _info_content_2(self):
        """
        若用户为大V 则有大V标志的图片 影响页面标签
        故此时个人信息页面块实际为`_info_content_2`
        """
        return self._soup.find('div', attrs={'class': 'u'}).table.tr.findAll('td')[1].div.span.get_text()

    @property
    @normal_attr()
    def name(self):
        return self._info_content.split(' ')[0].strip()

    @property
    @normal_attr()
    def sex(self):
        try:
            sex = self._info_content.split(' ')[1].split('/')[0].strip()
        except IndexError:
            sex = self._info_content_2.split('/')[0].strip()[-1:].strip()
        return sex

    @property
    @normal_attr()
    def location(self):
        try:
            location = self._info_content.split(' ')[1].split('/')[1].strip()
        except IndexError:
            # 将大V标志为真
            self.is_V = True
            location = self._info_content_2.split('/')[1].strip()[:3].strip()
        return location

    @property
    @normal_attr()
    def weibo_count(self):
        print(self._soup)
        print(self.href)
        return int(re.findall(pattern, self._soup.find('div', attrs={'class': 'u'}).
                              findAll('div', attrs={'class': 'tip2'})[0].get_text())[0])

    @property
    @normal_attr()
    def follow_count(self):
        return int(re.findall(pattern, self._soup.find('div', attrs={'class': 'u'}).
                              findAll('div', attrs={'class': 'tip2'})[0].get_text())[1])

    @property
    @normal_attr()
    def fans_count(self):
        return int(re.findall(pattern, self._soup.find('div', attrs={'class': 'u'}).
                              findAll('div', attrs={'class': 'tip2'})[0].get_text())[2])

    def _get_member_list(self, target_member_type):
        """
        获取所指定的当前用户的关注/粉丝列表
        每个被关注者或粉丝的信息存储在dict中
        :param required_member_count: 指定获取用户的数量
        :param time_delay: 延迟时间
        :param target_member_type: 指定获取用户的种类：fans或follow
        :return: member_list: 存放已获取的用户列表

        """
        # TODO: 获取人物基本信息
        member_url = 'http://weibo.cn/' + str(self.uid) + '/' + str(target_member_type)
        self.href = member_url
        print(member_url)
        page_count = 1
        now_page_count = 1
        is_first = True
        while True:

            tt.sleep(self.time_delay)
            # 获取页面源码(bs4对象)
            requests_content = BeautifulSoup(self._session.get(member_url).content, "lxml")

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

                yield member

            # 若是第一页，则获取总页数
            if is_first is True:
                # 若发现‘x/y页’ 则有不止一页
                if requests_content.find(attrs={'id': 'pagelist'}):
                    page_count = requests_content.find(attrs={'id': 'pagelist'}).form.div.contents[-1].strip()
                    page_count = page_count.split('/')[1]
                    pattern = re.compile(r'\d+')
                    page_count = int(re.findall(pattern, page_count)[0])
                    print(page_count)
                else:
                    return
                is_first = False

            now_page_count += 1
            if now_page_count >= page_count:
                return

            member_url = 'http://weibo.cn/' + str(self.uid)+'/'+str(target_member_type)+'?page=' + str(now_page_count)
            print(member_url)
            print(self.uid)
            print(target_member_type)
            print("以上")

    @property
    @normal_attr()
    def fans(self):
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
        for x in self._get_member_list(target_member_type='fans'):
            yield x

    @property
    @normal_attr()
    def follow(self):
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
        for x in self._get_member_list(target_member_type='follow'):
            yield x

    @property
    @other_obj()
    def weibo(self):
        """
        获取指定用户的微博
        :param required_weibo_count: 所需的微博条数
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
        page_count = 1
        now_page_count = 1
        is_first = True
        pattern = re.compile(r'\d+')

        while True:
            tt.sleep(self._time_delay)
            # 获取页面源码(bs4对象)
            requests_content = BeautifulSoup(self._session.get(weibo_url).content, "lxml")
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

                # 检查是否为转发的微博
                if len(i.div.find_all('span')) >= 2:
                    is_repost = True
                else:
                    is_repost = False
                # for c in i.div.find_all('span'):
                #     if str(c.attrs['class']) == "['cmt']":
                #         is_repost = True
                if is_repost:
                    text = i.div.find_all('span')[0].get_text()+i.div.find_all('span')[1].get_text()
                else:
                    text = i.div.span.get_text()

                # 有的微博处html格式不对
                try:
                    attitude_count = int(re.findall(pattern, i.div.find_all('a')[-4].get_text())[0])
                    repost_count = int(re.findall(pattern, i.div.find_all('a')[-3].get_text())[0])
                    comment_count = int(re.findall(pattern, i.find_all('div')[-1].find_all('a')[-2].get_text())[0])
                except IndexError:
                    print(weibo_uid)
                    try:
                        comment_count = int(re.findall(pattern, i.find_all('div')[-1].find_all('a')[-3].get_text())[0])
                        repost_count = int(re.findall(pattern, i.find_all('div')[-1].find_all('a')[-4].get_text())[0])
                        attitude_count = int(re.findall(pattern, i.find_all('div')[-1].find_all('a')[-5].get_text())[0])
                    except IndexError:
                        attitude_count = int(re.findall(pattern, i.find_all('div')[-1].get_text())[0])
                        repost_count = int(re.findall(pattern, i.find_all('div')[-1].get_text())[1])
                        comment_count = int(re.findall(pattern, i.find_all('div')[-1].get_text())[2])
                        print(attitude_count, repost_count, comment_count)
                try:
                    time = i.find_all('div')[-1].find_all('span', attrs={'class': 'ct'})[0].get_text().split('来自')[0]
                    terminal_source = i.div.find_all('span', attrs={'class': 'ct'})[0].get_text().split('来自')[1]
                except IndexError:
                    print(i.find_all('div')[-1].find_all('span', attrs={'class': 'ct'})[0].get_text())
                    time = i.find_all('div')[-1].find_all('span', attrs={'class': 'ct'})[0].get_text().split('来自')[0]
                    try:
                        terminal_source = i.find_all('div')[-1].find_all('span', attrs={'class': 'ct'})[0].get_text().split('来自')[1]
                    except IndexError:
                        terminal_source = '暂无'
                print(time, terminal_source)
                weibo_cache = {
                    "is_repost": is_repost,
                    "text": text,
                    "attitude_count": attitude_count,
                    "repost_count": repost_count,
                    "comment_count": comment_count,
                    "time": time,
                    "terminal_source": terminal_source
                }
                print(5555555555555555555555555555555)
                print(weibo_uid)
                self.now_weibo_cache = weibo_cache
                self.now_weibo_uid = weibo_uid
                yield weibo.Weibo(id=weibo_uid, cache=weibo_cache)
            is_repost = False

            # 若是第一页，则获取总页数
            if is_first:
                # 若发现‘x/y页’ 则有不止一页
                if requests_content.find(attrs={'id': 'pagelist'}):
                    page_count = requests_content.find(attrs={'id': 'pagelist'}).form.div.contents[-1].strip()
                    page_count = page_count.split('/')[1]
                    page_count = int(re.findall(pattern, page_count)[0])
                    print(page_count)
                else:
                    return
                is_first = False

            now_page_count += 1
            if now_page_count > page_count:
                return

            weibo_url = 'http://weibo.cn/u/' + str(self.uid) + '?page=' + str(now_page_count)

    # def get_weibo_list(self):
    #     """
    #     获取指定用户的微博
    #     :param required_weibo_count: 所需的微博条数
    #     :param time_delay: 时间延迟
    #     :return: weibo_list 元素为SinaWeibo对象
    #         ..  code-block:: python
    #         [
    #             {
    #                 'uid': 'EpO2KnAor',
    #                 'is_repost': False,
    #                 'text': '物是人非.',
    #                 'attitude_count' : 0,
    #                 'repost_count': 7,
    #                 'comment_count': 0,
    #                 'time': '01月08日 04:44'
    #                 'terminal_source': 'iPad mini'
    #             },
    #             {
    #                 'uid': 'EAJwkph8X',
    #                 'is_repost': False,
    #                 'text': '祝你生日快乐',
    #                 'attitude_count' : 0,
    #                 'repost_count': 0,
    #                 'comment_count': 1,
    #                 'time': '2016-12-30 23:34:34'
    #                 'terminal_source': '生日动态'
    #             },
    #         ]
    #     """
    #     required_weibo_count = self.required_weibo_count
    #     weibo_url = self.basic_url
    #     weibo_list = []
    #     weibo_count = 0
    #     page_count = 1
    #     now_page_count = 1
    #     is_first = True
    #     pattern = re.compile(r'\d+')
    #     while True:
    #
    #         tt.sleep(self.time_delay)
    #         # 获取页面源码(bs4对象)
    #         requests_content = self.retry_requests(weibo_url, uid=self.uid)
    #
    #         # 获取当前页的微博列表
    #         unit_list = requests_content.find_all('div', attrs={'class': 'c'})
    #         for i in unit_list:
    #             # 每个微博的信息以微博类SinaWeibo存储
    #             try:
    #                 if str(i.attrs['id']) and str(i.attrs['id']).startswith('M'):
    #                     weibo_uid = i.attrs['id'].split('_')[1]
    #                 else:
    #                     continue
    #             except:
    #                 continue
    #             weibo = sina_weibo.SinaWeibo(uid=weibo_uid, required_count=0)
    #
    #             # 检查是否为转发的微博
    #             for c in i.div.find_all('span'):
    #                 if str(c.attrs['class']) == "['cmt']":
    #                     weibo.is_repost = True
    #             if weibo.is_repost:
    #                 weibo.text = i.div.find_all('span')[0].get_text()+i.div.find_all('span')[1].get_text()
    #             else:
    #                 weibo.text = i.div.span.get_text()[1:]
    #
    #             weibo.uid = weibo_uid
    #
    #             # 有的微博处html格式不对
    #             try:
    #                 weibo.attitude_count = int(re.findall(pattern, i.div.find_all('a')[-4].get_text())[0])
    #                 weibo.repost_count = int(re.findall(pattern, i.div.find_all('a')[-3].get_text())[0])
    #                 weibo.comment_count = int(re.findall(pattern, i.find_all('div')[-1].find_all('a')[-2].get_text())[0])
    #             except IndexError:
    #                 print(weibo_uid)
    #                 print(weibo.author_uid)
    #                 try:
    #                     weibo.comment_count = int(re.findall(pattern, i.find_all('div')[-1].find_all('a')[-3].get_text())[0])
    #                     weibo.repost_count = int(re.findall(pattern, i.find_all('div')[-1].find_all('a')[-4].get_text())[0])
    #                     weibo.attitude_count = int(re.findall(pattern, i.find_all('div')[-1].find_all('a')[-5].get_text())[0])
    #                 except IndexError:
    #                     weibo.attitude_count = int(re.findall(pattern, i.find_all('div')[-1].get_text())[0])
    #                     weibo.repost_count = int(re.findall(pattern, i.find_all('div')[-1].get_text())[1])
    #                     weibo.comment_count = int(re.findall(pattern, i.find_all('div')[-1].get_text())[2])
    #                     print(weibo.attitude_count, weibo.repost_count, weibo.comment_count)
    #             try:
    #                 weibo.time = i.find_all('div')[-1].find_all('span', attrs={'class': 'ct'})[0].get_text().split('来自')[0]
    #                 weibo.terminal_source = i.div.find_all('span', attrs={'class': 'ct'})[0].get_text().split('来自')[1]
    #             except IndexError:
    #                 print(i.find_all('div')[-1].find_all('span', attrs={'class': 'ct'})[0].get_text())
    #                 weibo.time = i.find_all('div')[-1].find_all('span', attrs={'class': 'ct'})[0].get_text().split('来自')[0]
    #                 try:
    #                     weibo.terminal_source = i.find_all('div')[-1].find_all('span', attrs={'class': 'ct'})[0].get_text().split('来自')[1]
    #                 except IndexError:
    #                     weibo.terminal_source = '暂无'
    #             print(weibo.time, weibo.terminal_source)
    #             # 计数器加一
    #             weibo_count += 1
    #             # 若超过了要求获取的用户数量，则返回
    #             if weibo_count > required_weibo_count:
    #                 return weibo_list
    #             weibo_list.append(weibo)
    #
    #         # 若是第一页，则获取总页数
    #         if is_first:
    #             # 若发现‘x/y页’ 则有不止一页
    #             if requests_content.find(attrs={'id': 'pagelist'}):
    #                 page_count = requests_content.find(attrs={'id': 'pagelist'}).form.div.contents[-1].strip()
    #                 page_count = page_count.split('/')[1]
    #                 page_count = int(re.findall(pattern, page_count)[0])
    #                 print(page_count)
    #             else:
    #                 return weibo_list
    #             is_first = False
    #
    #         now_page_count += 1
    #         if now_page_count > page_count:
    #             break
    #
    #         weibo_url = 'http://weibo.cn/u/' + str(self.uid) + '?page=' + str(now_page_count)
    #
    #     return weibo_list

    # def get_personal_information(self):
    #     """
    #     注：新浪有奇怪的BUG 带cookies访问http://weibo.cn/3193031501/info这类个人资料url时，总是File not found
    #         若不带cookies则不能访问该页
    #         所以只能获取个人主页简单的性别和地点信息
    #
    #         @2017/06/12：
    #             新浪允许不带cookie访问某些页面，如某个微博页面
    #             而对另一些页面 如个人主页的详细情况，则有的用户需要cookie，有的不需要。
    #     :return:
    #     """
    #     requests_content = self.retry_requests(self.href)
    #     try:
    #         info_content = requests_content.find('div', attrs={'class': 'u'}).table.tr.findAll('td')[1].div.span.contents[0]
    #     except AttributeError:
    #         print(requests_content)
    #         return False
    #     # 此处split(' ')中的空格不是一般的空格 需要在原网页中复制
    #     # 普通用户无图片标签
    #     self.name = info_content.split(' ')[0].strip()
    #     print(self.name)
    #     try:
    #         self.sex = info_content.split(' ')[1].split('/')[0].strip()
    #         print(self.sex)
    #         self.location = info_content.split(' ')[1].split('/')[1].strip()
    #         print(self.name, self.sex, self.location)
    #     except IndexError:
    #         self.is_V = True
    #         info2 = requests_content.find('div', attrs={'class': 'u'}).table.tr.findAll('td')[1].div.span.get_text()
    #         self.sex = info2.split('/')[0].strip()[-1:].strip()
    #         print(self.sex)
    #         self.location = info2.split('/')[1].strip()[:3].strip()
    #         print(self.name, self.sex, self.location)
    #
    #     # 获取该用户的微博数 关注数 粉丝数
    #     self.weibo_count = int(re.findall(pattern, requests_content.find('div', attrs={'class': 'u'}).
    #                                       findAll('div', attrs={'class': 'tip2'})[0].get_text())[0])
    #     self.follow_count = int(re.findall(pattern, requests_content.find('div', attrs={'class': 'u'}).
    #                                        findAll('div', attrs={'class': 'tip2'})[0].get_text())[1])
    #     self.fans_count = int(re.findall(pattern, requests_content.find('div', attrs={'class': 'u'}).
    #                                      findAll('div', attrs={'class': 'tip2'})[0].get_text())[2])
    #     print(self.weibo_count, self.follow_count, self.fans_count)

    # def __get_member_list__(self, target_member_type='fans'):
    #     """
    #     获取所指定的当前用户的关注/粉丝列表
    #     每个被关注者或粉丝的信息存储在dict中
    #     :param required_member_count: 指定获取用户的数量
    #     :param time_delay: 延迟时间
    #     :param target_member_type: 指定获取用户的种类：fans或follow
    #     :return: member_list: 存放已获取的用户列表
    #
    #
    #     """
    #     required_member_count = self.required_member_count
    #     member_url = 'http://weibo.cn/' + str(self.uid) + '/' + str(target_member_type)
    #     self.href = member_url
    #     print(member_url)
    #     member_list = []
    #     member_count = 0
    #     page_count = 1
    #     now_page_count = 1
    #     is_first = True
    #     while True:
    #
    #         tt.sleep(self.time_delay)
    #         # 获取页面源码(bs4对象)
    #         requests_content = self.retry_requests(member_url, uid=self.uid)
    #
    #         # 获取当前页的关注列表
    #         unit_list = requests_content.find_all('table')
    #         for i in unit_list:
    #             # 每个用户的信息以dict存储
    #             member = {}
    #             member['href'] = str(i.tr.td.a.attrs['href'])
    #             try:
    #                 member['uid'] = i.tr.td.a.attrs['href'].split('u/')[1]
    #             except:
    #                 member['uid'] = i.tr.td.a.attrs['href'].split('cn/')[1]
    #             member['name'] = i.tr.find_all('td')[1].a.get_text()
    #             # 正则匹配获取粉丝的粉丝数
    #             pattern = re.compile(r'\d+')
    #             # 若粉丝是大V，则多了一个图片标签
    #             try:
    #                 member['is_v'] = False
    #                 member['fans_count'] = int(re.findall(pattern, i.tr.find_all('td')[1].contents[2])[0])
    #             except:
    #                 member['fans_count'] = int(re.findall(pattern, i.tr.find_all('td')[1].contents[3])[0])
    #                 member['is_v'] = True
    #             print(member['name'])
    #             print(member['fans_count'])
    #             # 计数器加一
    #             member_count += 1
    #             # 若超过了要求获取的用户数量，则返回
    #             if member_count > required_member_count:
    #                 return member_list
    #             member_list.append(member)
    #
    #         # 若是第一页，则获取总页数
    #         if is_first is True:
    #             # 若发现‘x/y页’ 则有不止一页
    #             if requests_content.find(attrs={'id': 'pagelist'}):
    #                 page_count = requests_content.find(attrs={'id': 'pagelist'}).form.div.contents[-1].strip()
    #                 page_count = page_count.split('/')[1]
    #                 pattern = re.compile(r'\d+')
    #                 page_count = int(re.findall(pattern, page_count)[0])
    #                 print(page_count)
    #             else:
    #                 return member_list
    #             is_first = False
    #
    #         now_page_count += 1
    #         if now_page_count >= page_count:
    #             break
    #
    #         member_url = 'http://weibo.cn/' + str(self.uid)+'/'+str(target_member_type)+'?page=' + str(now_page_count)
    #         print(member_url)
    #         print(self.uid)
    #         print(target_member_type)
    #         print("以上")
    #
    #     return member_list