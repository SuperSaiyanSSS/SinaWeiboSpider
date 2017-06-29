# -*- coding: utf-8 -*
from __future__ import unicode_literals, print_function
from __future__ import division
import json
import time as tt
import csv
import pymongo
import requests
from bs4 import BeautifulSoup
import sys
sys.path.append("..")
from a1 import base
from a1 import sina_store
from a1 import sina_weibo
from a1 import sina_people
import fenci
reload(sys)
sys.setdefaultencoding('utf-8')


class RealtimeUserRealationship(object):
    KEY = '9LF3gnOtYENP26HSoNAxPptHk7eCgxdWjL5ZuSdJXuGALaAcTrLXdGI7TkEYnIQm'

    def __init__(self, user_id, user=True, fans=True, follow=True):
        self.fans_href = 'http://api03.bitspaceman.com:8000/profile/weibo?type=3&id='+str(user_id)+'&apikey=' + \
                         self.KEY + '&size=30'
        self.fans_list = []
        self.follow_href = 'http://api03.bitspaceman.com:8000/profile/weibo?type=2&id='+str(user_id)+'&apikey=' + \
                           self.KEY+'&size=30'
        self.follow_list = []

        self.user_href = 'http://api03.bitspaceman.com:8000/profile/weibo?type=1&'+str(user_id)+'&apikey=' + self.KEY
        self.info_dict = {}
        self.get_relationship(user=user, fans=fans, follow=follow)

    def get_relationship(self, user=True, fans=True, follow=False):

        if fans:
            requests_get = requests.get(self.fans_href, timeout=15)
            requests_content = requests_get.content
            requests_dict = json.loads(requests_content)
            self.fans_list = self.parse_requests_dict(requests_dict)
        tt.sleep(5)
        if follow:
            requests_get = requests.get(self.follow_href, timeout=15)
            requests_content = requests_get.content
            requests_dict = json.loads(requests_content)
            self.follow_list = self.parse_requests_dict(requests_dict)
        tt.sleep(5)

        if user:
            requests_get = requests.get(self.user_href, timeout=15)
            requests_content = requests_get.content
            requests_dict = json.loads(requests_content)
            self.info_dict = self.parse_requests_info_dict(requests_dict)


        self.store_to_mongodb()

    @staticmethod
    def parse_requests_dict(requests_dict):
        relationship_list = []
        for item in requests_dict['data']:
            user_id = str(item['id'])
            user = {}
            try:
                user['id'] = str(user_id)
                user['name'] = str(item['userName'])
                user['fans_count'] = str(item['fansCount'])
                user['follow_count'] = str(item['followCount'])
                user['weibo_count'] = str(item['postCount'])
                user['location'] = str(item['location'])
                user['sex'] = str(item['gender'])
                print("粉丝数"+user['fans_count'])
            except:
                continue

            relationship_list.append(user)

        return relationship_list

    def parse_requests_info_dict(self, requests_dict):
        info_dict = {}
        try:
            for item in requests_dict['data']:
                try:
                    info_dict['fans_count'] = str(item['fansCount'])
                    info_dict['follow_count'] = str(item['followCount'])
                    info_dict['weibo_count'] = str(item['postCount'])
                    info_dict['location'] = str(item['location'])
                    info_dict['name'] = str(item['userName'])
                    info_dict['url'] = str(item['url'])
                except:
                    continue
            info_dict['fans_list'] = self.fans_list
            info_dict['follow_list'] = self.follow_list
            return info_dict
        except:
            print(requests_dict)


    def store_to_mongodb(self):
        sina_store_object = sina_store.SinaStore()
        sina_store_object.weibo_table = sina_store_object.db['temp_realtime_relationship']
        sina_store_object.store_in_mongodb(self.info_dict)
        # sina_store_object = sina_store.SinaStore()
        # if fans:
        #     sina_store_object.weibo_table = sina_store_object.db['realtime_user_fans']
        #     for user in user_list:
        #         sina_store_object.store_in_mongodb(user)
        # if follow:
        #     sina_store_object.weibo_table = sina_store_object.db['realtime_user_follow']
        #     for user in user_list:
        #         sina_store_object.store_in_mongodb(user)

if __name__ == '__main__':
    a = RealtimeUserRealationship(user_id='2671467531')

    b = {
        'topic':'水滴直播',
        'question_list':
            [
                {
                    'question_name':'如何看待。。问题1',
                    'anwser_words':
                            ['好','希拉里','4444']
                    'percent':'8.33'
                },
                {
                    'question_name': '如何看待。。问题2',
                    'anwser_words':
                        ['不会', '淳朴', '4444']
                    'percent': '4.44'
                },
            ]
    }


