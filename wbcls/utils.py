# coding=utf-8
from __future__ import unicode_literals, print_function
from bs4 import BeautifulSoup
import functools
import importlib
import people


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

    本装饰器的作用为：

    1. 标识这个属性为常规属性。
    2. 自动从当前对象的数据中取出对应属性。
       优先返回缓存中的数据。
    :param name_in_json: 要查找的属性在`self._cache`这个json中的名字
                         默认值为使用此装饰器的方法名。
    """
    def actual_decorator(func):
        @functools.wraps(func)
        def inner(self, *args, **kwargs):
            name = name_in_json or func.__name__
            if self._cache and name in self._cache.keys():
                return self._cache[name]
            else:
                value = func(self, *args, **kwargs)
                self._cache.setdefault(name, value)
                return self._cache[name]
        return inner
    return actual_decorator


def other_obj(class_name=None, name_in_json=None, module_filename=None):
    """

    本装饰器的作用为：

    1. 标识这个属性为另一个父类为base类的对象。
    2. 自动从当前对象的数据中取出对应属性，构建成所需要的对象。
    :param class_name: 要生成的对象类名。
    :param name_in_json: 属性在 JSON 里的键名。
    :param module_filename: <class_name> 所在的模块的文件名。
    """
    def actual_decorator(func):
        @functools.wraps(func)
        def inner(self, *args, **kwargs):
            cls_name = class_name or func.__name__
            name = name_in_json or func.__name__

            obj_cls = get_class_from_name(cls_name, module_filename)

            request_obj = func(self, *args, **kwargs)
     #       print(111111111111)
    #        print(request_obj)

            if request_obj is None:
                if name == 'people':
                    return obj_cls(self.author_uid, cache={'name': self.author_name})
            # if name == 'weibo':
            #     return obj_cls(uid=self.now_weibo_uid, cache=self.now_weibo_cache)
            return request_obj

        return inner

    return actual_decorator


def get_class_from_name(clsname=None, module_filename=None):
    """

    接收类名，通过处理返回对应的类

    :param clsname: 类名
    :param module_filename: 模块名
    :return: 模块中对应传入类名的类
    """
    cls_name = clsname.capitalize() if clsname.islower() else clsname
    file_name = module_filename or cls_name.lower()

    # 获取引用的模块 如 `<module 'wbcls.people' from 'H:\py\workplace\git_sina\real\SinaWeiboSpider\wbcls\people.pyc'>`
    imported_module = importlib.import_module('.'+file_name, 'wbcls')
    #  print(imported_module)
    #  print(getattr(imported_module, cls_name))
    # 返回模块中对应传入类名的类 如 `<class 'wbcls.people.People'>`
    return getattr(imported_module, cls_name)
    # except (ImportError, AttributeError):
    #     raise TypeError(
    #         'Unknown weibo obj type [{}]'.format(clsname)
    #     )
