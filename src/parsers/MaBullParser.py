#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-10-03
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
'''
class MaBullParser(BaseParser):
  _tag = 'MaBullParser'
  
  def __init__(self,parseDay,id=''):
    BaseParser.__init__(self,parseDay) 
  

  def parse(self,res,parseDay,id=''):
    dayList = self.getPastTradingDayList(parseDay,5)
    (v,v,ma5) = self.getMAPrice(res,dayList)
    if ma5<=0:
      return False

    dayList = self.getPastTradingDayList(parseDay,10)
    (v,v,ma10) = self.getMAPrice(res,dayList)
    if ma10<=0:
      return False
    if ma5 < ma10:
      return False

    dayList = self.getPastTradingDayList(parseDay,20)
    (v,v,ma20) = self.getMAPrice(res,dayList)
    if ma20<=0:
      return False
    if ma10 < ma20:
      return False

    dayList = self.getPastTradingDayList(parseDay,60)
    (v,v,ma60) = self.getMAPrice(res,dayList)
    if ma60<=0:
      return False
    if ma20 < ma60:
      return False

    dayList = self.getPastTradingDayList(parseDay,250)
    (v,v,ma250) = self.getMAPrice(res,dayList)
    if ma250<=0:
      return False
    if ma60 < ma250:
      return False

    return True



if __name__ == '__main__':
  print 'MaBullParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = MaBullParser(parseDay).getParseResult(True)
  print idList

















