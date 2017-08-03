# coding=utf-8
from __future__ import unicode_literals, print_function
from utils import *
import weibo
from base import SinaBaseObject
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Repost(SinaBaseObject):
    """
    回复类，一般不直接使用，而是作为`Answer.repost`迭代器的返回类型
    """

    def __init__(self, id, cache={}):
        super(Repost, self).__init__()
        self.uid = str(id)
        self._cache = cache
        self.author_name = cache['author_name']
        self.text = cache['text']
