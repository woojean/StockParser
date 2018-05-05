#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-05-05
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
from HotPointSniffer import HotPointSniffer

reload(sys)
sys.setdefaultencoding('utf-8')

rootPath = sys.path[0][0:sys.path[0].index('StockParser')]+'StockParser'
sys.path.append(rootPath+'/src') 
from common import Tools

'''
61 个行业  => 6
189 个概念 => 19
31 个地域  => 3
共281个板块
'''


class ColdPointSniffer(HotPointSniffer): 
  _source = 'cold-point-sniffer'

  def __init__(self): 
    self._dataPath = self._source
    self._failedDataPath = 'failed_' + self._source
  

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
TOP_BK_NUM = 28  # Top 5% + 2
RESONANCE_NUM = 3 # Resonance atleast 2
REVERSE = True 


if __name__ == '__main__':
  print 'ColdPointSniffer'
  ColdPointSniffer().initDir()
  sniffer = ColdPointSniffer()
  sniffer.run()



