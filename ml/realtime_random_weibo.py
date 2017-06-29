# -*- coding:utf-8 -*-
from __future__ import unicode_literals, print_function
import weibo
import time as tt
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("..")
from a1 import sina_store
from a1 import sina_weibo

APP_KEY = '3175988140'
APP_SECRET = 'f445636b8fc0b7b5e75474c3ab8d320b'
CALL_BACK = 'http://api.weibo.com/oauth2/default.html'
ACCESS_TOKEN = '2.00xUU4VGKbHw9D47e3cfc2c8UhoSBB'


class myAPIClient(weibo.APIClient):
    def __init__(self, app_key, app_secret, redirect_uri, access_token):
        weibo.APIClient.__init__(self, app_key, app_secret, redirect_uri, access_token)

    def request_access_token_info(self, access_token):
        r = weibo._http_post('%s%s' % (self.auth_url, 'get_token_info'), access_token=access_token)
        current = int(tt.time())
        expires = r.expire_in + current
        return weibo.JsonDict(expires_in=expires)


def get_client(appkey, appsecret, callback, access_token):
    client = myAPIClient(appkey, appsecret, callback, access_token)
    r = client.request_access_token_info(access_token)
    expires_in = r.expires_in
    client.set_access_token(access_token, expires_in)
    return client


def run(weiboList, client):
    statuses = client.statuses__public_timeline(count=2)['statuses']
    length = len(statuses)
    print('现在获得了'+str(length)+'条新微博')

    for i in range(0, length):
        created_at = statuses[i]['created_at']
        author_uid = statuses[i]['user']['id']
        id = statuses[i]['id']
        source = statuses[i]['source']
        province = statuses[i]['user']['province']
        city = statuses[i]['user']['city']
        followers_count = statuses[i]['user']['followers_count']
        friends_count = statuses[i]['user']['friends_count']
        statuses_count = statuses[i]['user']['statuses_count']
        url = statuses[i]['user']['url']
        geo = statuses[i]['geo']
        comments_count = statuses[i]['comments_count']
        reposts_count = statuses[i]['reposts_count']
        nickname = statuses[i]['user']['screen_name']
        desc = statuses[i]['user']['description']
        location = statuses[i]['user']['location']
        text = statuses[i]['text']

        weibo_dict = {
            'created_at': created_at,
            'author_uid': author_uid,
            'id': id,
            'author_name': nickname,
            'source': source,
            'text': text,
            'province': province,
            'location': location,
            'description': desc,
            'city': city,
            'followers_count': followers_count,
            'friends_count': friends_count,
            'statuses_count': statuses_count,
            'url': url,
            'geo': geo,
            'comments_count': comments_count,
            'reposts_count': reposts_count
            }
        weiboList.append(weibo_dict)
    return weiboList


def gain_random_weibolist(count_=-1):
    weibolist = []
    client = get_client(APP_KEY, APP_SECRET, CALL_BACK, ACCESS_TOKEN)
    while True:
        print('现在开始获取！')
        try:
            weibolist = run(weibolist, client)
            return weibolist
        except:
            tt.sleep(0.1)
            # 默认循环无数次，直到获得成功为止
            # 可通过更改参数count_的值来改变循环次数
            if(count_!= 0):
                count_ = count_-1
            else:
                break

# def clean_weibolist(weibolist):
#     for weibo in weibolist:
#         weibo_object = sina_weibo.SinaWeibo()
#
# def store_random_weibolist():
#     sina_store_object = sina_store.SinaStore()
#     sina_store_object.weibo_table = sina_store_object.db['random_weibo']
#     #sina_store_object.

if __name__ == "__main__":
    weiboList = gain_random_weibolist(count_=3)
    print(weiboList[0]['id'])
    print(weiboList[0]['author_uid'])
    print(weiboList[0]['author_name'])
    print(weiboList[0]['source'])
    print(weiboList[0]['text'])
    print(weiboList[0]['created_at'])
    print(111111111111111111111)
    for name, value in weiboList[0].items():
        print(name, value)