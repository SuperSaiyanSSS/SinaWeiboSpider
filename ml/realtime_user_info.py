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
from a1 import base
from a1 import sina_store
from a1 import sina_weibo
from a1 import sina_people
reload(sys)
sys.setdefaultencoding('utf-8')


class RealtimeRandomWeibo(object):
    KEY = '9LF3gnOtYENP26HSoNAxPptHk7eCgxdWjL5ZuSdJXuGALaAcTrLXdGI7TkEYnIQm'

    def __init__(self):
        self.href = 'http://api01.bitspaceman.com:8000/post/weibo?kw=的&apikey='+self.KEY
        self.get_random_weibo()

    def get_random_weibo(self):
        requests_get = requests.get(self.href, timeout=15)
        requests_content = requests_get.content
        requests_dict = json.loads(requests_content)
        for name, value in requests_dict.items():
            print(name, value)
        print(len(requests_dict['data']))
        self.parse_requests_dict(requests_dict)

    def parse_requests_dict(self, requests_dict):
        weibo_list = []
        weibo = sina_weibo.SinaWeibo()
        count = 0
        for i in requests_dict['data']:
            if i['mblog'].has_key('retweeted_status'):
                count+=1
                print(i['mblog']['retweeted_status']['user']['location'])
                print(i['mblog']['retweeted_status']['reposts_count'])
                print(i['mblog']['retweeted_status']['user']['id'])
                print(i['mblog']['retweeted_status']['text'])

        print(count)

if __name__ == '__main__':
    a = RealtimeRandomWeibo()