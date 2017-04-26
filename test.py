# -*- coding: utf-8 -*-
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from wbcls import sina_people
from wbcls import sina_weibo
from wbcls import base

import base64
import requests
import re
import rsa
import binascii

def Get_cookies():
    '''登陆新浪微博，获取登陆后的Cookie，返回到变量cookies中'''
    username = raw_input(u'请输入用户名：')
    password = raw_input(u'请输入密码：')

    url = 'http://login.sina.com.cn/sso/prelogin.php?entry=sso&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&client=ssologin.js(v1.4.4)%'+username
    html = requests.get(url).content

    servertime = re.findall('"servertime":(.*?),',html,re.S)[0]
    nonce = re.findall('"nonce":"(.*?)"',html,re.S)[0]
    pubkey = re.findall('"pubkey":"(.*?)"',html,re.S)[0]
    rsakv = re.findall('"rsakv":"(.*?)"',html,re.S)[0]

    username = base64.b64encode(username) #加密用户名
    rsaPublickey = int(pubkey, 16)
    key = rsa.PublicKey(rsaPublickey, 65537) #创建公钥
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(password) #拼接明文js加密文件中得到
    passwd = rsa.encrypt(message, key) #加密
    passwd = binascii.b2a_hex(passwd) #将加密信息转换为16进制。

    login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.4)'
    data = {'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '7',
        'userticket': '1',
        'ssosimplelogin': '1',
        'vsnf': '1',
        'vsnval': '',
        'su': username,
        'service': 'miniblog',
        'servertime': servertime,
        'nonce': nonce,
        'pwencode': 'rsa2',
        'sp': passwd,
        'encoding': 'UTF-8',
        'prelt': '115',
        'rsakv' : rsakv,
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype': 'META'
        }
    html = requests.post(login_url,data=data).content
    urlnew = re.findall('location.replace\(\'(.*?)\'',html,re.S)[0]

    #发送get请求并保存cookies
    cookies = requests.get(urlnew).cookies
    return cookies


def get_myuid(cookies):

    url = 'http://weibo.com/'
    html = requests.get(url,cookies=cookies).content #用get请求加入cookies参数登陆微博主页

    a = html.find('[\'uid\']=')
    b = html[a:].find(';')
    myuid = html[a + len('[\'uid\']='): a + b][1:-1] #获取我的uid

    a = html.find('[\'nick\']=')
    b = html[a:].find(';')
    myname = html[a + len('[\'nick\']='): a + b][1:-1] #获取我的用户名
    return myuid,myname


if __name__ == '__main__':
    cookies = Get_cookies()
    print cookies
    print type(cookies)
    base.SinaBaseObject.cookies = cookies
    uid,myname = get_myuid(cookies)
    print 1111111111111111111111111111111
    print myname
    print 1111111111111111111111111111111
    # a = SinaPeople(uid =5977796987)
    # hehe = a.get_fans_list(required_member_count=15)
    # #a.get_fans_list()
    # print(len(hehe))
    # b = SinaWeibo(uid='ECxqn6uA0')
    # a = b.get_repost_list(required_repost_count=10)
    # print(len(a))
    # print(a[-1]['time'])
    #print(a[-1]['terminal_source'])
    # p = sina_people.SinaPeople(uid=5977796987)
    # print("----------")
    # a = p.get_weibo_list(required_weibo_count=2)
    # for i in a:
    #     print("-------------")
    #     print(i.uid)
    #     b = i.uid
    #     print("---------------")
    #
   # init_json_file()
   # Get_cookies()
    c = sina_weibo.SinaWeibo(uid = 'EFX6orYJv', required_count=5)
    print(1111111111111111)
    print(c.comment_count)
    # print(c.comment_list)
    # print(c.author_uid)
    print(c.author_name)
    print(1111111111111111)
    # print(c.text)
    # print(c.attitude_count)
    # print(c.attitude_list)
    #pass