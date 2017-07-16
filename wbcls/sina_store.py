# coding=utf-8
from __future__ import unicode_literals, print_function
import pymongo
from base import SinaBaseObject
import people
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# 类转化为字典
def class_to_dict(obj):
    is_list = obj.__class__ == [].__class__
    is_set = obj.__class__ == set().__class__

    if is_list or is_set:
        obj_arr = []
        for o in obj:
            dict1 = {}
            dict1.update(o.__dict__)
            obj_arr.append(dict1)
        return obj_arr
    else:
        dict1 = {}
        dict1.update(obj.__dict__)
        return dict1


class SinaStore(SinaBaseObject):
    def __init__(self):
        super(SinaStore, self).__init__()
        self.is_first = True

        self.mongo_client = pymongo.MongoClient('localhost', 27017)
        self.db = self.mongo_client['Weibo']
        self.weibo_table = self.db['try3']

    # 递归分解传入的类 直至到原子项
    def analyze_data(self, data, dict0={}):

        if isinstance(data, list):
            for _item in data:
                self.analyze_data(_item)
        elif hasattr(data, '__dict__'):
            for name, value in vars(data).items():
                try:
                    dict0[name] = ''
                    self.analyze_data(value, dict0=dict0[name])
                except:
                    pass
        else:
            pass
        return data

    def store_in_mongodb(self, data):
        result = {}
        # 存储新浪用户类
        if isinstance(data, sina_people.SinaPeople):
            for name, value in vars(data).items():
                if unicode(name) != unicode('weibo_list'):
                    if not isinstance(value, list):
                        result[str(name)] = str(value)
                    else:
                        result[str(name)] = {}
                        for index, item in enumerate(value):
                            result[str(name)][str(index)] = {}
                            for name2, value2 in item.items():
                                result[str(name)][str(index)][str(name2)] = str(value2)
                else:
                    result[str(name)] = {}
                    print(type(value))
                    for index0, item0 in enumerate(value):
                        result[str(name)][str(index0)] = {}
                        for name2, value2 in vars(item0).items():
                            if not isinstance(value2, list):
                                result[str(name)][str(index0)][str(name2)] = str(value2)
                            else:
                                for index, item in enumerate(value2):
                                    result[str(name)][str(index0)][str(name2)] = {}
                                    result[str(name)][str(index0)][str(name2)][str(index)] = {}
                                    for name3, value3 in item.items():
                                        result[str(name)][str(index0)][str(name2)][str(index)][str(name3)] = str(value3)

        # 存储新浪微博类
        elif isinstance(data, sina_weibo.SinaWeibo):
            for name, value in vars(data).items():
              #  print(name, type(value))
                if not isinstance(value, list):
                    result[str(name)] = str(value)
                else:
                    result[str(name)] = {}
                    for index, item in enumerate(value):
                       # print(index, type(item))
                        result[str(name)][str(index)] = {}
                        for name2, value2 in item.items():
                            result[str(name)][str(index)][str(name2)] = str(value2)

        elif isinstance(data, dict):
            result = data
        else:
            raise TypeError+"非法类型！"

        self.weibo_table.insert_one(result)

    def get_human_info(self):
        for data in self.weibo_table.find():
            yield data

    def get_stored_information(self):
        for data in self.weibo_table.find():
            yield data










