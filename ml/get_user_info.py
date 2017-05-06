# -*- coding: utf-8 -*
from __future__ import unicode_literals, print_function
from __future__ import division
import math
import sys
sys.path.append("..")
reload(sys)
sys.setdefaultencoding('utf-8')
import datetime
import difflib
from a1 import sina_people
from a1 import sina_weibo
from a1 import base
from a1 import test1
from a1 import sina_store
from bs4 import BeautifulSoup
import requests
import time as tt
import pymongo
import re


headers_for_baidu = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Host':'www.baidu.com',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'
}


# def get_human_personal_info():
#     s = sina_store.SinaStore()
#     s.weibo_table = s.db['human_personal_info']
#     with open('human_uid.txt','r') as f:
#         for i in f.readlines():
#             if i!='':
#                 print(i)
#                 pe = sina_people.SinaPeople(i)
#                 s.store_in_mongodb(pe)


# 将时间转换为标准格式
def clean_time(now_time):
    if now_time.startswith('今'):
        now_time = datetime.datetime(2017, 5, 3)
    elif "分钟" in now_time:
        now_time = datetime.datetime(2017, 5, 3)
    elif "月" in now_time:
        month = int(now_time.split("月")[0][-2:])
        day = int(now_time.split("日")[0][-2:])
        now_time = datetime.datetime(2017, month, day)
    else:
        year = int(now_time.split('-')[0])
        month = int(now_time.split('-')[1])
        day = int(now_time.split('-')[2][:3])
        now_time = datetime.datetime(year, month, day)
    return now_time


# 最终修正条件信息熵计算公式
# TODO:论文给定的公式有问题 计算得出的离散有限序列的条件熵不满足非负性
def final_calculation_formula(space_list):
    lence = len(space_list)
    if lence < 2:
        raise IndexError+"时间间隔个数应至少2个！"
    entropy_list = []
    scale_list = []
    is_first = True
    end_seq = 2
    while end_seq < lence:
        local_lence = end_seq
        entropy = calculation_formula(space_list[:end_seq], local_lence)
        entropy_list.append(entropy)
        if is_first:
            is_first = False
        else:
            scale_list.append(calculate_perc_xm(space_list[:end_seq], local_lence))
        end_seq += 1
    result_list = []
    for i in range(len(entropy_list)-1):
        result_list.append(entropy_list[i+1]-entropy_list[i]+scale_list[i]*entropy_list[0])
    print(result_list)
    print(scale_list)
    return min(result_list)


# pers(Xm):长度为 m 的序列里面只出现过一次的序列所占的比例
def calculate_perc_xm(space_list, lence):
    only_count = 0
    print(space_list)
    for i in range(lence):
        for j in range(i+1, lence):
            if space_list[i] == space_list[j]:
                break
            if j == lence-1:
                only_count += 1
    scale = only_count/lence
    return scale


# 计算信息熵
def calculation_formula(space_list, lence):
    probability_list = []
    while space_list:
        item_count = space_list.count(space_list[0])
        # 由于引入了Python 3.x的除法规则，不会取整
        probability_list.append(item_count/lence)
        space_list = filter(lambda x: x != space_list[0], space_list)
    entropy = 0
    for p in probability_list:
        entropy += p*math.log(p)
    entropy = -entropy
    return entropy


# 获取信息熵
def get_entropy_of_information(person_dict):
    space_list = []
    weibo_list_lence = len(person_dict['weibo_list'])
    print(weibo_list_lence)
    # 有的原创微博太少 舍去该样本
    try:
        last_time = str(person_dict['weibo_list']['1']['time'])
        last_time = clean_time(last_time)
    except KeyError:
        return -1
    for i in range(weibo_list_lence-2):
        now_time = str(person_dict['weibo_list'][str(i+2)]['time'])
        now_time = clean_time(now_time)
        space_list.append((last_time - now_time).days)
        print((last_time-now_time).days)
        last_time = now_time

    entropy = calculation_formula(space_list, len(space_list))
    print(entropy)
    return entropy

    # while 1:
    #     try:
    #         print(next(a))
    #     except StopIteration:
    #         break


# 获取用户信誉度
def get_reputation(person_dict):
    try:
        fans_count = int(person_dict['fans_count'])
        follow_count = int(person_dict['follow_count'])
        reputation = fans_count/(fans_count+follow_count)
    except ValueError:
        return -1
    return reputation


