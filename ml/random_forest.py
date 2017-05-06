# -*- coding: utf-8 -*
from __future__ import unicode_literals, print_function
from __future__ import division
import sklearn
import pandas as pd
import json
import math
import csv
import pymongo
import sklearn
import sys
sys.path.append("..")
from a1 import base
from a1 import sina_store
reload(sys)
sys.setdefaultencoding('utf-8')


class MachineLearning(base.SinaBaseObject):
    def __init__(self):
        self.is_First = True
        self.is_First_2 = True
        self.gbc = ''
        self.dtc = ''
        self.rfc = ''

    def set_feature_vector_dict(self, feature_vector_dict):
        self.clean_feture_vector_dict(feature_vector_dict, is_first=self.is_First)
        self.is_First = False

    def set_test_feature_vector_dict(self, feature_vector_dict):
        self.clean_test_feture_vector_dict(feature_vector_dict, is_first_2=self.is_First_2)
        self.is_First_2 = False

    # 将传入的字典转化为csv文件
    @staticmethod
    def clean_feture_vector_dict(feature_vector_dict, is_first=False):
        with open('names.csv', 'ab') as csvfile:
            fieldnames = ['uid', 'similarity', 'platform', 'reputation', 'entropy', 'human_or_machine']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if is_first:
                writer.writeheader()
            writer.writerow(
                {'uid': feature_vector_dict['uid'],
                 'similarity': feature_vector_dict['similarity'],
                 'platform': feature_vector_dict['platform'],
                 'reputation': feature_vector_dict['reputation'],
                 'entropy': feature_vector_dict['entropy'],
                 'human_or_machine': feature_vector_dict['human_or_machine']
                 }
            )

    @staticmethod
    def clean_test_feture_vector_dict(feature_vector_dict, is_first_2=False):
        with open('needs.csv', 'ab') as csvfile:
            fieldnames = ['uid', 'similarity', 'platform', 'reputation', 'entropy', 'human_or_machine']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if is_first:
                writer.writeheader()
            writer.writerow(
                {'uid': feature_vector_dict['uid'],
                 'similarity': feature_vector_dict['similarity'],
                 'platform': feature_vector_dict['platform'],
                 'reputation': feature_vector_dict['reputation'],
                 'entropy': feature_vector_dict['entropy'],
                 'human_or_machine': feature_vector_dict['human_or_machine']
                 }
            )

    # 进行单一决策树和随机森林的训练模型及检验
    def rand_forest_train(self):
        # 读取本地用户特征信息
        users = pd.read_csv('names.csv')
        # 选取similarity、platform、reputation、entropy作为判别人类或机器的特征
        X = users[['similarity', 'platform', 'reputation', 'entropy']]
        y = users['human_or_machine']

        # 对原始数据进行分割， 25%的数据用于测试
        from sklearn.cross_validation import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=33)

        # 对类别特征进行转化，成为特征向量
        from sklearn.feature_extraction import DictVectorizer
        vec = DictVectorizer(sparse=False)
        X_train = vec.fit_transform(X_train.to_dict(orient='record'))
        X_test = vec.transform(X_test.to_dict(orient='record'))

        # 使用单一决策树进行集成模型的训练及预测分析
        from sklearn.tree import DecisionTreeClassifier
        dtc = DecisionTreeClassifier()
        dtc.fit(X_train, y_train)
        dtc_y_pred = dtc.predict(X_test)

        # 使用随机森林分类器进行集成模型的训练及预测分析
        from sklearn.ensemble import RandomForestClassifier
        rfc = RandomForestClassifier()
        rfc.fit(X_train, y_train)
        rfc_y_pred = rfc.predict(X_test)

        # 使用梯度提升决策树进行集成模型的训练及预测分析
        from sklearn.ensemble import GradientBoostingClassifier
        gbc = GradientBoostingClassifier()
        gbc.fit(X_train, y_train)
        gbc_y_pred = gbc.predict(X_test)

        from sklearn.metrics import classification_report
        # 输出单一决策树在测试集上的分类准确性， 以及更加详细的精确率 召回率 F1指标
        print("单一决策树的准确性为", dtc.score(X_test, y_test))
        print(classification_report(dtc_y_pred, y_test))

        # 输出随机森林分类器在测试集上的分类准确性，以及更加详细的精确率 召回率 F1指标
        print("随机森林分类器的准确性为", rfc.score(X_test, y_test))
        print(classification_report(rfc_y_pred, y_test))

        # 输出梯度提升决策树在测试集上的分类准确性，以及更加详细的精确率 召回率 F1指标
        print("梯度提升决策树的准确性为", gbc.score(X_test, y_test))
        print(classification_report(gbc_y_pred, y_test))


        users = pd.read_csv('values.csv')

        # 检验是否为机器或人类
        X = users[['similarity', 'platform', 'reputation', 'entropy']]
        X = vec.transform(X.to_dict(orient='record'))
        print(rfc.predict(X))

        self.dtc = dtc
        self.rfc = rfc
        self.gbc = gbc


def get_dict_from_weibo_table():
    ml = MachineLearning()
    sina_store_object = sina_store.SinaStore()
    sina_store_object.weibo_table = sina_store_object.db['human_vector_info']
    iter = sina_store_object.get_stored_information()
    while True:
        try:
            info_dict = next(iter)
            ml.set_feature_vector_dict(info_dict)
        except StopIteration:
            break
    sina_store_object.weibo_table = sina_store_object.db['machine_vector_info']
    iter = sina_store_object.get_stored_information()
    while True:
        try:
            info_dict = next(iter)
            ml.set_feature_vector_dict(info_dict)
        except StopIteration:
            break
    print("已结束 正在训练模型。。。")
    ml.rand_forest_train()


def start_training():
    get_dict_from_weibo_table()

if __name__ == "__main__":
    start_training()
