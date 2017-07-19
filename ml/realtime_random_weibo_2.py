# -*- coding: utf-8 -*
from __future__ import unicode_literals, print_function
from __future__ import division
import json
import pymongo
import requests
from bs4 import BeautifulSoup
import sys
sys.path.append("..")
import random
import fenci
reload(sys)
sys.setdefaultencoding('utf-8')

REALTIMEWEIBO = 'realtime719'
REALTIMEWEIBOT = 'realtime719t'


location_dict = {
    '上海': [121.4648,31.2891],
    '东莞': [113.8953,22.901],
    '东营': [118.7073,37.5513],
    '中山': [113.4229,22.478],
    '临汾': [111.4783,36.1615],
    '临沂': [118.3118,35.2936],
    '丹东': [124.541,40.4242],
    '丽水': [119.5642,28.1854],
    '乌鲁木齐': [87.9236,43.5883],
    '佛山': [112.8955,23.1097],
    '保定': [115.0488,39.0948],
    '兰州': [103.5901,36.3043],
    '包头': [110.3467,41.4899],
    '北京': [116.4551,40.2539],
    '北海': [109.314,21.6211],
    '南京': [118.8062,31.9208],
    '南宁': [108.479,23.1152],
    '南昌': [116.0046,28.6633],
    '南通': [121.1023,32.1625],
    '厦门': [118.1689,24.6478],
    '台州': [121.1353,28.6688],
    '合肥': [117.29,32.0581],
    '呼和浩特': [111.4124,40.4901],
    '咸阳': [108.4131,34.8706],
    '哈尔滨': [127.9688,45.368],
    '唐山': [118.4766,39.6826],
    '嘉兴': [120.9155,30.6354],
    '大同': [113.7854,39.8035],
    '大连': [122.2229,39.4409],
    '天津': [117.4219,39.4189],
    '太原': [112.3352,37.9413],
    '威海': [121.9482,37.1393],
    '宁波': [121.5967,29.6466],
    '宝鸡': [107.1826,34.3433],
    '宿迁': [118.5535,33.7775],
    '常州': [119.4543,31.5582],
    '广州': [113.5107,23.2196],
    '廊坊': [116.521,39.0509],
    '延安': [109.1052,36.4252],
    '张家口': [115.1477,40.8527],
    '徐州': [117.5208,34.3268],
    '德州': [116.6858,37.2107],
    '惠州': [114.6204,23.1647],
    '成都': [103.9526,30.7617],
    '扬州': [119.4653,32.8162],
    '承德': [117.5757,41.4075],
    '拉萨': [91.1865,30.1465],
    '无锡': [120.3442,31.5527],
    '日照': [119.2786,35.5023],
    '昆明': [102.9199,25.4663],
    '杭州': [119.5313,29.8773],
    '枣庄': [117.323,34.8926],
    '柳州': [109.3799,24.9774],
    '株洲': [113.5327,27.0319],
    '武汉': [114.3896,30.6628],
    '汕头': [117.1692,23.3405],
    '江门': [112.6318,22.1484],
    '沈阳': [123.1238,42.1216],
    '沧州': [116.8286,38.2104],
    '河源': [114.917,23.9722],
    '泉州': [118.3228,25.1147],
    '泰安': [117.0264,36.0516],
    '泰州': [120.0586,32.5525],
    '济南': [117.1582,36.8701],
    '济宁': [116.8286,35.3375],
    '海口': [110.3893,19.8516],
    '淄博': [118.0371,36.6064],
    '淮安': [118.927,33.4039],
    '深圳': [114.5435,22.5439],
    '清远': [112.9175,24.3292],
    '温州': [120.498,27.8119],
    '渭南': [109.7864,35.0299],
    '湖州': [119.8608,30.7782],
    '湘潭': [112.5439,27.7075],
    '滨州': [117.8174,37.4963],
    '潍坊': [119.0918,36.524],
    '烟台': [120.7397,37.5128],
    '玉溪': [101.9312,23.8898],
    '珠海': [113.7305,22.1155],
    '盐城': [120.2234,33.5577],
    '盘锦': [121.9482,41.0449],
    '石家庄': [114.4995,38.1006],
    '福州': [119.4543,25.9222],
    '秦皇岛': [119.2126,40.0232],
    '绍兴': [120.564,29.7565],
    '聊城': [115.9167,36.4032],
    '肇庆': [112.1265,23.5822],
    '舟山': [122.2559,30.2234],
    '苏州': [120.6519,31.3989],
    '莱芜': [117.6526,36.2714],
    '菏泽': [115.6201,35.2057],
    '营口': [122.4316,40.4297],
    '葫芦岛': [120.1575,40.578],
    '衡水': [115.8838,37.7161],
    '衢州': [118.6853,28.8666],
    '西宁': [101.4038,36.8207],
    '西安': [109.1162,34.2004],
    '贵阳': [106.6992,26.7682],
    '连云港': [119.1248,34.552],
    '邢台': [114.8071,37.2821],
    '邯郸': [114.4775,36.535],
    '郑州': [113.4668,34.6234],
    '鄂尔多斯': [108.9734,39.2487],
    '重庆': [107.7539,30.1904],
    '金华': [120.0037,29.1028],
    '铜川': [109.0393,35.1947],
    '银川': [106.3586,38.1775],
    '镇江': [119.4763,31.9702],
    '长春': [125.8154,44.2584],
    '长沙': [113.0823,28.2568],
    '长治': [112.8625,36.4746],
    '阳泉': [113.4778,38.0951],
    '青岛': [120.4651,36.3373],
    '韶关': [113.7964,24.7028]
}


