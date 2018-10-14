#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-10-11
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
连续小阳线
'''
class ContinuouslyRiseLineParser(BaseParser):
  _tag = 'ContinuouslyRiseLineParser'
  
  def __init__(self,parseDay,id=''):
    BaseParser.__init__(self,parseDay) 

  def parse(self,res,parseDay,id=''):
    days = 5
    amplitudeLimit = 0.05
    isContinuouslyRiseLine = True

    # 5日线在10日线上
    dayList = BaseParser.getPastTradingDayList(parseDay,5)
    (v,v,ma5) = self.getMAPrice(res,dayList)
    dayList = BaseParser.getPastTradingDayList(parseDay,10)
    (v,v,ma10) = self.getMAPrice(res,dayList)
    if ma5 < ma10:
      return False


    dayList = BaseParser.getPastTradingDayList(parseDay,days)
    minPriceOfDays = 99999
    maxPriceOfDays = 0
    for day in dayList:
      startPrice = self.getStartPriceOfDay(res,day)
      endPrice = self.getEndPriceOfDay(res,day)
      minPrice = self.getMinPriceOfDay(res,day)
      maxPrice = self.getMaxPriceOfDay(res,day)
      
      if startPrice == 0 or endPrice ==0 or minPrice == 0 or maxPrice==0: # 排除错误数据
        isContinuouslyRiseLine = False
        break

      if endPrice <= startPrice: # 阳线
        isContinuouslyRiseLine = False
        break

      if minPrice < minPriceOfDays:
        minPriceOfDays = minPrice

      if maxPrice > maxPriceOfDays:
        maxPriceOfDays = maxPrice

    if not isContinuouslyRiseLine:
      return False

    # 振幅判断
    amplitude = (maxPriceOfDays - minPriceOfDays)/minPriceOfDays
    if amplitude > 0.05:
      return False

    return True


if __name__ == '__main__':
  print 'ContinuouslyRiseLineParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = ContinuouslyRiseLineParser(parseDay).getParseResult(True)
  print idList

















