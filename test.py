# -*- coding: utf-8 -*-
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from wbcls import people
from wbcls import base
from wbcls import sina_store
from bs4 import BeautifulSoup
import requests
from wbcls import client
from wbcls import weibo

cookies = \
'_T_WM=55ac8f6c31f4eb6f286ad2e9ed8d729a; ALF=1502368858; SCF=AjsEaVa0e8KjEg3yEjwEx270PLOpYvK-1BhV7AdkMSQgcMGXjA4iW487m2bSJBS8OfK_4rraZvkWErkpduc8rzg.; SUB=_2A250YLcKDeThGeBP4lQW-CbFyj6IHXVXqtlCrDV6PUNbktAKLXXkkW19fBxtN7dryXpI0IREBn9vqzbcwQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWC9U1RTKpYdAAz2GZeMbFX5JpX5KMhUgL.Foqp1KqN1hn4eKz2dJLoI7fgB.pTSKyCKoWH1Kn4; SUHB=0XD1E55KJiiWIq; SSOLoginState=1499776859'

if __name__ == '__main__':
    dic_c = {}
    str_c = cookies
    for i in str_c.split('; '):
        dic_c[i.split('=')[0]] = i.split('=')[1]
    cookies2 = requests.utils.cookiejar_from_dict(dic_c)
    base.SinaBaseObject.cookies = cookies2
    # a = requests.get('http://weibo.cn/u/5195713909')
    # print(a.content)
    #pe = sina_people.SinaPeople('1737449733')
    pe0 = client.WeiboClient(cookies=cookies)
   # ri = pe0.sina_weibo()
  #  a = pe0._session
    pe2 = pe0.Weibo('F36Tkz299')
  #  pe2 = sina_weibo.sina_weibo(uid='FbVMx8Mtd', session=a)
    pe3 = pe2._session.get('https://weibo.cn/u/1116150122')
    print(pe3)
    print(pe3.content)
    #pe = sina_people.SinaPeople('6021561452')
  #  print(pe2.get_text())
    print(444)
    pe4 = pe0.People('6312678992')
    print(pe4)
    print(pe4.name)
    print(pe4.weibo_count)
    print(pe4.location)
    for i,j in zip(pe4.fans, range(4)):
        print(i,j)
    for i,j in zip(pe4.weibo, range(3)):
        print i.text
    print(pe2.author.name)

  # #  print(pe2.get_text())
  #   print(pe2.repost_count)
  #   print(pe2.attitude_count)
  #   print("评论数量")
  #   print(pe2.comment_count)
  #   print(pe2.author)
  #   print(pe2.time)
  #   print(pe2.author_name)
  #   for i,j in zip(pe2.comment,range(3)):
  #       print(i,j)
  #
  #   for i,j in zip(pe2.attitude, range(4)):
  #       print(i,j)
  #
  #   for i,j in zip(pe2.repost, range(2)):
  #       print(i,j)




