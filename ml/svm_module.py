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

import svm_result
from svm_utils import *
# path_doc_root = 'H:\py\workplace\/a2\SogouC.reduced2\\Reduced'  # 根目录 即存放按类分类好的问本纪
# path_tmp = 'H:\py\workplace\/a2\SogouC.reduced2ss4\\temp1'  # 存放中间结果的位置
# path_dictionary = os.path.join(path_tmp, 'THUNews.dict')
# path_tmp_tfidf = os.path.join(path_tmp, 'tfidf_corpus')
# path_tmp_lsi = os.path.join(path_tmp, 'lsi_corpus')
# path_tmp_lsimodel = os.path.join(path_tmp, 'lsi_model.pkl')
# path_tmp_predictor = os.path.join(path_tmp, 'predictor.pkl')
#
#
# def get_stop_words(path='stopwords_cn.txt'):
#     file = open(path,'rb').read().split('\n')
#     return set(file)


# def svm_classify(train_set, train_tag, test_set, test_tag):
#     clf = svm.LinearSVC()
#     clf_res = clf.fit(train_set, train_tag)
#     train_pred  = clf_res.predict(train_set)
#     test_pred = clf_res.predict(test_set)
#
#     train_err_num, train_err_ratio = checkPred(train_tag, train_pred)
#     test_err_num, test_err_ratio = checkPred(test_tag, test_pred)
#
#     print('=== 分类训练完毕，分类结果如下 ===')
#     print('训练集误差: {e}'.format(e=train_err_ratio))
#     print('检验集误差: {e}'.format(e=test_err_ratio))
#
#     return clf_res
#
#
# def checkPred(data_tag, data_pred):
#     if data_tag.__len__() != data_pred.__len__():
#         raise RuntimeError('The length of data tag and data pred should be the same')
#     err_count = 0
#     for i in range(data_tag.__len__()):
#         if data_tag[i]!=data_pred[i]:
#             err_count += 1
#     err_ratio = err_count / data_tag.__len__()
#     return [err_count, err_ratio]


def reduce_module(dictionary, corpus_lsi, lsi_model, weibo_test):
    # # # # 第四阶段，  分类
    predictor = None
    if not os.path.exists(path_tmp_predictor):
        print('=== 未检测到判断器存在，开始进行分类过程 ===')
        if not corpus_lsi:  # 如果跳过了第三阶段
            print('--- 未检测到lsi文档，开始从磁盘中读取 ---')
            files = os.listdir(path_tmp_lsi)
            catg_list = []
            for file in files:
                t = file.split('.')[0]
                if t not in catg_list:
                    catg_list.append(t)
            # 从磁盘中读取corpus
            corpus_lsi = {}
            for catg in catg_list:
                path = '{f}{s}{c}.mm'.format(f=path_tmp_lsi, s=os.sep, c=catg)
                corpus = corpora.MmCorpus(path)
                corpus_lsi[catg] = corpus
            print('--- lsi文档读取完毕，开始进行分类 ---')

        tag_list = []
        doc_num_list = []
        corpus_lsi_total = []
        catg_list = []
        files = os.listdir(path_tmp_lsi)
        for file in files:
            t = file.split('.')[0]
            if t not in catg_list:
                catg_list.append(t)
        for count, catg in enumerate(catg_list):
            tmp = corpus_lsi[catg]
            tag_list += [count] * tmp.__len__()
            doc_num_list.append(tmp.__len__())
            corpus_lsi_total += tmp
            corpus_lsi.pop(catg)

        # 将gensim中的mm表示转化成numpy矩阵表示
        data = []
        rows = []
        cols = []
        line_count = 0
        for line in corpus_lsi_total:
            for elem in line:
                rows.append(line_count)
                cols.append(elem[0])
                data.append(elem[1])
            line_count += 1
        lsi_matrix = csr_matrix((data, (rows, cols))).toarray()
        # 生成训练集和测试集
        rarray = np.random.random(size=line_count)
        train_set = []
        train_tag = []
        test_set = []
        test_tag = []
        for i in range(line_count):
            if rarray[i] < 0.8:
                train_set.append(lsi_matrix[i, :])
                train_tag.append(tag_list[i])
            else:
                test_set.append(lsi_matrix[i, :])
                test_tag.append(tag_list[i])

        # 生成分类器
        predictor = svm_classify(train_set, train_tag, test_set, test_tag)
        x = open(path_tmp_predictor, 'wb')
        pkl.dump(predictor, x)
        x.close()
    else:
        print('=== 检测到分类器已经生成，跳过该阶段 ===')

    svm_result.reduce_result(dictionary, lsi_model, predictor, weibo_test)