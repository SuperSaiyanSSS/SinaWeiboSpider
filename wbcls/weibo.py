# coding=utf-8

from __future__ import unicode_literals, print_function
import time as tt
import bs4
from bs4 import BeautifulSoup
import re
import requests
from base import SinaBaseObject
import sys
import people
reload(sys)
sys.setdefaultencoding('utf-8')
from utils import *

pattern = re.compile(r'\d+')


class Weibo(SinaBaseObject):
    """
    新浪微博的微博类
    {
        uid: F0Mg7a8Wh,
        author_uid: rmrb,
        is_repost: False,
        href: http://weibo.cn/comment/F0Mg7a8Wh,
        text: :【中国大学教学质量排行榜800强出炉！你的母校排多少？】近日，《2017中国大学评价研究报告》发布2017中国大学
              教学质量排行榜。清华大学本科生和研究生教育教学和人才培养质量问鼎榜首，北大第2，复旦第3，南大第4，武大第5，
              上海交大第6，浙大第7，人大第8，吉大第9，川大第10。戳↓你的学校第几名？ ​​​  [组图共9张]
        time: 04月29日 12:58,
        time_delay: 1,
        author_name: 人民日报,
        repost_count: 3910,
        attitude_count: 3076,
        comment_count: 3248,
        repost_list:
            [
                {
                    u'text': ':',
                    u'name': u'\u56db\u5ddd\u5927\u5b66'
                },
                {
                    u'text': ':27[\xe6\x91\x8a\xe6\x89\x8b][\xe5\xbf\x83] //',
                    u'name': u'\u674e\u5199\u610f'},
                {
                    u'text': ':\xe5\xa4\xaa\xe6\x83\xa8\xe4\xba\x86\xef\xbc\x8c\xe5\x89\x8d56\
                    xe4\xb8\xaa\xe9\x83\xbd\xe6\x98\xaf\xe4\xb8\x96\xe7\x95\x8c\xe7\x9f\xa5\xe5\x90\x8d... //',
                    u'name': u'\u897f\u8d22\u975e\u5b98\u65b9\u65b0\u95fb\u4e2d\u5fc3'
                },
                ....
            ]
        comment_list:
            [
                {
                    uid: C_4101856898497093,
                    terminal_source: iPhone 6s,
                    text: \u4eba\u6c11\u65e5\u62a5\u4e5f\u53d1\u8fd9\u79cd\u5546\u4e1a\u6027\u8d28\u7684\u5927\u5b66
                        \u6392\u884c\u699c\u3002\u3002\u3002[\u62dc\u62dc][\u62dc\u62dc][\u62dc\u62dc]',
                    time: 04\u670829\u65e5 13:05\xa0,
                    attitude_count: 270,
                    is_hot: True,
                    name: M-never
                },
                ....
            ]
        hot_comment_list:
            [
                {
                    uid: C_4101856898497093,
                    terminal_source: iPhone 6s,
                    text: \u4eba\u6c11\u65e5\u62a5\u4e5f\u53d1\u8fd9\u79cd\u5546\u4e1a\u6027\u8d28\u7684\u5927\u5b66
                        \u6392\u884c\u699c\u3002\u3002\u3002[\u62dc\u62dc][\u62dc\u62dc][\u62dc\u62dc]',
                    time: 04\u670829\u65e5 13:05\xa0,
                    attitude_count: 270,
                    is_hot: True,
                    name: M-never
                },
                ....
            ]
        attitude_list:
            [
                {
                    name: \u723d\u5cf0\u4e2b\u4e2b,
                    time: 13\u5206\u949f\u524d
                },
                {
                    name: \u8393\u5c7f,
                    time: \u4eca\u5929 19:55
                },
                ....
            ]

    """
    def __init__(self, id, session=None, cache={}, text='', time='', required_count=0):
        super(Weibo, self).__init__()
        self.uid = id
        self._cache = cache
        self._session = session
        self.href = 'http://weibo.cn/comment/'+str(id)
        self.main_page_resource = ''
        self.__get_author_data__()
        # 作者信息
     #   self.author_name = ''
    #    self.author_uid = ''
        # 评论
#        self.comment_count = 0
        self.comment_list = []
        self.hot_comment_list = []
        # 赞
   #     self.attitude_count = 0
        self.attitude_list = []
        # 转发
     #   self.repost_count = 0
        self.repost_list = []
        # 该微博是否为转发
        self.is_repost = False
        # 该微博转发的微博的信息
        self.repost_location = ''
        self.repost_author_uid = ''
        self.repost_text = ''
        self.repost_reposted_count = 0

