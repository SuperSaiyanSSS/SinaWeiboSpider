# coding=utf-8
from __future__ import print_function
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pandas as pd
import re
import numpy as np
from gensim import corpora, models
from scipy.sparse import csr_matrix
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn import svm
import numpy as np
import os,re,time,logging
import jieba
import pickle as pkl

import svm_tfidf
import os_path

from svm_utils import *

# path_doc_root = 'H:\py\workplace\/a2\SogouC.reduced2\\Reduced'
# path_tmp = 'H:\py\workplace\/a2\SogouC.reduced2\\temp1'
# path_dictionary = os.path.join(path_tmp, 'THUNews.dict')
# path_tmp_tfidf = os.path.join(path_tmp, 'tfidf_corpus')
# path_tmp_lsi = os.path.join(path_tmp, 'lsi_corpus')
# path_tmp_lsimodel = os.path.join(path_tmp, 'lsi_model.pkl')
# path_tmp_predictor = os.path.join(path_tmp, 'predictor.pkl')
#
#
# def convert_doc_to_wordlist(str_doc,cut_all):
#     sent_list = str_doc.split('\n')
#     sent_list = map(rm_char, sent_list) # 去掉一些字符，例如\u3000
#     word_2dlist = [rm_tokens(jieba.cut(part,cut_all=cut_all)) for part in sent_list] # 分词
#     word_list = sum(word_2dlist,[])
#     return word_list
#
#
# def rm_tokens(words): # 去掉一些停用次和数字
#     words_list = list(words)
#     stop_words = get_stop_words()
#     for i in range(words_list.__len__())[::-1]:
#         if words_list[i] in stop_words: # 去除停用词
#             words_list.pop(i)
#         elif words_list[i].isdigit():
#             words_list.pop(i)
#     return words_list
#
#
# def get_stop_words(path='stopwords_cn.txt'):
#     file = open(path,'rb').read().split('\n')
#     return set(file)
#
#
# def rm_char(text):
#     text = re.sub('\u3000','',text)
#     return text


def reduce_dict(weibo_test):
    dictionary = None
    if not os.path.exists(path_tmp):
        os.makedirs(path_tmp)
    # 若不存在之前创建的词典，则生成词典
    if not os.path.exists(path_dictionary):
        dictionary = corpora.Dictionary()
        files = os_path.LoadFiles(path_doc_root)
        for i, msg in enumerate(files):
            catg = msg[0]
            file = msg[1]
            file = convert_doc_to_wordlist(file, cut_all=False)
            dictionary.add_documents([file])
        # 去掉词典中出现次数过少的词语
        small_freq_ids = [tokenid for tokenid, docfreq in dictionary.dfs.items() if docfreq < 5]
        dictionary.filter_tokens(small_freq_ids)
        dictionary.compactify()
        dictionary.save(path_dictionary)
    svm_tfidf.reduce_tfidf(dictionary, weibo_test)

if __name__ == "__main__":
    reduce_dict(weibo_test = "小粉红滚！你个傻逼，体育老师教你的？吾问无为谓")