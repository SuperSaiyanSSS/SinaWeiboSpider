# coding=utf-8

from __future__ import unicode_literals, print_function
import requests
import json
import time as tt
from bs4 import BeautifulSoup
import sys
import re

reload(sys)
sys.path.append('../')
sys.setdefaultencoding('utf-8')


# headers_for_get = {
# 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
# 'Accept-Encoding':'gzip, deflate, sdch',
# 'Accept-Language':'zh-CN,zh;q=0.8',
# 'Cache-Control':'max-age=0',
# 'Connection':'keep-alive',
# 'Cookie': '_T_WM=0ff248d78f4984aa135c5b2e53c11079; ALF=1495630107; SCF=AjsEaVa0e8KjEg3yEjwEx270PLOpYvK-1BhV7AdkMSQgVvrJ48ic42g3Xqe49zEjKtpWuFcU6KaL2lKIyLzY43s.; SUB=_2A251-YQQDeRhGeNH7VIV9izNwj2IHXVXBSxYrDV6PUJbktBeLUn6kW0ntTSLDvUTciwLCGGI3rSIiDX8jQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhaydrjX2CLPhFdjQ77gn4P5JpX5o2p5NHD95Qf1Kq7ShqEeK.pWs4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNSK.cehBceo24eBtt; SUHB=0mxUEyUKiYW96L; SSOLoginState=1493038144',
# 'Host':'weibo.cn',
# 'Upgrade-Insecure-Requests':'1',
# 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'
# }


class SinaBaseObject(object):
    """
    所有新浪类的基类
    :TODO 刷新cookie策略
    """
    # 静态变量cookies
    cookies = ''
    headers_for_get = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'weibo.cn',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'
    }

    def __init__(self):
        self.time_delay = 1

    # 对requests.get()函数进行改进，增加重试和报错功能
    def retry_requests(self, url, uid=''):
        """
        :param url: 待爬取的链接
        :param headers: 请求头
        :param uid: 帖子或用户的uid值（str类型）
        :return: requests_content 爬起的页面源码(bs4类型)
        """
        # 设置重试次数
        retry_count = 3
        while retry_count != 0:
            try:
                requests_get = requests.get(url, headers=self.headers_for_get, cookies=self.cookies, timeout=3)
                requests_content = requests_get.content
                # 加入了__T_WM的cookie项后仍然无法在wap版微博登录
                # 只能采用网页版
                # if self.flag == 0:
                #     cookies = requests.utils.dict_from_cookiejar(self.cookies)
                #     requests_get.cookies = requests.utils.dict_from_cookiejar(requests_get.cookies)
                #     cookies = dict(cookies.items() + requests_get.cookies.items())
                #     self.cookies = requests.utils.cookiejar_from_dict(cookies)
                #     self.flag = 1
                #     print(self.cookies)
                print(url)
                print(requests_content)
                print(requests_get.status_code)
                # 记录发起网络请求的url及时间
                with open('log_url.txt', 'a') as f:
                    f.write(str(url) + ' ' + str(tt.strftime("%Y-%m-%d %H:%M:%S", tt.localtime())) + '\n')

                requests_content = BeautifulSoup(requests_content, "lxml")
                return requests_content
            except:
                tt.sleep(3)
                print("获取" + str(uid) + "页面时失败，正在重试。。。")
                print(requests_get.status_code)
            finally:
                retry_count -= 1
                if retry_count == 0:
                    raise Exception("重试次数已完，仍获取" + str(uid) + "的页面失败！")

    @staticmethod
    def retry_requests_static(url, headers={}, timeout=3):
        """
        :param url: 待爬取的链接
        :param headers: 请求头
        :param uid: 帖子或用户的uid值（str类型）
        :return: requests_content 爬起的页面源码(bs4类型)
        """
        # 设置重试次数
        retry_count = 3
        while retry_count != 0:
            try:
                tt.sleep(3)
                print(url)
                requests_get = requests.get(url, headers=headers, timeout=3)
                print(url)
                # 记录发起网络请求的url及时间
                with open('log_static_url.txt', 'a') as f:
                    f.write(str(url) + ' ' + str(tt.strftime("%Y-%m-%d %H:%M:%S", tt.localtime())) + '\n')
                return requests_get
            except:
                tt.sleep(3)
                print("获取页面时失败，正在重试。。。")
            finally:
                retry_count -= 1
                if retry_count == 0:
                    raise Exception, "重试次数已完，仍获取页面失败！"


if __name__ == '__main__':
    print(111)
