<<<<<<< HEAD
# -*- coding: utf-8 -*-
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from wbcls import sina_people
from wbcls import sina_weibo
from wbcls import base
from wbcls import sina_store
from bs4 import BeautifulSoup
import base64
import requests
import re
import rsa
import binascii
try_headers = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie':'SINAGLOBAL=9749994808807.969.1462031573715; UM_distinctid=15ba31e8f531d7-07c52349a-67151474-15f900-15ba31e8f543cf; UOR=v.baidu.com,widget.weibo.com,login.sina.com.cn; un=dd083764@163.com; wvr=6; SSOLoginState=1493290759; SCF=AjsEaVa0e8KjEg3yEjwEx270PLOpYvK-1BhV7AdkMSQglzpQYR4kh9QpdmBGwjflxudOsWcvwNjH44y5HkUaYEo.; SUB=_2A250BaKCDeThGeNH7FMX9CzJzjmIHXVXcpNKrDV8PUJbmtBeLVeikW9TBGBZrKdS00g7g8PZSM1sGVha8g..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5uXfcJCAoMCAZgGpXYw6fj5JpX5o2p5NHD95Qf1KMpSoBESK-fWs4Dqcjyi--ciKL8iK.Ni--4iK.fi-isi--ci-zpiKLsPNifIsip; SUHB=0nl-AZgzIqF98d; ALF=1524799399; YF-Ugrow-G0=57484c7c1ded49566c905773d5d00f82; YF-V5-G0=d22a701aae075ca04c11f0ef68835839; _s_tentry=-; Apache=4257309376262.1284.1493291763610; ULV=1493291763620:62:18:7:4257309376262.1284.1493291763610:1493262270015; YF-Page-G0=b98b45d9bba85e843a07e69c0880151a; WBStorage=02e13baf68409715|undefined',
'Host':'weibo.com',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'
}

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
    print(servertime, nonce, pubkey, rsakv)
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


def get_weibo(uid,cookies,page):
    '''获取前page页的微博'''

    url = 'http://weibo.com/'+uid+'/profile'
    my_weibo = []
    for p in range(1,page+1):
        #新浪微博每一页信息是异步加载的，分三次加载
        for pb in range(-1,2):
            data = {'pagebar':str(pb),
                    'pre_page':str(p),
                    'page':str(p),
                    }
            if p == 1:
                if pb == -1:
                    html = requests.get(url,cookies=cookies).content
                else:
                    html = requests.get(url,cookies=cookies,params=data).content
            else:
                html = requests.get(url,cookies=cookies,params=data).content

            hlist = html.split('node-type=\\"feed_list_content\\"')[1:]
            for i in hlist:
                i = i.split('<\/div>')[0]
                s = re.findall('>(.*?)<',i)
                weibo = ''
                for j in s:
                    weibo = weibo + j.strip('\\n /\\')
                if len(weibo) != 0:
                    my_weibo.append(weibo)
    return my_weibo

def get_follow(myuid,cookies):

    '''获取微博关注用户的uid与用户名'''
    url = 'http://weibo.com/' + myuid + '/follow'
    html = requests.get(url,cookies=cookies).content

    c = html.find('member_ul clearfix')-13
    html = html[c:]
    u = re.findall(r'[uid=]{4}([0-9]+)[&nick=]{6}(.*?)\\"',html)

    user_id = []
    uname = []
    for i in u:
        user_id.append(i[0]) #把uid储存到列表user_id中
        uname.append(i[1])   #把用户名储存到列表uname中
    return user_id,uname


def pass_cookies():
    return headers_2

headers_2 = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie': '_T_WM=0ff248d78f4984aa135c5b2e53c11079; ALF=1496318146; SCF=AjsEaVa0e8KjEg3yEjwEx270PLOpYvK-1BhV7AdkMSQgcvtxS-8hSqQgtOi37X15usxPejtU-Q-P-S5eLluIwnI.; SUB=_2A250DARDDeThGeBP4lQW-CbFyj6IHXVXDqwLrDV6PUJbktBeLWjgkW0mRdcHIzWZqvsMrQuwo8DpPQmeXg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWC9U1RTKpYdAAz2GZeMbFX5JpX5o2p5NHD95QceK.cS0nR1K2EWs4DqcjSH.ieC0-R-.R7HK.R1Btt; SUHB=0ElKxu4GSlYMWP; SSOLoginState=1493726227',
'Host':'weibo.cn',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'
}

