# -*- coding: utf-8 -*
from __future__ import print_function
import sys
sys.path.append("..")
reload(sys)
sys.setdefaultencoding('utf-8')
import jieba
from a1 import sina_people
from a1 import sina_people
from a1 import sina_weibo
from a1 import base
from a1 import test1
from a1 import sina_store
from bs4 import BeautifulSoup
import requests
import pymongo
import re

sys.path.append('../')

import jieba
import jieba.analyse
from optparse import OptionParser



def clean_keyword():
    """
    将敏感词转化为标准格式
    :return:
    """
    word_list = []
    with open('xie.txt', 'r') as f:
        for i in f.readlines():
            if i.split('=')[0].strip().strip('\n'):
                word_list.append(i.split('=')[0].strip().strip('\n'))

    with open('guang.txt', 'r') as f:
        for i in f.readlines():
            if i.split('=')[0].strip().strip('\n'):
                word_list.append(i.split('=')[0].strip().strip('\n'))

    with open('huang.txt', 'r') as f:
        for i in f.readlines():
            if i.split('=')[0].strip().strip('\n'):
                word_list.append(i.split('=')[0].strip().strip('\n'))

    with open('mingan.txt', 'r') as f:
        for i in f.readlines():
            if i.split('=')[0].strip().strip('\n'):
                word_list.append(i.split('=')[0].strip().strip('\n'))

    with open('mingan_9.txt','a') as f:
        print(word_list)
        for i in word_list:
            if i:
                b = repr(i)
                try:
                    print(unicode(eval(b), "gbk"))
                except:
                    continue
                f.write(str(unicode(eval(b), "gbk"))+' '+'300'+'\n')


def remove_equal():
    """
    去除网上所得敏感词中的等号
    :return:
    """
    count = 0
    target_list = []
    with open('mingan_word.txt', 'r') as f:
        word_list = f.readlines()
        print(len(word_list))
        for i in word_list:
             count += 1
             print(count)
             target_list.append(i.split(' ')[0])
    with open('mingan_strip_equal.txt', 'w') as f:
        for i in target_list:
            f.write(i+'\n')


class TestKeyword(object):
    """
    对传入的微博文本分词并检测是否含有敏感词
    """
    def __init__(self):
        jieba.load_userdict("keyword.txt")
        jieba.load_userdict("mingan_word.txt")
        self.topK = 12
        self.mingan_list = []
        self.get_mingan_list()

    def get_mingan_list(self):
        with open('mingan_strip_equal.txt', 'r') as f:
            word_list = f.readlines()
            for word in word_list:
                self.mingan_list.append(word.strip('\n'))

    def test_if_has_keyword(self, weibo_text):
        content = weibo_text
        tags = jieba.analyse.extract_tags(content, topK=self.topK)

        for tag in tags:
            if tag in self.mingan_list:
                print("6666666")
                print(content)
                print(tag)
                return True
            else:
                print("no")
        return False

if __name__ == '__main__':
    sys.setdefaultencoding('utf-8')
    s = sina_store.SinaStore()
    s.weibo_table = s.db['realtime_weibo']
    weibo_iter = s.get_stored_information()
    print(weibo_iter)

    count = 0
    while count < 400:
        weibo = next(weibo_iter)
        weibo_txt = weibo['text']
        print(weibo_txt)
        jieba.load_userdict("keyword.txt")
        jieba.load_userdict("mingan_word.txt")
        file_name = 'mm.txt'

        topK = 12

        content = weibo_txt
        tags = jieba.analyse.extract_tags(content, topK=topK)

     #   print(",".join(tags))

        mingan_list = []
        with open('mingan_strip_equal.txt', 'r') as f:
            word_list = f.readlines()
            print(len(word_list))
            for i in word_list:
                mingan_list.append(i.strip('\n'))
        for i in tags:
            if i in mingan_list:
                print("6666666")
                print(content)

        count += 1

   # seg_list = jieba.cut(content)
   # print(", ".join(seg_list))


    # with open('mm.txt','r') as f:
    #     s = "".join(f.readlines())
    # seg_list = jieba.cut(s, cut_all=True)
    #
    # print("Full Mode:", "/ ".join(seg_list))
    # seg_list = jieba.cut(s, cut_all=False)
    # print("Default Mode:", "/ ".join(seg_list))
    # seg_list = jieba.cut(s)
    # print(", ".join(seg_list))
    # seg_list = jieba.cut_for_search(s)
    # print(", ".join(seg_list))