class RealtimeRandomWeibo(object):
    KEY = '9LF3gnOtYENP26HSoNAxPptHk7eCgxdWjL5ZuSdJXuGALaAcTrLXdGI7TkEYnIQm'

    def __init__(self, lazy=True):
        self.href = 'http://api03.bitspaceman.com:8000/post/weibo?kw=的&apikey=' + self.KEY
        self.weibo_list = []
        self.weibo_list_all = []
        self.weibo_list_threat = []
        self.iter_all = None
        self.iter_count = 0
        if not lazy:
            self.get_random_weibo()

        # 连接至mongodb
        self.mongo_client = pymongo.MongoClient('localhost', 27017)
        self.db = self.mongo_client['Weibo']

    def get_random_weibo(self):
        self.iter_count += 15
        requests_get = requests.get(self.href, timeout=15)
        requests_content = requests_get.content
        requests_dict = json.loads(requests_content)

        weibo_list = self.parse_requests_dict(requests_dict)

        copy_of_weibo_list = self.parse_weibo_list(weibo_list)
        self.weibo_list_all = copy_of_weibo_list
        self.weibo_list_threat = [weibo for weibo in copy_of_weibo_list if int(weibo['threatened']) > 68]
        self.store_to_mongodb()

    def parse_requests_dict(self, requests_dict):
        weibo_list = []
        count = 0
        for item in requests_dict['data']:

            weibo = {}
            try:
                weibo['is_repost'] = False
                weibo['repost_location'] = ''
                weibo['text'] = str(item['mblog']['text'])
                print(weibo['text'])
                weibo['uid'] = str(item['from']['url']).split('/')[-1]
                weibo['time'] = str(item['pDate'])
                weibo['comment_count'] = str(item['commentCount'])
                weibo['author_name'] = str(item['from']['name'])
                weibo['author_uid'] = str(item['from']['id'])
                weibo['author_fans'] = str(item['from']['fansCount'])
                weibo['author_follower'] = str(item['from']['friendCount'])
                weibo['location'] = str(item['from']['extend']['location'])
                weibo['province'] = ''
                print(weibo['author_uid'])
            except:
                continue

            try:
                weibo['terminal_source'] = str(item['mblog']['source']).split('>')[1].split('<')[0]
            except IndexError:
                weibo['terminal_source'] = '未知'
            if item['mblog'].has_key('retweeted_status'):
                count += 1
                weibo['is_repost'] = True
                try:
                    weibo['repost_location'] = str(item['mblog']['retweeted_status']['user']['location'])
                    weibo['repost_reposted_count'] = str(item['mblog']['retweeted_status']['reposts_count'])
                    weibo['repost_text'] = str(item['mblog']['retweeted_status']['text'])
                    weibo['repost_attitude_count'] = str(item['mblog']['retweeted_status']['attitudes_count'])
                    print(weibo['repost_location'])
                    print(weibo['repost_reposted_count'])
                    print(weibo['repost_text'])
                    print(weibo['repost_attitude_count'])
                except:
                    pass

            weibo_list.append(weibo)

        print("为转发的微博数： ", str(count))
     #   self.store_to_mongodb(weibo_list)
        self.weibo_list = weibo_list
        print(weibo_list)

        return weibo_list

    def parse_weibo_list(self, weibo_list):
        """
        分析微博威胁程度与规范地址格式
        :param weibo_list: 初始微博列表
        :return: 分析后的微博列表
        """
        for i in weibo_list:
            i['location'] = mapped_province(i['location'], weibo=i)
            i['repost_location'] = mapped_province(i['repost_location'])
            print(i['location'], i['repost_location'])
        print('111111111111111111111111111111111111111111111111111')

        copy_of_weibo_list = []

        # 筛选符合地图显示的地点
        for i in weibo_list:
            if i['location'] is None or i['location'] == '':
                continue
            if i['repost_location'] is None or i['repost_location'] == '':
                i['is_repost'] = False

            i['location'] = str(i['location'])
            i['repost_location'] = str(i['repost_location'])
            copy_of_weibo_list.append(i)

        copy_of_weibo_list = assess_threat_levels(copy_of_weibo_list)
        return copy_of_weibo_list

    def store_to_mongodb(self):

        weibo_table = self.db[REALTIMEWEIBO]
        for i in self.weibo_list_all:
            weibo_table.insert(i)

        weibo_table = self.db[REALTIMEWEIBOT]
        for i in self.weibo_list_threat:
            weibo_table.insert(i)

    # def get_iter_all(self):
    #     weibo_table = self.db['realtime719']
    #     for i in weibo_table.find():
    #         yield i

    def get_realtime_weibo_from_mongodb(self):
        weibo_table = self.db[REALTIMEWEIBO]
        count = 0
        now_weibo_all = []
        for i in weibo_table.find():
            if count<self.iter_count:
                continue
            else:
                now_weibo_all.append(i)
        return now_weibo_all

    def get_realtime_weibo_from_mongodb(self):
        weibo_table = self.db[REALTIMEWEIBO]
        count = 0
        now_weibo_all = []
        for i in weibo_table.find():
            if count<self.iter_count:
                count += 1
                continue
            else:
                count+=1
                now_weibo_all.append(i)
        return now_weibo_all

    def get_realtime_weibo_of_province(self, target_province):
        weibo_table = self.db[REALTIMEWEIBO]
        target_province_weibo_list = []
        for i in weibo_table.find():
            if i['province'] == str(target_province):
                target_province_weibo_list.append(i)
        return target_province_weibo_list


