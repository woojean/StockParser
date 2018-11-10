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
换手率选股
'''
class CrParser(BaseParser):
  _tag = 'CrParser'
  
  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 

  

  def parse(self,res,parseDay,id=''):
    # 换手率
    crStatus = True
    dayList = BaseParser.getPastTradingDayList(parseDay,10)
    for day in dayList:
      cr = self.getChangeRateOfDay(res,parseDay)
      if cr < 0.1 or cr > 0.20:
        crStatus = False
        break

    if not crStatus:
      return False

    # 区间涨幅
    # day1  = dayList[0]
    # day2  = dayList[-1]
    # endPrice1 = self.getEndPriceOfDay(res,day1)
    # endPrice2 = self.getEndPriceOfDay(res,day2)
    # gr = (endPrice2 - endPrice1)/endPrice1
    
    # if id  == '002464':
    #   print day1,endPrice1
    #   print day2,endPrice2
    #   print gr

    # if gr > 0.05:
    #   return False

    # 区间振幅
    minPrice = 999999
    maxPrice = 0
    for day in dayList:
      minP = self.getMinPriceOfDay(res,day)
      if minP < minPrice:
        minPrice = minP

    for day in dayList:
      maxP = self.getMaxPriceOfDay(res,day)
      if maxP > maxPrice:
        maxPrice = maxP

    ar = (maxPrice - minPrice)/minPrice
    if ar >0.12:
      return False


    return True


if __name__ == '__main__':
  print 'CrParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = CrParser(parseDay).getParseResult(True)
  print idList

















