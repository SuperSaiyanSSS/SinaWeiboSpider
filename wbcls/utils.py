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

