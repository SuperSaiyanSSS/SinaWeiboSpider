# -*- coding:utf-8 -*-
from __future__ import unicode_literals, print_function
import weibo
import time as tt

APP_KEY = '4205885419'
APP_SECRET = '892c885ff32a4b452be58cda23c1cea6'
CALL_BACK = 'http://api.weibo.com/oauth2/default.html'
ACCESS_TOKEN = '2.00GrlpNEwp7azCa0cf771a73RorfEE'


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
    statuses = client.statuses__public_timeline()['statuses']
    length = len(statuses)
    print('现在获得了'+str(length)+'条新微博')

    for i in range(0, length):
        created_at = statuses[i]['created_at']
        id = statuses[i]['user']['id']
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
            'id': id,
            'nickname': nickname,
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


def startCollecte(count_=-1):
    weiboList = []
    client = get_client(APP_KEY, APP_SECRET, CALL_BACK, ACCESS_TOKEN)
    while True:
        print('现在开始获取！')
        try:
            weiboList = run(weiboList, client)
            return weiboList
        except:
            tt.sleep(0.1)
            # 默认循环无数次，直到获得成功为止
            # 可通过更改参数count_的值来改变循环次数
            if(count_!=0):
                count_ = count_-1
            else:
                break

if __name__ == "__main__":
    weiboList = startCollecte(count_=3)
    print(weiboList.getLastValue()['description'])