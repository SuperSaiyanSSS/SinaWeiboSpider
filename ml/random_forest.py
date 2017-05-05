# -*- coding: utf-8 -*
from __future__ import unicode_literals, print_function
from __future__ import division
import sklearn
import pandas as pd
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
import sklearn

if __name__ == "__main__":
    sina_store_object = sina_store.SinaStore()
    sina_store_object.weibo_table = sina_store_object.db['human_vector_info']
    iter = sina_store_object.get_stored_information()
    info_dict = next(iter)
    print(info_dict)
    print(info_dict['uid'])