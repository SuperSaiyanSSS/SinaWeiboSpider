# -*- coding: utf-8 -*-
from weibospider import WeiboClient
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#cookies = \
#'ALF=1504271525; SCF=AjsEaVa0e8KjEg3yEjwEx270PLOpYvK-1BhV7AdkMSQgREMFA0bd3IqV3weK9ydf5NAbDXjKT69Rfndb2m9Ah4I.; SUB=_2A250hb_2DeRhGeNH7VIV9izNwj2IHXVXicG-rDV6PUNbktANLRPhkW1ZeSLr49kFNMgwrWThnh1bPUhWPw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhaydrjX2CLPhFdjQ77gn4P5JpX5KMhUgL.Fo-4So5XSozp1K22dJLoI0YLxK.LB.-L1K.LxKML12qLBK5LxKqL1KBLBo.LxK.LB-BL1KBLxKBLB.2LB.2LxK-LBonL1heLxKqLB-eLBKMt; SUHB=03oF_eQuesy4xQ; SSOLoginState=1501679526; _T_WM=544d051d212d2d6f3adece8b6949b373'

cookies = 'ALF=1512959361; SCF=AlGHrwmWqyhSdpml9a836b5TfwBwT3_aqlPQLm4VGPX5AnF7W-51O8sb-246XgliUA_jtEUQg3I0XisboShzSK4.; SUB=_2A253Ah7JDeRhGeNH7VIV9izNwj2IHXVUDKKBrDV6PUJbktAKLUehkW02ueHV00_NzZ0DwjSbUFYBB6B69g..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhaydrjX2CLPhFdjQ77gn4P5JpX5K-hUgL.Fo-4So5XSozp1K22dJLoI0YLxK.LB.-L1K.LxKML12qLBK5LxKqL1KBLBo.LxK.LB-BL1KBLxKBLB.2LB.2LxK-LBonL1heLxKqLB-eLBKMt; SUHB=0M2Flmef-A-AIV; SSOLoginState=1510370969; _T_WM=28de7b7a225087a87cbe9c2ad92df1ea'

if __name__ == '__main__':
    pe0 = WeiboClient(cookies=cookies)
    pe2 = pe0.Weibo('E6iRJofK6')
    pe4 = pe0.People('1884866222')
    print(pe4)
    print(pe4.name)
    print(pe4.weibo_count)
    print(pe4.location)
    pe2_people = pe2.author
    print('______test________')
    print(pe2_people.name)
    print(pe2_people.weibo_count)
    for i, j in zip(range(3), pe2_people.weibo):
        print(j.text)
        for ii, jj in zip(range(4), j.repost):
            print(jj.author_name)


