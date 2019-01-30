#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-10-29
'''

import os
import re
import requests,time
import shutil
import sys
import threading
import time
import datetime
from BaseParser import BaseParser
 
reload(sys)
sys.setdefaultencoding('utf-8')


rootPath = sys.path[0][0:sys.path[0].index('StockParser')]+'/StockParser'
sys.path.append(rootPath+'/src') 
from common import Tools


'''
大阳线、缺口、突破（线索1、2、3）
'''
class AdamParser(BaseParser):
  _tag = 'AdamParser'
  
  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 

  

  def parse(self,res,parseDay,id=''):
    
    # 最近发生向上跳空
    # ----------------------------------------------------------------------------------------
    ret = False
    dayList = self.getPastTradingDayList(parseDay,20)
    for day in dayList:
      if self.isUpwardGap(res,day):
        print day
        ret = True
        break
    
    return ret


if __name__ == '__main__':
  print 'AdamParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = AdamParser(parseDay).getParseResult(True)
  print idList

