if __name__ == '__main__':
    # cookies = Get_cookies()
    # print cookies
    # print type(cookies)
    # myuid,myname = get_myuid(cookies)
    # print 1111111111111111111111111111111
    # print myname
    # print 1111111111111111111111111111111
    # s = requests.Session()
    # a = s.get('http://weibo.com/u/5971642555/home?wvr=5',cookies=cookies, headers=headers_3)
    # print(a.content)
    # print(a.cookies)
    # print(a.headers)
    # print(44444444444444444444)
    # headers_3['Referer'] = 'http://login.sina.com.cn/sso/login.php?url=http%3A%2F%2Fweibo.cn%2F&_rand=1493689476.0249&gateway=1&service=sinawap&entry=sinawap&useticket=1&returntype=META&sudaref=&_client_version=0.6.24'
    # b = s.get('http://weibo.cn/u/5195713909', allow_redirects=True)
    # print(b.content)
    # print(b.history)
    # print(b.status_code)
    # print(b.url)
    # print(b.headers['Location'])
    # 这是网页版的 暂时不作
    # base.SinaBaseObject.cookies = cookies
    # a = requests.get('http://weibo.cn/u/5195713909', cookies=cookies)
    # print a.content

    #这是wp版的
    if 1:
        dic_c = {}
        str_c = headers_2['Cookie']
        for i in str_c.split('; '):
            dic_c[i.split('=')[0]] = i.split('=')[1]
        cookies2 = requests.utils.cookiejar_from_dict(dic_c)
        base.SinaBaseObject.cookies = cookies2
    # a = requests.get('http://weibo.cn/u/5195713909')
    # print(a.content)
    pe = sina_people.SinaPeople('6021561452')
  #  pe = sina_weibo.SinaWeibo('F16aup9Im')
    #we = sina_weibo.SinaWeibo('F15Kpbev2')
    #for name, value in vars(we).items():
     #   print(name, value)
    s = sina_store.SinaStore()
    s.store_in_mongodb(pe)
    # pe = sina_people.SinaPeople('5501547091')
    # #pe2 = sina_people.SinaPeople('5141786170')
    # c = sina_store.SinaStore()
    # dd = c.analyze_data(pe)
    # print(dd)
    # print(type(dd))
    # c.store_in_mongodb([pe])





    # uid, uname = get_follow(myuid, cookies)  # 获取关注用户的uid与用户名
    # for i in range(len(uid)):
    #     my_weibo = get_weibo(uid[i], cookies, 3)  # 获取用户前三页的微博信息
    #     for j in my_weibo:
    #         print(uid[i] + ' ' + uname[i] + ' ' + j + '\n')
    #     print str(i + 1) + '/' + str(len(uid))

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
   #  c = sina_weibo.SinaWeibo(uid = 'EFX6orYJv', required_count=5)
   #  print(1111111111111111)
   #  print(c.comment_count)
   #  print(c.text)
   #  # print(c.comment_list)
   #  # print(c.author_uid)
   #  print(c.author_name)
   #  print(1111111111111111)
   #  b = sina_weibo.SinaWeibo(uid='ECvINo9oQ')
   #  print b.text
   #  print(6666666666666)
   #  print b.cookies
   #  # print(c.text)
   #  print(b.attitude_count)
    # print(c.attitude_list)
    #pass
    # d_cookie = requests.get('http://weibo.cn/comment/ECvINo9oQ', cookies=cookies).cookies
    # base.SinaBaseObject.cookies = d_cookie
    # print cookies
    # print d_cookie
   # cookie_str = ''
    #base.SinaBaseObject.headers_for_get['Cookie'] = cookie_str
   # a = sina_people.SinaPeople(uid='5503147448')
    #print(a.cookies)
    # cookie_dict = requests.utils.dict_from_cookiejar(c.cookies)
    # for key, value in cookie_dict.items():
    #     cookie_str += key+'='+value+';'
    # print 22222222222
    # print(c.cookies)
    # print cookie_str
    # print 999999999999999999999999999999999999999999999
    # base.SinaBaseObject.headers_for_get['Cookie'] = cookie_str
    # print base.SinaBaseObject.headers_for_get
   # a.get_personal_information()
=======
# -*- coding: utf-8 -*-
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from wbcls import sina_people
from wbcls import sina_weibo
from wbcls import base
from wbcls import sina_store
from bs4 import BeautifulSoup
import base64
import requests
import re
import rsa
import binascii
try_headers = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie':'SINAGLOBAL=9749994808807.969.1462031573715; UM_distinctid=15ba31e8f531d7-07c52349a-67151474-15f900-15ba31e8f543cf; UOR=v.baidu.com,widget.weibo.com,login.sina.com.cn; un=dd083764@163.com; wvr=6; SSOLoginState=1493290759; SCF=AjsEaVa0e8KjEg3yEjwEx270PLOpYvK-1BhV7AdkMSQglzpQYR4kh9QpdmBGwjflxudOsWcvwNjH44y5HkUaYEo.; SUB=_2A250BaKCDeThGeNH7FMX9CzJzjmIHXVXcpNKrDV8PUJbmtBeLVeikW9TBGBZrKdS00g7g8PZSM1sGVha8g..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5uXfcJCAoMCAZgGpXYw6fj5JpX5o2p5NHD95Qf1KMpSoBESK-fWs4Dqcjyi--ciKL8iK.Ni--4iK.fi-isi--ci-zpiKLsPNifIsip; SUHB=0nl-AZgzIqF98d; ALF=1524799399; YF-Ugrow-G0=57484c7c1ded49566c905773d5d00f82; YF-V5-G0=d22a701aae075ca04c11f0ef68835839; _s_tentry=-; Apache=4257309376262.1284.1493291763610; ULV=1493291763620:62:18:7:4257309376262.1284.1493291763610:1493262270015; YF-Page-G0=b98b45d9bba85e843a07e69c0880151a; WBStorage=02e13baf68409715|undefined',
'Host':'weibo.com',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'
}

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
    print(servertime, nonce, pubkey, rsakv)
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