#        self.text = text
  #      self.time = time
        self.terminal_source = ''
        self.location = ''

        # 威胁程度
        self.threatened = 0

        if required_count != 0:
            self.get_text()
            #self.comment_list = self.get_comment_list(required_comment_count=required_count)
           # self.get_hot_comment_list()
            #self.attitude_list = self.get_attitude_list(required_attitude_count=required_count)
           # self.attitude_list = self.attitude_list[1:]
           # self.repost_list = self.get_repost_list(required_repost_count=required_count)
           # self.repost_list = self.repost_list[1:]


    @property
    @normal_attr()
    def html(self):
        return self._session.get('http://weibo.cn/repost/' + self.uid).content

    @property
    @normal_attr()
    def _soup(self):
        return BeautifulSoup(self.html, "lxml")

    @property
    @other_obj(name_in_json='people', class_name='people')
    def author(self):
        return None

    @property
    @normal_attr()
    def time(self):
        return self._soup.find(attrs={'id': 'M_'}).findAll('div')[1].span.get_text()

    @property
    @normal_attr()
    def text(self):
        """
        微博文本
        """
        if not self._soup.find(attrs={'id': 'M_'}):
            raise AttributeError("cookies失效或网络故障！")
        return self._soup.find(attrs={'id': 'M_'}).div.span.get_text()

    @property
    @normal_attr()
    def repost_count(self):
        """
        :return:int 转发数
        """
        # wap版的微博页面，此页面内容格式特别不规范
        repost_number_node = self._soup.find(attrs={'id': 'rt'})
        try:
            repost_count = int(re.findall(pattern, repost_number_node.get_text())[0])
        except IndexError:
            print("获取转发数出错")
            repost_count = 0
        return repost_count

    @property
    @normal_attr()
    def comment_count(self):
        """
        :return:int 评论数
        """
        # wap版的微博页面，此页面内容格式特别不规范
        try:
            comment_number_node = self._soup.find(attrs={'id': 'rt'}).next_sibling
            comment_count = int(re.findall(pattern, comment_number_node.get_text())[0])
        except IndexError:
            print("获取评论数出错")
            comment_count = 0
        return comment_count

    @property
    @normal_attr()
    def attitude_count(self):
        # wap版的微博页面，此页面内容格式特别不规范
        try:
            attitude_number_node = self._soup.find(attrs={'id': 'rt'}).next_sibling.next_sibling
            attitude_count = int(re.findall(pattern, attitude_number_node.get_text())[0])
        except IndexError:
            print("获取点赞数出错")
            attitude_count = 0
        return attitude_count

    # def get_text(self):
    #     """
    #     获取微博内容
    #     :return: str类型的微博文本内容
    #     """
    #  #   if self.text != '':
    #   #      return self.text
    #     if 1:
    #         _retry_count = 3
    #         while _retry_count > 0:
    #             requests_content = self._soup
    #             self.main_page_resource = requests_content
    #             print(requests_content)
    #             print("测试session的get方法")
    #             try:
    #                 self.text = requests_content.find(attrs={'id': 'M_'}).div.span.get_text()
    #                 self.__get_author_data__()
    #                 _retry_count -= 1
    #                 break
    #             except AttributeError:
    #                 _retry_count -= 1
    #
    #         # 微博属性（转发数、赞数、评论数）
    #         # wap版的此内容格式特别不规范
    #         repost_number_node = requests_content.find(attrs={'id': 'rt'})
    #         try:
    #             self.repost_count = int(re.findall(pattern, repost_number_node.get_text())[0])
    #         except IndexError:
    #             self.repost_count = 0
    #         try:
    #             comment_number_node = repost_number_node.next_sibling
    #             self.comment_count = int(re.findall(pattern, comment_number_node.get_text())[0])
    #         except IndexError:
    #             self.comment_count = 0
    #         try:
    #             attitude_number_node = comment_number_node.next_sibling
    #             self.attitude_count = int(re.findall(pattern, attitude_number_node.get_text())[0])
    #         except IndexError:
    #             self.attitude_count = 0
    #
    #         # 微博发表时间
    #         #self.time = requests_content.find(attrs={'id': 'M_'}).findAll('div')[1].span.get_text()
    #         return self.text

    # 获取微博作者的昵称和uid
    def __get_author_data__(self):
        self.author_name = self._soup.find(attrs={'id': 'M_'}).div.a.get_text()
        self._cache.setdefault('author_name', self.author_name)
        self.author_uid = self._soup.find(attrs={'id': 'M_'}).div.a.attrs['href'].split('/')[-1]
        self._cache.setdefault('author_uid', self.author_uid)

    def __get_attribute_list__(self, target_attribute_type, target_attribute_fuction, required_attribute_count=8):
        """

        :param target_attribute_type:
        :param target_attribute_fuction:
        :param required_attribute_count:
        :return:
        """
        attribute_url = 'http://weibo.cn/' + str(target_attribute_type) + '/' + str(self.uid)
        attribute_list = []
        attribute_count = 0
        page_count = 1
        now_page_count = 1
        is_first = True
        pattern = re.compile(r'\d+')
        while True:
            print("现在是评论第一页")
            tt.sleep(self.time_delay)
            # 获取页面源码(bs4对象)
            requests_content = self.retry_requests(attribute_url, uid=self.uid)

            # 获取当前页的关注列表
            unit_list = requests_content.find_all('div', attrs={'class': 'c'})
            for i in unit_list:
                # 调用具体函数提取内容
                attribute = target_attribute_fuction(i)
                if attribute is False:
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

    def _get_attribute_item(self, target_attribute_type, target_attribute_fuction):
        """

        :param target_attribute_type:
        :param target_attribute_fuction:
        :param required_attribute_count:
        :return:
        """
        attribute_url = 'http://weibo.cn/' + str(target_attribute_type) + '/' + str(self.uid)
        attribute_list = []
        page_count = 1
        now_page_count = 1
        is_first = True
        pattern = re.compile(r'\d+')
        while True:
            print("现在是评论第一页")
            tt.sleep(self.time_delay)
            # 获取页面源码(bs4对象)
            requests_content =BeautifulSoup(self._session.get(attribute_url).content)

            # 获取当前页的关注列表
            unit_list = requests_content.find_all('div', attrs={'class': 'c'})
            for i in unit_list:
                # 调用具体函数提取内容
                attribute = target_attribute_fuction(i)
                if attribute is False:
                    continue
                yield attribute

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
            if now_page_count >= page_count:
                return

            attribute_url = 'http://weibo.cn/' + str(target_attribute_type) +'/' + str(self.uid) +'?&&page=' + \
                            str(now_page_count)

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
        comment['author_uid'] = str(str(unit.a.attrs['href']).split('/')[-1])
        # 有的用户是个性域名，不符合/u/‘uid’的特点，故同时存href
      #  comment['people'] = sina_people.SinaPeople(uid=str(unit.a.attrs['href']).split('/')[-1],
                               #        href='http://http://weibo.cn'+str(unit.a.attrs['href']))
        # 检查是否有“热门”标签
        try:
            if str(unit.span.attrs['class']) == "['kt']":
                comment['is_hot'] = True
            else:
                comment['is_hot'] = False
        except:
            comment['is_hot'] = False
        # 正则匹配获取评论的赞数
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

    @property
    def comment(self):
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
        for x in self._get_attribute_item('comment', self.__get_comment_list__):
            yield x

        #self.comment_list = self.__get_attribute_list__('comment', self.__get_comment_list__, required_attribute_count=
