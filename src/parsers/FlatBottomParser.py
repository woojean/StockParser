#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-01-06
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

'''
平底
'''
class FlatBottomParser(BaseParser):
  _tag = 'FlatBottomParser'
  
  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 


  
  


  def parse(self,res,parseDay,id=''):
    
    # 前期跌势当日MA60小于20日前MA60
    dayList = BaseParser.getPastTradingDayList(parseDay,20)
    day1 = dayList[0]
    day2 = dayList[-1]
    dayList1 = BaseParser.getPastTradingDayList(day1,60)
    dayList2 = BaseParser.getPastTradingDayList(day2,60)
    (v,v,ma1) = self.getMAPrice(res,dayList1)
    (v,v,ma2) = self.getMAPrice(res,dayList2)
    if ma2 > ma1:
      return False

    # 连续10日涨跌幅绝对值不超过3%
    isExceed = False 
    dayList = BaseParser.getPastTradingDayList(parseDay,10)
    l = len(dayList)
    for i in xrange(0,l-1):
      day1 = dayList[i]
      day2 = dayList[i+1]
      endPriceOfDay1 = self.getEndPriceOfDay(res,day1)
      endPriceOfDay2 = self.getEndPriceOfDay(res,day2)
      rate = abs((endPriceOfDay2 - endPriceOfDay1)/endPriceOfDay1)
      if rate > 0.02:
        isExceed = True
        break
    if isExceed:
      return False

    # 连续10日的最高价序列、最低价序列的差额
    minMaxPrice = 999999
    maxMaxPrice = 0
    minMinPrice = 999999
    maxMinPrice = 0
    dayList = BaseParser.getPastTradingDayList(parseDay,10)
    for day in dayList:
      minPrice = self.getMinPriceOfDay(res,day)
      maxPrice = self.getMaxPriceOfDay(res,day)
      if minPrice > maxMinPrice:
        maxMinPrice = minPrice
      if minPrice < minMinPrice:
        minMinPrice = minPrice

      if maxPrice > maxMaxPrice:
        maxMaxPrice = maxPrice
      if maxPrice < minMaxPrice:
        minMaxPrice = maxPrice

    isExceed = False 
    maxRate = 0.05
    for day in dayList:
      minPrice = self.getMinPriceOfDay(res,day)
      maxPrice = self.getMaxPriceOfDay(res,day)
      rate = abs((minPrice-minMinPrice)/minMinPrice)
      if rate > maxRate:
        isExceed = True
        break

      rate = abs((minPrice-maxMinPrice)/maxMinPrice)
      if rate > maxRate:
        isExceed = True
        break

      rate = abs((maxPrice-minMaxPrice)/minMaxPrice)
      if rate > maxRate:
        isExceed = True
        break

      rate = abs((maxPrice-maxMaxPrice)/maxMaxPrice)
      if rate > maxRate:
        isExceed = True
        break

    if isExceed:
      return False

    return True


if __name__ == '__main__':
  print 'FlatBottomParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = FlatBottomParser(parseDay).getParseResult(True)
  print idList

