def get_weibo(uid,cookies,page):
    '''获取前page页的微博'''

    url = 'http://weibo.com/'+uid+'/profile'
    my_weibo = []
    for p in range(1,page+1):
        #新浪微博每一页信息是异步加载的，分三次加载
        for pb in range(-1,2):
            data = {'pagebar':str(pb),
                    'pre_page':str(p),
                    'page':str(p),
                    }
            if p == 1:
                if pb == -1:
                    html = requests.get(url,cookies=cookies).content
                else:
                    html = requests.get(url,cookies=cookies,params=data).content
            else:
                html = requests.get(url,cookies=cookies,params=data).content

            hlist = html.split('node-type=\\"feed_list_content\\"')[1:]
            for i in hlist:
                i = i.split('<\/div>')[0]
                s = re.findall('>(.*?)<',i)
                weibo = ''
                for j in s:
                    weibo = weibo + j.strip('\\n /\\')
                if len(weibo) != 0:
                    my_weibo.append(weibo)
    return my_weibo

def get_follow(myuid,cookies):

    '''获取微博关注用户的uid与用户名'''
    url = 'http://weibo.com/' + myuid + '/follow'
    html = requests.get(url,cookies=cookies).content

    c = html.find('member_ul clearfix')-13
    html = html[c:]
    u = re.findall(r'[uid=]{4}([0-9]+)[&nick=]{6}(.*?)\\"',html)

    user_id = []
    uname = []
    for i in u:
        user_id.append(i[0]) #把uid储存到列表user_id中
        uname.append(i[1])   #把用户名储存到列表uname中
    return user_id,uname


def pass_cookies():
    return headers_2

headers_2 = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie': '_T_WM=0ff248d78f4984aa135c5b2e53c11079; ALF=1496318146; SCF=AjsEaVa0e8KjEg3yEjwEx270PLOpYvK-1BhV7AdkMSQgcvtxS-8hSqQgtOi37X15usxPejtU-Q-P-S5eLluIwnI.; SUB=_2A250DARDDeThGeBP4lQW-CbFyj6IHXVXDqwLrDV6PUJbktBeLWjgkW0mRdcHIzWZqvsMrQuwo8DpPQmeXg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWC9U1RTKpYdAAz2GZeMbFX5JpX5o2p5NHD95QceK.cS0nR1K2EWs4DqcjSH.ieC0-R-.R7HK.R1Btt; SUHB=0ElKxu4GSlYMWP; SSOLoginState=1493726227',
'Host':'weibo.cn',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'
}

if __name__ == '__main__':
    """
    使用说明：把上面的headers_2换成自己的即可
    方法： 提前用自己的账号在本机登录新浪微博
        在chrome浏览器中F12，点击Network选项
        在浏览器的url栏中输入weibo.cn
        此时可以抓到目标地址为weibo.cn的数据包
        复制粘贴Network框中的headers值粘贴到headers_2中
    警告:  若用于商业用途请提前联系 3233069648@qq.com
        这是测试版 所以设置的延迟较高，避免新浪监测
        持续改进中。。。
        后期会加入cookie池 代理池
        机器学习判别水军用户等
        并尝试破解新浪.cn的登录
        喜欢的就点个Star吧~！
                                     2017/5/4
    """
    # cookies = Get_cookies()
    # print cookies
    # print type(cookies)
    # myuid,myname = get_myuid(cookies)
    # print 1111111111111111111111111111111
    # print myname
    # print 1111111111111111111111111111111

    # 这是网页版的 暂时不作
    # base.SinaBaseObject.cookies = cookies
    # a = requests.get('http://weibo.cn/u/5195713909', cookies=cookies)
    # print a.content

    #这是wap版的
    if 1:
        dic_c = {}
        str_c = headers_2['Cookie']
        for i in str_c.split('; '):
            dic_c[i.split('=')[0]] = i.split('=')[1]
        cookies2 = requests.utils.cookiejar_from_dict(dic_c)
        base.SinaBaseObject.cookies = cookies2
    pe = sina_people.SinaPeople('6021561452')
    s = sina_store.SinaStore()
    s.store_in_mongodb(pe)


>>>>>>> dc68cd2a148a888e7b401e4472f276d6dedd779c