mapped_dict = {
'北京':'北京',
'上海':'上海',
'天津':'天津',
'重庆':'重庆',
'河北':'石家庄',
'山西':'太原',
'辽宁':'沈阳',
'吉林':'长春',
'黑龙江':'哈尔滨',
'江苏':'南京',
'浙江':'杭州',
'安徽':'合肥',
'福建':'福州',
'江西':'南昌',
'山东':'济南',
'河南' :'郑州',
'湖北':'武汉',
'湖南':'长沙',
'广东':'广州',
'海南':'海口',
'四川':'成都',
'贵州':'贵阳',
'云南':'昆明',
'陕西':'西安',
'甘肃':'兰州',
'青海': '西宁',
'西藏' :'拉萨',
'广西':'南宁',
'内蒙':'呼和浩特',
'宁夏':'银川',
'新疆':'乌鲁木齐'
}


def mapped_province(weibo_location, weibo=None):
    """
    匹配省份
    """
    if len(weibo_location.split(' ')) > 1:
        if weibo and weibo_location.split(' ')[0] in mapped_dict.keys():
            weibo['province'] = weibo_location.split(' ')[0]

        if weibo_location.split(' ')[1] in location_dict.keys():
            weibo_location = weibo_location.split(' ')[1]
        elif weibo_location.split(' ')[0] in location_dict.keys():
            weibo_location = weibo_location.split(' ')[0]
        else:
            weibo_location = ''


    else:

        if weibo and weibo_location in mapped_dict.keys():
            weibo['province'] = weibo_location.strip()

        if weibo_location.strip() in location_dict.keys():
            weibo_location = weibo_location.strip()
        else:
            if weibo_location.strip() in mapped_dict.keys():
                print(weibo_location.strip())
                weibo_location = mapped_dict.get(weibo_location.strip())
            else:
                weibo_location = ''


    return weibo_location


