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
 
reload(sys)
sys.setdefaultencoding('utf-8')

'''
最高价低于5日线的大阳线
'''
class MaxPriceUnderMaParser(BaseParser):
  _tag = 'MaxPriceUnderMaParser'
  
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
    dayList = BaseParser.getPastTradingDayList(parseDay,5)
    (v,v,ma) = self.getMAPrice(res,dayList)
    startPrice = self.getStartPriceOfDay(res,parseDay)
    endPrice = self.getEndPriceOfDay(res,parseDay)
    minPrice = self.getMinPriceOfDay(res,parseDay)
    maxPrice = self.getMaxPriceOfDay(res,parseDay)
    endPriceOfLastDay = self.getEndPriceOfDay(res,dayList[-2])
    

    # 阳线
    if endPrice <= startPrice:
      return False


    # 位于ma之下 = 最高价低于ma
    if maxPrice >= ma:
      return False


    # 向上波幅大于7%
    minP = min(endPriceOfLastDay,minPrice)  # 取昨日收盘价和今日最低价中的最小值
    r = (maxPrice - minP)/minP
    if (r <= 0.07):
      return False


    # SLOWKD近期有死叉
    # if KdjParser.haveDeathCross(parseDay,id,5,5):
      # return False
    

    return True



if __name__ == '__main__':
  print 'MaxPriceUnderMaParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = MaxPriceUnderMaParser(parseDay).getParseResult(True)
  print idList

















