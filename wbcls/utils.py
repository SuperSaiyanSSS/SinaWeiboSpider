# coding=utf-8
from __future__ import unicode_literals, print_function
from bs4 import BeautifulSoup
import functools


def check_cache(attr):
    def real(func):
        @functools.wraps(func)
        def wrapper(self):
            value = getattr(self, attr, None)
            if not value:
                value = func(self)
                setattr(self, attr, value)
            return value
        return wrapper
    return real


def normal_attr(name_in_json=None):
    """
    一般属性获取的装饰器
    优先返回缓存中的数据
    :param name_in_json: 要查找的属性在`self._cache`这个json中的名字
                         默认值为使用此装饰器的方法名。
    :return: 属性值
    """
    def actual_decorator(func):
        @functools.wraps(func)
        def inner(self, *args, **kwargs):
            name = name_in_json or func.__name__
            if self._cache:
                if name in self._cache.keys():
                    return self._cache[name]
            else:
                return func(self, *args, **kwargs)
        return inner
    return actual_decorator