def assess_threat_levels(copy_of_weibo_list):
    """
    评估威胁程度
    """
    check_object = fenci.TestKeyword()

    for weibo in copy_of_weibo_list:
        flag = check_object.test_if_has_keyword(weibo['text'])
        threat = 0
        if weibo['is_repost']:
            flag = flag or check_object.test_if_has_keyword(weibo['repost_text'])
        if flag:
            if weibo.has_key('repost_reposted_count') and weibo['repost_reposted_count']:
                if int(weibo['repost_reposted_count']) > 10:
                    threat += 1
            if weibo.has_key('comment_count') and weibo['comment_count']:
                if int(weibo['comment_count'] > 1):
                    threat += 1
            if weibo.has_key('repost_attitude_count') and weibo['repost_attitude_count']:
                if int(weibo['repost_attitude_count']) > 10:
                    threat += 1
            if weibo.has_key('author_fans') and weibo['author_fans']:
                if int(weibo['author_fans']) > 100:
                    threat += 1

            weibo['threatened'] = random.randint(68, 80)

            if threat == 1 or threat == 2:
                weibo['threatened'] = random.randint(80, 90)
                print('what?????????????????????')
                print(weibo['threatened'] )

            if threat > 2:
                weibo['threatened'] = random.randint(90, 100)
                print('what?????????????????????')
                print(weibo['threatened'] )

            print(weibo['time'])
            print(weibo['author_uid'])
        else:
            weibo['threatened'] = random.randint(0, 68)

    return copy_of_weibo_list


def start_run():

    realtime_weibo_object = RealtimeRandomWeibo()

    for i in realtime_weibo_object.weibo_list:
        i['location'] = mapped_province(i['location'], weibo=i)
        i['repost_location'] = mapped_province(i['repost_location'])
        print(i['location'], i['repost_location'])
    print('111111111111111111111111111111111111111111111111111')

    copy_of_weibo_list = []

    # 筛选符合地图显示的地点
    for i in realtime_weibo_object.weibo_list:
        if i['location'] is None or i['location'] == '':
            continue
        if i['repost_location'] is None or i['repost_location'] == '':
            i['is_repost'] = False

        i['location'] = str(i['location'])
        i['repost_location'] = str(i['repost_location'])
        copy_of_weibo_list.append(i)

    copy_of_weibo_list = assess_threat_levels(copy_of_weibo_list)
    return copy_of_weibo_list





if __name__ == '__main__':

    a = RealtimeRandomWeibo()
    a.get_random_weibo()
    l = a.get_realtime_weibo_from_mongodb()
    for i in l:
        print(i)
    # a = start_run()
    # for i in a:
    #     print(i['location'])
    #     print(type(i['location']))
    #     if i['is_repost']:
    #         print("转发自"+str(i['repost_location']))