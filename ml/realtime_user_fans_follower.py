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
from wbcls.sina_store import SinaStore
import fenci
reload(sys)
sys.setdefaultencoding('utf-8')

RALATIONTABLE = 'Relation719'


class RealtimeUserRealationship(object):
    KEY = '9LF3gnOtYENP26HSoNAxPptHk7eCgxdWjL5ZuSdJXuGALaAcTrLXdGI7TkEYnIQm'

    def __init__(self, user_id, user=True, fans=True, follow=True):
        # 连接至mongodb
        self.mongo_client = pymongo.MongoClient('localhost', 27017)
        self.db = self.mongo_client['Weibo']

        self._session = requests.Session()
        self._session.mount('http://', self._create_adapter())

        self.fans_href = 'http://api03.bitspaceman.com:8000/profile/weibo?type=3&id='+str(user_id)+'&apikey=' + \
                         self.KEY + '&size=30'
        self.fans_list = []
        self.follow_href = 'http://api03.bitspaceman.com:8000/profile/weibo?type=2&id='+str(user_id)+'&apikey=' + \
                           self.KEY+'&size=30'
        self.follow_list = []

        self.user_href = 'http://api03.bitspaceman.com:8000/profile/weibo?type=1&id='+str(user_id)+'&apikey=' + self.KEY

        self.info_dict = {}
        self.get_relationship(user=user, fans=fans, follow=follow)

    def get_relationship(self, user=True, fans=True, follow=False):

        if fans:
            requests_get = self._session.get(self.fans_href, timeout=15)
            requests_content = requests_get.content
            requests_dict = json.loads(requests_content)
            self.fans_list = self.parse_requests_dict(requests_dict)
        tt.sleep(0.5)
        if follow:
            requests_get = self._session.get(self.follow_href, timeout=15)
            requests_content = requests_get.content
            requests_dict = json.loads(requests_content)
            self.follow_list = self.parse_requests_dict(requests_dict)
        tt.sleep(0.5)

        if user:
            requests_get = self._session.get(self.user_href, timeout=15)
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
            print(info_dict['name'])
            print(1111111111111111111111)
            return info_dict
        except:
            print(requests_dict)

    def store_to_mongodb(self):
        table = self.db[RALATIONTABLE]
        table.insert(self.info_dict)


    @staticmethod
    def _create_adapter():
        return requests.adapters.HTTPAdapter(
            max_retries=requests.adapters.Retry(
                total=5,
                status_forcelist=[403, 404, 408, 500, 502],
            )
        )



def get_relationship_from_mongodb(user_id):
    mongo_client = pymongo.MongoClient('localhost', 27017)
    db = mongo_client['Weibo']
    table = db[RALATIONTABLE]
    for i in table.find():
        if i['url'] == 'http://weibo.com/u/' + str(user_id):
            print(i['name'])


if __name__ == '__main__':
    a = RealtimeUserRealationship(user_id='2671467531')
    get_relationship_from_mongodb('2671467531')
    b = {
        'topic':'水滴直播',
        'question_list':
            [
                {
                    'question_name':'如何看待。。问题1',
                    'anwser_words':
                            ['好','希拉里','4444'],
                    'percent':'8.33'
                },
                {
                    'question_name': '如何看待。。问题2',
                    'anwser_words':
                        ['不会', '淳朴', '4444'],
                    'percent': '4.44'
                },
            ]
    }


