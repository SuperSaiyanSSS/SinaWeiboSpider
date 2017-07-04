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
'_T_WM=55ac8f6c31f4eb6f286ad2e9ed8d729a; ALF=1501757269; SCF=AjsEaVa0e8KjEg3yEjwEx270PLOpYvK-1BhV7AdkMSQg6GnmWvNUCfhJuEaNVwG-f1xzQqCpNiGlhdX5myd0cOk.; SUB=_2A250XwIBDeThGeBP4lQW-CbFyj6IHXVXo65JrDV6PUNbktAKLVmkkW1iLH6PrXnuPsDVPDx2JM7Xw8araQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWC9U1RTKpYdAAz2GZeMbFX5JpX5KMhUgL.Foqp1KqN1hn4eKz2dJLoI7fgB.pTSKyCKoWH1Kn4; SUHB=0laVSs7LQCygWF; SSOLoginState=1499165269'

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



