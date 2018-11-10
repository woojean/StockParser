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
“均线汇合于实体”
'''
class MaConvergenceParser(BaseParser):
  _tag = 'MaConvergenceParser'
  
  def __init__(self,parseDay,id=''):
    BaseParser.__init__(self,parseDay) 

  # 是否处于平台当中
  def isInPlatform(self,res,parseDay):
    platformDays = 10
    # 平台期总涨跌幅小于5%
    dayList = BaseParser.getPastTradingDayList(parseDay,platformDays)
    day1 = dayList[0]
    day2 = dayList[-1]
    startPriceOfDay1 = self.getStartPriceOfDay(res,day1)
    endPriceOfDay2 = self.getEndPriceOfDay(res,day2)
    rate = (endPriceOfDay2 - startPriceOfDay1)/startPriceOfDay1
    if abs(rate) > 0.05:
      return False

    # 平台期每一日的涨跌幅绝对值不超过3%
    isExceed = False 
    dayList = BaseParser.getPastTradingDayList(parseDay,platformDays)
    l = len(dayList)
    for i in xrange(0,l-1):
      day1 = dayList[i]
      day2 = dayList[i+1]
      endPriceOfDay1 = self.getEndPriceOfDay(res,day1)
      endPriceOfDay2 = self.getEndPriceOfDay(res,day2)
      rate = abs((endPriceOfDay2 - endPriceOfDay1)/endPriceOfDay1)
      if rate > 0.03:
        isExceed = True
        break
    if isExceed:
      return False

    # 平台期的最高价序列、最低价序列的差额不超过10%
    minMaxPrice = 999999 # 最高价序列中的最小值
    maxMaxPrice = 0 # 最高价序列中的最大值
    minMinPrice = 999999 # 最低价序列中的最小值
    maxMinPrice = 0 # 最低价序列中的最大值
    dayList = BaseParser.getPastTradingDayList(parseDay,platformDays)
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
     
    isExceed = False # 每一日的最高价、最低价与边界值的差异小于5%
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



  def parse(self,res,parseDay,id=''):
    ret = False

    startPrice = self.getStartPriceOfDay(res,parseDay)
    endPrice = self.getEndPriceOfDay(res,parseDay)

    # 阳线
    if endPrice <= startPrice: 
      return False
    
    # 取均线
    dayList5 = BaseParser.getPastTradingDayList(parseDay,5)
    dayList10 = BaseParser.getPastTradingDayList(parseDay,10)
    dayList20 = BaseParser.getPastTradingDayList(parseDay,20)
    (v1,v2,ma5) = self.getMAPrice(res,dayList5)
    (v1,v2,ma10) = self.getMAPrice(res,dayList10)
    (v1,v2,ma20) = self.getMAPrice(res,dayList20)

    minMa = min(ma5,ma10,ma20)
    maxMa = max(ma5,ma10,ma20)


    # (maxMa - minMa) < endPrice*0.03
    if not ((maxMa - minMa) < endPrice*0.03):
      return False

    # 条件2
    maxP = max(ma5,ma10,ma20,endPrice)
    minP = min(ma5,ma10,ma20,endPrice)
    r = maxP/minP
    if r > 1.06:
      return False

    if not self.isInPlatform(res,parseDay):
      return False

    #
    # if minMa <= min(startPrice,endPrice):
    #   return False
    
    # if maxMa >= max(startPrice,endPrice):
    #   return False

    return True



if __name__ == '__main__':
  print 'MaConvergenceParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = MaConvergenceParser(parseDay).getParseResult(True)
  print idList

















