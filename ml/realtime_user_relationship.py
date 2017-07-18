# -*- coding: utf-8 -*
from __future__ import unicode_literals, print_function
from __future__ import division
import json
import csv
import pymongo
import requests
from bs4 import BeautifulSoup
import sys
sys.path.append("..")
# from a1 import base
# from a1 import sina_store
# from a1 import sina_weibo
# from a1 import sina_people
import fenci
reload(sys)
sys.setdefaultencoding('utf-8')


class RealtimeUserRealationship(object):
    KEY = '9LF3gnOtYENP26HSoNAxPptHk7eCgxdWjL5ZuSdJXuGALaAcTrLXdGI7TkEYnIQm'

    def __init__(self, user_id, fans=True, follow=False):
        self.fans_href = 'http://api03.bitspaceman.com:8000/profile/weibo?type=3&id='+str(user_id)+'&apikey=' + \
                         self.KEY + '&size=50'
        self.fans_list = []
        self.follow_href = 'http://api03.bitspaceman.com:8000/profile/weibo?type=2&id='+str(user_id)+'&apikey=' + \
                           self.KEY + '&size=50'
        self.follow_list = []
        self.get_relationship(fans=fans, follow=follow)

    def get_relationship(self, fans=True, follow=False):
        if fans:
            requests_get = requests.get(self.fans_href, timeout=15)
            requests_content = requests_get.content
            requests_dict = json.loads(requests_content)
            self.fans_list = self.parse_requests_dict(requests_dict)
            self.store_to_mongodb(self.fans_list, fans=fans, follow=follow)
        if follow:
            requests_get = requests.get(self.fans_href, timeout=15)
            requests_content = requests_get.content
            requests_dict = json.loads(requests_content)
            self.follow_list = self.parse_requests_dict(requests_dict)
            self.store_to_mongodb(self.fans_list, fans=fans, follow=follow)

    @staticmethod
    def parse_requests_dict(requests_dict):
        relationship_list = []
        for item in requests_dict['data']:
            user_id = str(item['id'])
            user = sina_people.SinaPeople(uid=user_id, lazy=True)
            try:
                user.name = str(item['userName'])
                print(user.name)
                user.fans_count = str(item['fansCount'])
                user.follow_count = str(item['followCount'])
                user.weibo_count = str(item['postCount'])
                user.location = str(item['location'])
                user.sex = str(item['gender'])
                print("粉丝数"+user.fans_count)
            except:
                continue

            relationship_list.append(user)

        return relationship_list

    @staticmethod
    def store_to_mongodb(user_list, fans=True, follow=False):
        sina_store_object = sina_store.SinaStore()
        if fans:
            sina_store_object.weibo_table = sina_store_object.db['realtime_user_fans']
            for user in user_list:
                sina_store_object.store_in_mongodb(user)
        if follow:
            sina_store_object.weibo_table = sina_store_object.db['realtime_user_follow']
            for user in user_list:
                sina_store_object.store_in_mongodb(user)