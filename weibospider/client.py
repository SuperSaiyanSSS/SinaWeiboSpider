# coding:utf-8
from __future__ import unicode_literals, print_function
import requests
from utils import *
import os
import importlib
import base


class WeiboClient(object):
    """
    微博客户端类 维护网络会话 使用cookies登录
    """

    def __init__(self, cookies=None):
        self._session = requests.Session()
        self._session.verify = False
        self._session.headers.update(Default_Header)
        self._session.mount('http://', self._create_adapter())
        if cookies is not None:
            self.login_with_acquired_cookies(cookies)
        else:
            raise SystemError("未传入cookies")

    @staticmethod
    def _create_adapter():
        return requests.adapters.HTTPAdapter(
            max_retries=requests.adapters.Retry(
                total=5,
                status_forcelist=[403, 404, 408, 500, 502],
            )
        )

    def login_with_acquired_cookies(self, cookies):
        """
        note:
            保存在文件中的cookies形式为chrome浏览器F12后NetWork中Headers里的形式
            如：
                'ALF=1501159357; SCF=AjsEaVa0e8KjEg3yEjwEx270PLOpYvK-1BhV7AdkMSQgUozbT8VN9e7zDppTz6FZs5PD6E5VoJ3e0J
                yOHFF-HIw.; SUB=_2A250ViLtDeThGeBP4lQW-CbLyTqIHXVXuU6lrDV6PUJbktANLWLBkW2HmYSKxGkq2uS0728TOqfHWar_RQ..;
                 SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhzhoVOn6pkLuGbnO5GBEu35JpX5o2p5NHD95QceK.cS0nRS0zcWs4DqcjMi--
                 NiK.Xi-2Ri--ciKnRi-zNSo24SoMR1hMESntt; SUHB=0FQ7hD651l5Cff; _T_WM=55ac8f6c31f4eb6f286ad2e9ed8d729'
        """
        # 若文件目录下存在cookies，则其为文件, 打开后获取
        # 否则为cookies字符串，直接获取
        if os.path.isfile(cookies):
            with open(cookies, 'r') as f:
                cookies = f.read()

        cookies_dict = {}
        # 将cookies字符串转为字典
        for item in cookies.split('; '):
            cookies_dict[item.split('=')[0]] = item.split('=')[1]
        self._session.cookies.update(cookies_dict)
        # cookies2 = requests.utils.cookiejar_from_dict(cookies_dict)
        base._session = self._session

    def __getattr__(self, item):
        """本函数为类工厂模式，用于获取各种类的实例，如 `Answer` `Question` 等.
        :支持的形式有:
            1. client.me()   （暂未实现）
            2. client.weibo()
            3. client.people()
            4. client.comment()
            5. client.attitude()
            6. client.repost()
            参数均为对应的id，返回对应的类的实例。
        """
        # 回调对应模块的构造函数
        base.SinaBaseObject._session = self._session

        def callback_getattr(id):
            # 类名第一个字母大写
            return getattr(module, item.capitalize())(id)
        # TODO: 增加me
        attr_list = ['me', 'weibo', 'people', 'comment', 'attitude', 'repost']
        if item.lower() in attr_list:
            module = importlib.import_module('.'+item.lower(), 'weibospider')
            return callback_getattr


if __name__ == '__main__':
    a = WeiboClient(cookies='as=12')
    a.sina_weibo('666')
