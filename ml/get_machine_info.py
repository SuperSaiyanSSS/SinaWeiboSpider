from __future__ import unicode_literals, print_function
import sys
sys.path.append("..")
reload(sys)
sys.setdefaultencoding('utf-8')
from a1 import sina_people
from a1 import sina_people
from a1 import sina_weibo
from a1 import base
from a1 import test1
from a1 import sina_store
import time as tt
from bs4 import BeautifulSoup
import requests
import pymongo
import re

headers_2 = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie': '_T_WM=0ff248d78f4984aa135c5b2e53c11079; ALF=1496373314; SCF=AjsEaVa0e8KjEg3yEjwEx270PLOpYvK-1BhV7AdkMSQgM7IlYI27IV6TA5-eb6avSBhK-q5migy9jGYZkeqPPpU.; SUB=_2A250DTviDeThGeBP4lQW-CbFyj6IHXVXDkWqrDV6PUJbktBeLWLAkW1fCr2k7XOfWxI9AQSa5M6kQfvxPg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWC9U1RTKpYdAAz2GZeMbFX5JpX5o2p5NHD95QceK.cS0nR1K2EWs4DqcjSH.ieC0-R-.R7HK.R1Btt; SUHB=04W-CMkuo5eJq_; SSOLoginState=1493781426',
'Host':'weibo.cn',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'
}


def get_machine_personal_info():
    s = sina_store.SinaStore()
    s.weibo_table = s.db['machine_personal_info']
    with open('machine_uid.txt','r') as f:
        for i in f.readlines():
            if i!='':
                print(i)
                pe = sina_people.SinaPeople(i)
                s.store_in_mongodb(pe)




if __name__ == '__main__':
    dic_c = {}
    str_c = headers_2['Cookie']
    for i in str_c.split('; '):
        dic_c[i.split('=')[0]] = i.split('=')[1]
    cookies2 = requests.utils.cookiejar_from_dict(dic_c)
    base.SinaBaseObject.cookies = cookies2
    if 1:
        dic_c = {}
        str_c = headers_2['Cookie']
        for i in str_c.split('; '):
            dic_c[i.split('=')[0]] = i.split('=')[1]
        cookies2 = requests.utils.cookiejar_from_dict(dic_c)
        base.SinaBaseObject.cookies = cookies2

    # for i in range(0,21):
    #     if
    print(cookies2)
    with open('machine_uid.txt','r') as f:
        uid = f.readlines()
    print(len(uid))
    # get_machine_personal_info()


    # a = requests.get('https://weibo.cn/2318253071/fans?page=1', cookies=cookies2)
    # a = BeautifulSoup(a.content, "lxml")
    # unit = a.findAll('div', attrs={'class': 'c'})[1]
    # print(unit)
    # unit_list = unit.findAll('table')
    # print(unit_list)
    # uid_list = []
    #
    # for i in unit_list:
    #     print(str(i.tr.findAll('td')[1].a.attrs['href']).split('/')[-1])
    #     uid_list.append(str(i.tr.findAll('td')[1].a.attrs['href']).split('/')[-1])
    #
    # for j in range(2,5):
    #     tt.sleep(4)
    #     a = requests.get('https://weibo.cn/2318253071/fans?page='+str(j), cookies=cookies2)
    #     a = BeautifulSoup(a.content, "lxml")
    #     unit = a.findAll('div', attrs={'class': 'c'})[1]
    #     unit_list = unit.findAll('table')
    #     for i in unit_list:
    #         print(str(i.tr.findAll('td')[1].a.attrs['href']).split('/')[-1])
    #         uid_list.append(str(i.tr.findAll('td')[1].a.attrs['href']).split('/')[-1])
    #
    # with open('machine_uid.txt','a') as f:
    #     for i in uid_list:
    #         f.write(i+'\n')
   # get_human_personal_info()
    # a = requests.get('http://weibo.cn/u/5195713909')
    # print(a.content)
   # pe = sina_people.SinaPeople('6021561452')
    #  pe = sina_weibo.SinaWeibo('F16aup9Im')
    # we = sina_weibo.SinaWeibo('F15Kpbev2')
    # for name, value in vars(we).items():
    #   print(name, value)
    # c_set = set()
    # s = sina_store.SinaStore()
    # s.weibo_table = s.db['try2']
    # rmrb = s.get_human_info()
    # comment_list = rmrb['comment_list']
    # for name, value in comment_list.items():
    #     author_uid = value['author_uid']
    #     c_set.add(str(author_uid))

    # with open('human_uid.txt','a') as f:
    #     for i in c_set:
    #         f.write(i+'\n')




