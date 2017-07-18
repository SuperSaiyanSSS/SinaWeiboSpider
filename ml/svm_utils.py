# coding=utf-8
from __future__ import print_function
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import re
import jieba
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn import svm

path_doc_root = 'H:\py\workplace\/a2\SogouC.reduced2\\Reduced'  # 根目录 即存放按类分类好的问本纪
path_tmp = 'H:\py\workplace\/a2\SogouC.reduced2ss11\\temp1'  # 存放中间结果的位置
path_dictionary = os.path.join(path_tmp, 'THUNews.dict')
path_tmp_tfidf = os.path.join(path_tmp, 'tfidf_corpus')
path_tmp_lsi = os.path.join(path_tmp, 'lsi_corpus')
path_tmp_lsimodel = os.path.join(path_tmp, 'lsi_model.pkl')
path_tmp_predictor = os.path.join(path_tmp, 'predictor.pkl')

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


def svm_classify(train_set, train_tag, test_set, test_tag):
    clf = svm.LinearSVC()
    clf_res = clf.fit(train_set, train_tag)
    train_pred  = clf_res.predict(train_set)
    test_pred = clf_res.predict(test_set)

    train_err_num, train_err_ratio = checkPred(train_tag, train_pred)
    test_err_num, test_err_ratio = checkPred(test_tag, test_pred)

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