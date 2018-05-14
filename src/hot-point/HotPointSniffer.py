#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-05-03
'''

import os
import re
import copy
import requests,time
import shutil
import sys
import threading
import time
import new
from operator import itemgetter 
from BaseHotPoint import BaseHotPoint

reload(sys)
sys.setdefaultencoding('utf-8')

rootPath = sys.path[0][0:sys.path[0].index('StockParser')]+'StockParser'
sys.path.append(rootPath+'/src') 
from common import Tools

'''
抓取靠前的板块
'''


class HotPointSniffer(BaseHotPoint): 
  _source = 'hot-point-sniffer'

  def __init__(self): 
    self._dataPath = self._source
    self._failedDataPath = 'failed_' + self._source
  

  def getFilteredBkList(self,n,reverse = False):
    print 'getFilteredBkList...'
    d = self.getRootPath()+'/data/'+self._dataPath+'/'
    bkList = []
    topBkList = []
    for bk,url in self._BKs.items():
      path = d + bk
      res = open(path,'r').read()
      l = re.findall('"(.*?)"', res)
      for item in l:
        arr = item.split(',')
        '''
        ['1', 'BK0458', '\xe4\xbb\xaa\xe5\x99\xa8\xe4\xbb\xaa\xe8\xa1\xa8', '1.95', '268981406042', '1.27', '38|2|3|2', '300007', '2', '\xe6\xb1\x89\xe5\xa8\x81\xe7\xa7\x91\xe6\x8a\x80', '15.97', '9.99', '300515', '2', '\xe4\xb8\x89\xe5\xbe\xb7\xe7\xa7\x91\xe6\x8a\x80', '11.00', '-2.65', '2', '7671.56', '146.92']
        '''
        if 'BK' != arr[1][:2]:
          continue
        #if arr[1] in ['BK0816','BK0815']:  # BK0816 昨日连板，BK0815 昨日涨停
        #  continue
        bkData = (arr[1],arr[2],arr[3])  # 板块编码、板块名称、板块涨幅
        bkList.append(bkData)
    length = len(bkList)
    print "\n板块总数："+str(length)+"\n"
    self.dumpBkDict(bkList)  # 保存文件到本地方便后续查询
    bkList = sorted(bkList,key=lambda x: (-float(x[2])if('-'!=x[2])else(0)))
    #bkList = sorted(bkList,key=itemgetter(2), reverse=True)
    if not reverse:
      topBkList = bkList[:n]  # <----------------------------------------------------------------------------------------
    else:
      topBkList = bkList[len(bkList)-n:]
    self.dumpFilteredBkDict(topBkList)
    return topBkList
  

  def getFilteredIdList(self,minBkNum=2):
    print 'getFilteredIdList...'
    count = {}
    d = self.getRootPath()+'/data/'+self._dataPath+'/'
    for root,dirs,files in os.walk(d):
      for f in files:
        try:
          if 'BK'== f[:2]:
            path = root + f
            res = open(path,'r').read()
            l = re.findall('"(.*?)"', res)
            for item in l:
              '''
              2018-05-03 
              2,002681,奋达科技,9.41,0.86,10.06%,9.71,165823,153715449,8.55,8.59,9.41,8.58,-,-,-,-,-,-,-,-,0.00%,2.99,2.28,64.40,2012-06-05
              
              1 代码  2 名称  3 价格  4 价格增长  5 涨幅  6 振幅  23 换手率
              '''
              arr = item.split(',')
              id = arr[1]
              if 6 == len(id):
                if count.has_key(id):
                  count[id]['bkList'].append(f)
                else:
                  count[id] = {}
                  count[id]['basicInfo'] = arr
                  count[id]['bkList'] = [f]
        except Exception, e:
          pass
          print repr(e)
    filterdIdList = []
    for id,data in count.items():
      if len(data['bkList']) >= minBkNum:  # <----------------------------------------------------------------------------------------
        filterdIdList.append((id,data))
    return filterdIdList



  def run(self):
    # 获取板块数据
    self.genBKdata()

    # 过滤板块
    bkList = self.getFilteredBkList(TOP_BK_NUM,REVERSE) 

    # 获取板块个股数据
    self.genBkStockData(bkList)

    # 过滤个股 
    idList = self.getFilteredIdList(RESONANCE_NUM)
    print idList
    
    self.dumpReport(idList,RESONANCE_NUM)


# config
# ===============================================================
TOP_BK_NUM = 14  # Top n% 
RESONANCE_NUM = 2 # Resonance atleast 2
REVERSE = False 


if __name__ == '__main__':
  print 'HotPointSniffer'
  HotPointSniffer().initDir()
  sniffer = HotPointSniffer()
  sniffer.run()



