# coding=utf-8
from __future__ import unicode_literals, print_function
from utils import *
import weibo
from base import SinaBaseObject
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Comment(SinaBaseObject):
    """
    评论类，一般不直接使用，而是作为`Answer.comment`迭代器的返回类型
    """

    def __init__(self, id, cache={}):
        super(Comment, self).__init__()
        self.uid = str(id)
        self._cache = cache
        self.attitude_count = cache['attitude_count']
        self.author_name = cache['author_name']
        self.author_uid = cache['author_uid']
        self.content = cache['text']
        self.is_hot = cache['is_hot']
        self.terminal_source = cache['terminal_source']
        self.text = cache['text']
        self.time = cache['time']




    # @property
    # @normal_attr
    # def _soup(self):
    #     return self._cache['_soup']
    #
    # # 获取微博作者的昵称和uid
    # def _get_author_data(self):
    #     # self.author_name = self._soup.find(attrs={'id': 'M_'}).div.a.get_text()
    #     # self._cache.setdefault('author_name', self.author_name)
    #
    #     self.author_uid = self._soup.find(attrs={'id': 'M_'}).div.a.attrs['href'].split('/')[-1]
    #     self._cache.setdefault('author_uid', self.author_uid)
    #
    # @property
    # @other_obj(class_name='people', name_in_json='people')
    # def author(self):
    #     pass




