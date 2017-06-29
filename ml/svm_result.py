# coding=utf-8
from __future__ import unicode_literals, print_function
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

path_doc_root = 'H:\py\workplace\/a2\SogouC.reduced2\\Reduced'  # 根目录 即存放按类分类好的问本纪
path_tmp = 'H:\py\workplace\/a2\SogouC.reduced2\\temp1'  # 存放中间结果的位置
path_dictionary = os.path.join(path_tmp, 'THUNews.dict')
path_tmp_tfidf = os.path.join(path_tmp, 'tfidf_corpus')
path_tmp_lsi = os.path.join(path_tmp, 'lsi_corpus')
path_tmp_lsimodel = os.path.join(path_tmp, 'lsi_model.pkl')
path_tmp_predictor = os.path.join(path_tmp, 'predictor.pkl')
n = 2  # n 表示抽样率， n抽1
def convert_doc_to_wordlist(str_doc,cut_all):
    sent_list = str_doc.split('\n')
    sent_list = map(rm_char, sent_list) # 去掉一些字符，例如\u3000
    word_2dlist = [rm_tokens(jieba.cut(part,cut_all=cut_all)) for part in sent_list] # 分词
    word_list = sum(word_2dlist,[])
    return word_list
def rm_tokens(words): # 去掉一些停用次和数字
    words_list = list(words)
    stop_words = get_stop_words()
    for i in range(words_list.__len__())[::-1]:
        if words_list[i] in stop_words: # 去除停用词
            words_list.pop(i)
        elif words_list[i].isdigit():
            words_list.pop(i)
    return words_list
def get_stop_words(path='stopwords_cn.txt'):
    file = open(path,'rb').read().split('\n')
    return set(file)
def rm_char(text):
    text = re.sub('\u3000','',text)
    return text

def svm_classify(train_set,train_tag,test_set,test_tag):

    clf = svm.LinearSVC()
    clf_res = clf.fit(train_set,train_tag)
    train_pred  = clf_res.predict(train_set)
    test_pred = clf_res.predict(test_set)

    train_err_num, train_err_ratio = checkPred(train_tag, train_pred)
    test_err_num, test_err_ratio  = checkPred(test_tag, test_pred)

    print('=== 分类训练完毕，分类结果如下 ===')
    print('训练集误差: {e}'.format(e=train_err_ratio))
    print('检验集误差: {e}'.format(e=test_err_ratio))

    return clf_res


def checkPred(data_tag, data_pred):
    if data_tag.__len__() != data_pred.__len__():
        raise RuntimeError('The length of data tag and data pred should be the same')
    err_count = 0
    for i in range(data_tag.__len__()):
        if data_tag[i]!=data_pred[i]:
            err_count += 1
    err_ratio = err_count / data_tag.__len__()
    return [err_count, err_ratio]


def reduce_result(dictionary, lsi_model, predictor, weibo_test):
    # # # # 第五阶段，  对新文本进行判断
    if not dictionary:
        dictionary = corpora.Dictionary.load(path_dictionary)
    if not lsi_model:
        lsi_file = open(path_tmp_lsimodel,'rb')
        lsi_model = pkl.load(lsi_file)
        lsi_file.close()
    if not predictor:
        x = open(path_tmp_predictor,'rb')
        predictor = pkl.load(x)
        x.close()
    files = os.listdir(path_tmp_lsi)
    catg_list = []
    for file in files:
        t = file.split('.')[0]
        if t not in catg_list:
            catg_list.append(t)

    demo_doc = weibo_test
    print(demo_doc)
    demo_doc = list(jieba.cut(demo_doc,cut_all=False))
    demo_bow = dictionary.doc2bow(demo_doc)
    tfidf_model = models.TfidfModel(dictionary=dictionary)
    demo_tfidf = tfidf_model[demo_bow]
    demo_lsi = lsi_model[demo_tfidf]
    data = []
    cols = []
    rows = []
    for item in demo_lsi:
        data.append(item[1])
        cols.append(item[0])
        rows.append(0)
    demo_matrix = csr_matrix((data,(rows,cols))).toarray()
    x = predictor.predict(demo_matrix)
    print('分类结果为：{x}'.format(x=catg_list[x[0]]))