# 获取发表微博的平台种类数量
def get_num_of_platform(person_dict):
    platform_set = set()
    for item in person_dict['weibo_list']:
        platform_set.add(str(person_dict['weibo_list'][str(item)]['terminal_source']).strip())
    return len(platform_set)


# 检查原创微博是否过少 偶然性影响较大
def check_if_too_little(person_dict):
    repost_count = 0
    total_count = len(person_dict['weibo_list'])
    for item in person_dict['weibo_list']:
        if str(person_dict['weibo_list'][str(item)]['is_repost'])=='True':
            print(person_dict['weibo_list'][str(item)]['is_repost'])
            repost_count += 1
            continue
    if total_count-repost_count < 3:
        return -1
    return 0


# 获取发表微博的内容相似度
def get_similarity_of_content(person_dict):
    """
    利用百度搞基搜索的site:(weibo.com) 查找是否存在重复微博
    :param person_dict: 用户信息的字典
    :return: 内容相似度
    """
    identical_count = 0
    total_count = 0
    repost_count = 0
    if check_if_too_little(person_dict) == -1:
        return -1
    for item in person_dict['weibo_list']:
        if str(person_dict['weibo_list'][str(item)]['is_repost'])=='True':
            print(person_dict['weibo_list'][str(item)]['is_repost'])
            repost_count += 1
            continue
        else:
            total_count += 1

            if total_count >= 15:
                break
            copy_test_1 = False
            copy_test_2 = False

            text = str(person_dict['weibo_list'][str(item)]['text'])
            print(person_dict['weibo_list'][str(item)]['href'])
            q1 = text
            print(q1)

            re_emotion = re.compile('(\[.*?\])')            # 去除微博表情文字
            q1 = re_emotion.sub('', q1)
            q1_list = re.split('!|！|,|。|……|：|、|,|，|；|;|——', unicode(q1))    # 按标点符号分割

            # 选择最大和第二大子字符串
            max_len = 'x'
            for string_seq in q1_list:
                if len(string_seq)> len(max_len):
                    max_len = string_seq
            print(max_len)
            second_len = 'x'
            for string_seq in q1_list:
                if len(string_seq) > len(second_len) and string_seq != max_len:
                    second_len = string_seq
            q1 = max_len
            q1_2 = second_len

            url = 'https://www.baidu.com/s?q1='+q1+'&q2=&q3=&q4=&rn=10&lm=0&ct=0&ft=&q5=&q6=weibo.com&tn=baiduadv'
            url_2 = 'https://www.baidu.com/s?q1='+q1_2+'&q2=&q3=&q4=&rn=10&lm=0&ct=0&ft=&q5=&q6=weibo.com&tn=baiduadv'
            # baidu_requests = requests.get(url, headers=headers_for_baidu, timeout=3)
            baidu_requests = base.SinaBaseObject.retry_requests_static(url, headers=headers_for_baidu, timeout=3)
            copy_test_1 = __parse_baidu_page__(baidu_requests, q1)

            if len(q1_2) > 5:
                baidu_requests = base.SinaBaseObject.retry_requests_static(url_2, headers=headers_for_baidu, timeout=3)
                # baidu_requests = requests.get(url_2, headers=headers_for_baidu, timeout=3)
                copy_test_2 = __parse_baidu_page__(baidu_requests, q1_2)

            if copy_test_1 or copy_test_2:
                identical_count += 1
                print(copy_test_1, copy_test_2)
                print("确实是抄袭的")
            else:
                print("是原创的")
            tt.sleep(3)

    # 部分数据有残缺，未能成功抓取到微博或几乎全为转发，则舍去
    if total_count < 3 or repost_count > 28:
        return -1

    similarity = identical_count/total_count
    print("内容相似度为"+str(similarity))
    return similarity


# 百度搜索页面处理逻辑
def __parse_baidu_page__(baidu_requests, q1):
    """
    @ author: wxw
    @ time: 2017/5/4
    提取搜索到的高亮字符串 并与要查找的进行对比
    若满足一定的相似度要求 则认为重复
    :param baidu_requests: requests抓取百度搜索所得页面源代码
    :param q1: 要查找的字符串
    :return: 是否重复
    """
    baidu_bs4 = BeautifulSoup(baidu_requests.content, "lxml")
    highlight_list = baidu_bs4.find_all('div', attrs={'class': 'c-abstract'})
    ok_count = 0
    for unit in highlight_list:
        try:
            highlight_word = unit.em.get_text()
            print(highlight_word)
            if str(q1).strip() == str(highlight_word).strip():
                ok_count += 1
                print("已发现")
            # 若高亮的文本与寻找的文本差异很小（可能少了几个字符）则同样认为是已找到
            elif difflib.SequenceMatcher(None, str(q1), str(highlight_word)).ratio() > 0.88:
                print(difflib.SequenceMatcher(None, str(q1), str(highlight_word)).ratio())
                ok_count += 1
                print("认为已找到")
            else:
                print("no")
        except AttributeError:
            print("这是空的")

    if ok_count > 1:
        return True
    else:
        return False


