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
import requests


cookies = \
            'ALF=1501159357; SCF=AjsEaVa0e8KjEg3yEjwEx270PLOpYvK-1BhV7AdkMSQgUozbT8VN9e7zDppTz6FZs5PD6E5VoJ3e0JyOHFF-HIw.; SUB=_2A250ViLtDeThGeBP4lQW-CbLyTqIHXVXuU6lrDV6PUJbktANLWLBkW2HmYSKxGkq2uS0728TOqfHWar_RQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhzhoVOn6pkLuGbnO5GBEu35JpX5o2p5NHD95QceK.cS0nRS0zcWs4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNSo24SoMR1hMESntt; SUHB=0FQ7hD651l5Cff; _T_WM=55ac8f6c31f4eb6f286ad2e9ed8d729a'
if __name__ == '__main__':
    dic_c = {}
    str_c = cookies
    for i in str_c.split('; '):
        dic_c[i.split('=')[0]] = i.split('=')[1]
    cookies2 = requests.utils.cookiejar_from_dict(dic_c)
    base.SinaBaseObject.cookies = cookies2
    # a = requests.get('http://weibo.cn/u/5195713909')
    # print(a.content)
    pe = sina_people.SinaPeople('1737449733')

    #pe = sina_people.SinaPeople('6021561452')
    print(pe.fans_count)



