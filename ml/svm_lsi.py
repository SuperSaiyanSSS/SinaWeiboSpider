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

import svm_module

path_doc_root = 'H:\py\workplace\/a2\SogouC.reduced2\\Reduced'  # 根目录 即存放按类分类好的问本纪
path_tmp = 'H:\py\workplace\/a2\SogouC.reduced2\\temp1'  # 存放中间结果的位置
path_dictionary = os.path.join(path_tmp, 'THUNews.dict')
path_tmp_tfidf = os.path.join(path_tmp, 'tfidf_corpus')
path_tmp_lsi = os.path.join(path_tmp, 'lsi_corpus')
path_tmp_lsimodel = os.path.join(path_tmp, 'lsi_model.pkl')
path_tmp_predictor = os.path.join(path_tmp, 'predictor.pkl')


def reduce_lsi(dictionary, corpus_tfidf, weibo_test):
    corpus_lsi = None
    lsi_model = None
    # # # # 第三阶段，  开始将tfidf转化成lsi
    if not os.path.exists(path_tmp_lsi):
        print('=== 未检测到有lsi文件夹存在，开始生成lsi向量 ===')
        if not dictionary:
            dictionary = corpora.Dictionary.load(path_dictionary)
        if not corpus_tfidf:  # 如果跳过了第二阶段，则从指定位置读取tfidf文档
            print('--- 未检测到tfidf文档，开始从磁盘中读取 ---')
            # 从对应文件夹中读取所有类别
            files = os.listdir(path_tmp_tfidf)
            catg_list = []
            for file in files:
                t = file.split('.')[0]
                if t not in catg_list:
                    catg_list.append(t)

            # 从磁盘中读取corpus
            corpus_tfidf = {}
            for catg in catg_list:
                path = '{f}{s}{c}.mm'.format(f=path_tmp_tfidf, s=os.sep, c=catg)
                corpus = corpora.MmCorpus(path)
                corpus_tfidf[catg] = corpus
            print('--- tfidf文档读取完毕，开始转化成lsi向量 ---')

        # 生成lsi model
        os.makedirs(path_tmp_lsi)
        corpus_tfidf_total = []
        catgs = list(corpus_tfidf.keys())
        for catg in catgs:
            tmp = corpus_tfidf.get(catg)
            corpus_tfidf_total += tmp
        lsi_model = models.LsiModel(corpus=corpus_tfidf_total, id2word=dictionary, num_topics=50)
        # 将lsi模型存储到磁盘上
        lsi_file = open(path_tmp_lsimodel, 'wb')
        pkl.dump(lsi_model, lsi_file)
        lsi_file.close()
        del corpus_tfidf_total  # lsi model已经生成，释放变量空间
        print('--- lsi模型已经生成 ---')

        # 生成corpus of lsi, 并逐步去掉 corpus of tfidf
        corpus_lsi = {}
        for catg in catgs:
            corpu = [lsi_model[doc] for doc in corpus_tfidf.get(catg)]
            corpus_lsi[catg] = corpu
            corpus_tfidf.pop(catg)
            corpora.MmCorpus.serialize('{f}{s}{c}.mm'.format(f=path_tmp_lsi, s=os.sep, c=catg),
                                       corpu,
                                       id2word=dictionary)
        print('=== lsi向量已经生成 ===')
    else:
        print('=== 检测到lsi向量已经生成，跳过该阶段 ===')

    svm_module.reduce_module(dictionary, corpus_lsi, lsi_model, weibo_test)