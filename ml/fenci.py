# -*- coding: utf-8 -*
from __future__ import unicode_literals, print_function
import sys
sys.path.append("..")
reload(sys)
sys.setdefaultencoding('utf-8')
import jieba

sys.path.append('../')

import jieba
import jieba.analyse
from optparse import OptionParser

if __name__ == '__main__':
    sys.setdefaultencoding('utf-8')
    s = sina_store.SinaStore()
    human = s.get_human_info()
    print(human)
    weibo_txt = human['weibo_list']['10']['text']
    print(weibo_txt)
    jieba.load_userdict("keyword.txt")
    file_name = 'mm.txt'

    topK = 12

    #content = open(file_name, 'rb').read()
    content = weibo_txt
    tags = jieba.analyse.extract_tags(content, topK=topK)

    print(",".join(tags))

    seg_list = jieba.cut(content)
    print(", ".join(seg_list))


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

