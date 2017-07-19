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