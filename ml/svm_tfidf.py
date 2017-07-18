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

import svm_lsi
import os_path
from svm_utils import *

# path_doc_root = 'H:\py\workplace\/a2\SogouC.reduced2\\Reduced'  # 根目录 即存放按类分类好的问本纪
# path_tmp = 'H:\py\workplace\/a2\SogouC.reduced2ss1\\temp1'  # 存放中间结果的位置
# path_dictionary = os.path.join(path_tmp, 'THUNews.dict')
# path_tmp_tfidf = os.path.join(path_tmp, 'tfidf_corpus')
# path_tmp_lsi = os.path.join(path_tmp, 'lsi_corpus')
# path_tmp_lsimodel = os.path.join(path_tmp, 'lsi_model.pkl')
# path_tmp_predictor = os.path.join(path_tmp, 'predictor.pkl')

corpus_lsi = None
lsi_model = None
predictor = None


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


def reduce_tfidf(dictionary, weibo_test):
    corpus_tfidf = None
    # # # # 第二阶段，  开始将文档转化成tfidf
    if not os.path.exists(path_tmp_tfidf):
        print('=== 未检测到有tfidf文件夹存在，开始生成tfidf向量 ===')
        # 如果指定的位置没有tfidf文档，则生成一个。如果有，则跳过该阶段
        if not dictionary:  # 如果跳过了第一阶段，则从指定位置读取词典
            dictionary = corpora.Dictionary.load(path_dictionary)
        os.makedirs(path_tmp_tfidf)
        files = os_path.LoadFiles(path_doc_root)
        tfidf_model = models.TfidfModel(dictionary=dictionary)
        corpus_tfidf = {}
        for i, msg in enumerate(files):
            catg = msg[0]
            file = msg[1]
            word_list = convert_doc_to_wordlist(file, cut_all=False)
            file_bow = dictionary.doc2bow(word_list)
            file_tfidf = tfidf_model[file_bow]
            tmp = corpus_tfidf.get(catg, [])
            tmp.append(file_tfidf)
            if tmp.__len__() == 1:
                corpus_tfidf[catg] = tmp
        # 将tfidf中间结果储存起来
        catgs = list(corpus_tfidf.keys())
        for catg in catgs:
            corpora.MmCorpus.serialize('{f}{s}{c}.mm'.format(f=path_tmp_tfidf, s=os.sep, c=catg),
                                       corpus_tfidf.get(catg),
                                       id2word=dictionary
                                       )
            print('catg {c} has been transformed into tfidf vector'.format(c=catg))
        print('=== tfidf向量已经生成 ===')
    else:
        print('=== 检测到tfidf向量已经生成，跳过该阶段 ===')

    svm_lsi.reduce_lsi(dictionary, corpus_tfidf, weibo_test)