#                                                        required_comment_count)
     #   return self.comment_list

    # # 获取热门评论
    # def get_hot_comment_list(self):
    #     for i in self.comment_list:
    #         if i['is_hot']:
    #             self.hot_comment_list.append(i)
    #     return self.hot_comment_list

    @staticmethod
    def __get_attitude_list__(unit):
        attitude = {}
        # 若有a标签则为点赞的unit
        try:
            attitude['name'] = unit.a.get_text()
            attitude['time'] = unit.span.get_text()
           # attitude['people'] = SinaPeople(uid=str(unit.a.attrs['href']).split('/')[-1],
                                           # href='http://weibo.cn' + str(unit.a.attrs['href']))
        except AttributeError:
            return False
        return attitude

    def get_attitude_list(self, required_attitude_count=5):
        self.attitude_list = self.__get_attribute_list__('attitude', self.__get_attitude_list__,
                                                         required_attribute_count=required_attitude_count)
        return self.attitude_list

    @staticmethod
    def __get_repost_list__(unit):
        repost = {}
        try:
            repost['name'] = unit.a.get_text()
            tmp_slibing = unit.a.next_sibling
            while not isinstance(tmp_slibing, bs4.element.NavigableString):
                tmp_slibing = tmp_slibing.next_sibling
            repost['text'] = str(tmp_slibing)
     #       repost['people'] = SinaPeople(uid=unit.a.attrs['href'].split('/')[-1],
               #                           href='http://weibo.cn/'+unit.a.attrs['href'])
        except:
            return False
        return repost

    def get_repost_list(self, required_repost_count=5):
        self.repost_list = self.__get_attribute_list__('repost', self.__get_repost_list__,
                                                       required_attribute_count=required_repost_count)
        return self.repost_list

if __name__ == '__main__':
    def a():
        return 1
    print(type(a))