def __store_human_feature_vector__(feature_vector):
    s = sina_store.SinaStore()
    s.weibo_table = s.db['human_vector_info']
    iter = s.get_stored_information()
    flag = 0
    while True:
        try:
            person_dict = next(iter)
            if str(person_dict['uid']) == str(feature_vector['uid']):
                flag = 1
                break
        except StopIteration:
            flag = 0
            break

    if flag == 0:
        s.store_in_mongodb(feature_vector)


def store_human_feature_vector(sina_store_object):
    sina_store_object.weibo_table = sina_store_object.db['human_personal_info']
    # 获取返回的生成器
    iter = sina_store_object.get_stored_information()
    item_count = 0
    while True:
        try:
            feature_vector = {}
            person_dict = next(iter)
            entropy = get_entropy_of_information(person_dict)
            similarity = get_similarity_of_content(person_dict)
            platform = get_num_of_platform(person_dict)
            reputation = get_reputation(person_dict)
            if reputation == -1:
                print("该数据为残缺数据！舍去")
                print("现在抽取到第" + str(item_count) + "个用户！！")
                item_count += 1
                continue
            feature_vector['entropy'] = entropy
            feature_vector['similarity'] = similarity
            if similarity == -1 or entropy == -1:
                print("该数据为残缺数据！舍去")
                print("现在抽取到第" + str(item_count) + "个用户！！")
                item_count += 1
                continue
            feature_vector['uid'] = str(person_dict['uid'])
            feature_vector['platform'] = platform
            feature_vector['reputation'] = reputation
            feature_vector['human_or_machine'] = 1
            item_count += 1
            print("现在抽取到第"+str(item_count)+"个用户！！")
            __store_human_feature_vector__(feature_vector)
        except StopIteration:
            print("人类用户已提取特征向量完毕！")
            break


def __store_machine_feature_vector__(feature_vector):
    s = sina_store.SinaStore()
    s.weibo_table = s.db['machine_vector_info']
    iter = s.get_stored_information()
    flag = 0
    while True:
        try:
            person_dict = next(iter)
            if str(person_dict['uid']) == str(feature_vector['uid']):
                flag = 1
                break
        except StopIteration:
            flag = 0
            break

    if flag == 0:
        s.store_in_mongodb(feature_vector)


def store_machine_feature_vector(sina_store_object):
    sina_store_object.weibo_table = sina_store_object.db['machine_personal_info']
    # 获取返回的生成器
    iter = sina_store_object.get_stored_information()
    item_count = 0
    while True:
        try:
            feature_vector = {}
            person_dict = next(iter)
            entropy = get_entropy_of_information(person_dict)
            similarity = get_similarity_of_content(person_dict)
            platform = get_num_of_platform(person_dict)
            reputation = get_reputation(person_dict)
            if reputation == -1:
                print("该数据为残缺数据！舍去")
                print("现在抽取到第" + str(item_count) + "个用户！！")
                item_count += 1
                continue
            feature_vector['entropy'] = entropy
            feature_vector['similarity'] = similarity
            if similarity == -1 or entropy == -1:
                print("该数据为残缺数据！舍去")
                print("现在抽取到第" + str(item_count) + "个用户！！")
                item_count += 1
                continue
            feature_vector['uid'] = str(person_dict['uid'])
            feature_vector['platform'] = platform
            feature_vector['reputation'] = reputation
            feature_vector['human_or_machine'] = 0
            item_count += 1
            print("现在抽取到第"+str(item_count)+"个用户！！")
            __store_machine_feature_vector__(feature_vector)
        except StopIteration:
            print("机器用户已提取特征向量完毕！")
            break


if __name__ == '__main__':
    """
    从mongodb中获取human和machine的信息，
    并计算其信息熵、相似度、信誉度等特征
    并将特征存入mongodb

    示例：
    s = sina_store.SinaStore()
    store_human_feature_vector(s)
    store_machine_feature_vector(s)
    """





