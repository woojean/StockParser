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
from KdjParser import KdjParser
from BiasParser import BiasParser
 
reload(sys)
sys.setdefaultencoding('utf-8')

'''
'''
class DailyParser(BaseParser):
  _tag = 'DailyParser'
  
  def __init__(self,parseDay,id=''):
    BaseParser.__init__(self,parseDay) 

  def isMaxPriceUnderMa(self,res,day,days):
    maxPrice = self.getMaxPriceOfDay(res,day)
    dayList = BaseParser.getPastTradingDayList(day,days)
    (v,v,ma) = self.getMAPrice(res,dayList)
    if maxPrice < ma:
      return True
    return False


  def isUpwardLimit(self,res,parseDay):
    dayList = BaseParser.getPastTradingDayList(parseDay,2)
    endPrice1 = self.getEndPriceOfDay(res,dayList[-2])
    endPrice2 = self.getEndPriceOfDay(res,dayList[-1])
    if endPrice1 == 0 or  endPrice2 == 0:
      return False
    r = (endPrice2 - endPrice1)/endPrice1
    if r < 0.09:
      return False
    return True

  def isRgbBear(self,res,day):
    R = 5
    G = 10
    B = 20

    dayList = self.getPastTradingDayList(day,R)
    (v,v,maR) = self.getMAPrice(res,dayList)

    dayList = self.getPastTradingDayList(day,G)
    (v,v,maG) = self.getMAPrice(res,dayList)

    dayList = self.getPastTradingDayList(day,B)
    (v,v,maB) = self.getMAPrice(res,dayList)

    if ((maR < maG) and (maG < maB)):
      return True
    return False


  def isLongUpLine(self,res,parseDay):
    startPrice = self.getStartPriceOfDay(res,parseDay)
    endPrice = self.getEndPriceOfDay(res,parseDay)
    minPrice = self.getMinPriceOfDay(res,parseDay)
    maxPrice = self.getMaxPriceOfDay(res,parseDay)
    totalLine = maxPrice - minPrice
    upLine = maxPrice - max(startPrice,endPrice)
    if totalLine == 0 :
      return True
    r = upLine/totalLine
    if r > 0.33:
      return True
    return False


  def parse(self,res,parseDay,id=''):
    # 取参
    dayList = BaseParser.getPastTradingDayList(parseDay,5) # 5日线
    (v,v,ma) = self.getMAPrice(res,dayList)
    startPrice = self.getStartPriceOfDay(res,parseDay)
    endPrice = self.getEndPriceOfDay(res,parseDay)
    minPrice = self.getMinPriceOfDay(res,parseDay)
    maxPrice = self.getMaxPriceOfDay(res,parseDay)
    startPriceOfLastDay = self.getStartPriceOfDay(res,dayList[-2])
    endPriceOfLastDay = self.getEndPriceOfDay(res,dayList[-2])
    minPriceOfLastDay = self.getMinPriceOfDay(res,dayList[-2])
    maxPriceOfLastDay = self.getMaxPriceOfDay(res,dayList[-2])

    # 参数校验
    if startPrice ==0 or endPrice ==0 or minPrice ==0 or maxPrice ==0:
      return False
    if ma < 0:
      return False

    ###############################################################
    # 阳线
    # if endPrice <= startPrice:
    #   return False

    # 最高价位于ma之下
    if maxPrice >= ma:
      return False

    # 振幅大于n%
    # minP = minPrice  # 取昨日收盘价和今日最低价中的最小值
    # r = (maxPrice - minP)/minP
    # if (r < 0.05):
    #   return False


    return True



if __name__ == '__main__':
  print 'DailyParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = DailyParser(parseDay).getParseResult(True)
  print idList

















